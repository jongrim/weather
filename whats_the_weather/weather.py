import json
import os
import shelve
from datetime import datetime, timedelta

import requests


class Weather:
    '''
    Request and store weather data for a city.

    Attributes:
        city_list (list): A list loaded from a json file of the openweatherapi
            city names and IDs.
        api_key (string): The api key to use for requests loaded from
            'API_key.txt'.
        api_limit (timedelta): The minimum amount of time that must pass
            between api calls.
        last_call_time (datetime): The time of the last api call.
        wthr_data_dict (dict): A dictionary to store weather data for any city
            that has been searched for.
        root_dir (string): Defaults to the path in which the application is
            installed. Used to determine the location of other files.
        data_dir (string): The path where data files are stored including
            city.list.json and API_key.txt.
        data_paths (dict): A dictionary of paths used for ease of reference.
    '''
    city_list = None
    api_key = ''
    api_limit = timedelta(minutes=10)
    last_call_time = None
    wthr_data_dict = {}
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, 'data/')
    data_paths = {
        'api': os.path.join(data_dir, 'API_key.txt'),
        'city_list': os.path.join(data_dir, 'city.list.json'),
        'db': os.path.join(data_dir, 'weather')
    }

    def __init__(self, last_call_time=None):
        if not os.path.isfile(self.data_paths['api']):
            self.setup_data_directory_and_files()

        with open(self.data_paths['api'], 'r') as file:
            self.api_key = file.readline().strip('\n')

        with open(self.data_paths['city_list'], 'r') as file:
            self.city_list = json.load(file)

        if os.path.isfile("{self.data_paths['db']+'.db'}"):
            self.restore_saved_info(last_call_time)
        else:
            self.make_shelf_file(last_call_time)

    def get_city_id_by_name(self, name):
        '''Translate a city name into an ID.

        Returns:
            city["id"] (int): The ID of the city requested.
            None: Returns None if no match is found.
        '''
        for city in self.city_list:
            if city["name"] == name:
                return city["id"]
        return None

    def check_if_within_limit(self):
        '''Determine if a new api request is permissible per time limit.

        Returns:
            True (bool): Return True if the time since the last call exceeds
                the necessary time limit.
            False (bool): Return False if the time since the last call does
                not exceed the necessary time limit.
        '''
        return (datetime.now() - self.last_call_time) > self.api_limit

    def make_shelf_file(self, last_call_time):
        '''Create the shelf file used for data storage.'''
        shelfFile = shelve.open(self.data_paths['db'])
        shelfFile['last_call_time'] = datetime(1988, 6, 6)
        self.last_call_time = last_call_time or shelfFile['last_call_time']
        shelfFile.close()

    def restore_saved_info(self, last_call_time):
        '''Load the data from the shelf file'''
        with shelve.open(self.data_paths['db']) as file:
            self.last_call_time = last_call_time or file['last_call_time']
            self.wthr_data_dict = file['weather_data']

    def store_current_info(self):
        '''Store the last call time and weather data for future reference'''
        now = datetime.now()
        with shelve.open(self.data_paths['db']) as file:
            file['last_call_time'] = now
            file['weather_data'] = self.wthr_data_dict
        self.last_call_time = now

    def request_weather_with_id(self, city_id, forecast=None):
        '''Request current weather conditions for the supplied city id and
        update the instance variables last_call_time and wthr_data_dict.
        '''
        # Builds params and url for the api request
        params = {'APPID': self.api_key, 'id': city_id}
        if forecast:
            base_url = 'http://api.openweathermap.org/data/2.5/forecast'
        else:
            base_url = 'http://api.openweathermap.org/data/2.5/weather'

        # Makes sure the dictionary is initialized properly
        cur_city = self.wthr_data_dict.setdefault(
            city_id, {'forecast': {}, 'current': {}})

        # check last call time to rate limit
        if self.check_if_within_limit():
            response = requests.get(base_url, params=params)
            if forecast:
                cur_city['forecast']['json'] = response.json()
            else:
                cur_city['current']['json'] = response.json()
            self.store_current_info()

    def get_the_weather(self, city_name, forecast=False):
        '''Get the current weather or forecast weather for the city specified.
        This is the entry point to the module from __main__.

        Raises:
            KeyError: raised when city_name does not match any in the
                city.list.json file.
        Returns:
            city_id: the id of the city for which weather info was requested.
        '''
        city_id = self.get_city_id_by_name(city_name)
        if not city_id:
            raise KeyError(f'No city found matching {city_name}')
        self.request_weather_with_id(city_id, forecast)
        return city_id

    def setup_data_directory_and_files(self):
        '''Create the data directory and store the API key in the proper file'''
        os.chdir(self.data_dir)
        key = input('Enter openweathermap api key:\n')
        while not key:
            input('Please enter your api key for openweathermap:\n')
        with open(self.data_paths['api'], 'w') as file:
            file.write(key + '\n')
