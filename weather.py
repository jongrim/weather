#! /usr/bin/env python

import json
import os
import shelve
from datetime import datetime, timedelta

import requests


class Weather:
    city_list = None
    api_key = ''
    api_limit = timedelta(minutes=10)
    last_call_time = None
    wthr_data_dict = {}

    def __init__(self, last_call_time=None):
        with open('API_key.txt', 'r') as file:
            self.api_key = file.readline().strip('\n')

        with open('city.list.json', 'r') as file:
            self.city_list = json.load(file)

        if os.path.isfile('weather.db'):
            self.restore_saved_info(last_call_time)

        else:
            self.make_shelf_file(last_call_time)

    def get_city_id_by_name(self, name):
        for city in self.city_list:
            if city["name"] == name:
                return city["id"]
        return None

    def check_if_within_limit(self):
        return (datetime.now() - self.last_call_time) > self.api_limit

    def make_shelf_file(self, last_call_time):
        shelfFile = shelve.open('weather')
        shelfFile['last_call_time'] = datetime(1988, 6, 6)
        self.last_call_time = last_call_time or shelfFile['last_call_time']
        shelfFile.close()

    def restore_saved_info(self, last_call_time):
            with shelve.open('weather') as file:
                self.last_call_time = last_call_time or file['last_call_time']
                self.wthr_data_dict = file['weather_data']

    def store_current_info(self):
        '''Store the last call time and weather data for future reference'''
        now = datetime.now()
        with shelve.open('weather') as file:
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

    def get_weather_by_id(self, city_name, forecast=False):
        '''Links together the other methods to retrieve the weather data.

        Raises:
            KeyError: raised when city_name does not match any in the
                city.list.json file.
        '''
        city_id = self.get_city_id_by_name(city_name)
        if not city_id:
            raise KeyError(f'No city found matching {city_name}')
        self.request_weather_with_id(city_id, forecast)
        return city_id
