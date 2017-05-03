#! /usr/bin/env python

import argparse
import json
import os
import pprint
import shelve
from collections import namedtuple
from datetime import datetime, timedelta

import requests


class Weather:
    city_list = None
    api_key = ''
    api_limit = timedelta(minutes=10)
    last_call_time = None
    WeatherData = None

    def __init__(self, last_call_time=None):
        with open('API_key.txt', 'r') as file:
            self.api_key = file.readline().strip('\n')

        with open('city.list.json', 'r') as file:
            self.city_list = json.load(file)

        if os.path.isfile('weather.db'):
            with shelve.open('weather') as file:
                self.last_call_time = last_call_time or file['last_call_time']
        else:
            # open and close the shelf so it will exist going forward
            shelfFile = shelve.open('weather')
            shelfFile['last_call_time'] = datetime(1988, 6, 6)
            self.last_call_time = last_call_time or shelfFile['last_call_time']
            shelfFile.close()

    def get_city_id_by_name(self, name):
        for city in self.city_list:
            if city["name"] == name:
                return city["id"]
        return None

    def check_if_within_limit(self):
        return (datetime.now() - self.last_call_time) > self.api_limit

    def store_current_time(self):
        now = datetime.now()
        with shelve.open('weather') as file:
            file['last_call_time'] = now
        self.last_call_time = now

    def request_weather_with_id(self, id):
        params = {'APPID': self.api_key, 'id': id}
        base_url = 'http://api.openweathermap.org/data/2.5/weather'

        # check last call time to rate limit
        if self.check_if_within_limit():
            response = requests.get(base_url, params=params)
            weather_data = response.json()
            response = response
            WeatherData = namedtuple('WeatherData', ['json', 'response'])
            self.WeatherData = WeatherData(weather_data, response)
            self.store_current_time()

    def get_weather_by_id(self, city_name, forecast=False):
        '''Links together the other methods to retrieve the weather data

        Returns:
            None: Returns None when the city name is not found in the city_list
            WeatherData.json (json): The json weather data stored on the
                object's WeatherData named tuple.
        '''
        city_id = self.get_city_id_by_name(city_name)
        if not city_id:
            raise KeyError(f'No city found matching {city_name}')
        self.request_weather_with_id(city_id)
        self.display_weather()

    def display_weather(self):
        '''Display the json in a pleasing manner'''
        pprint.pprint(self.WeatherData.json)
        weather_dict = self.WeatherData.json
        result_city = weather_dict['name']
        weather_description = weather_dict['weather'][0]['description']
        Temps_F = convert_temps(weather_dict['main'])
        sunrise = convert_timestamp(weather_dict['sys']['sunrise'])
        sunset = convert_timestamp(weather_dict['sys']['sunset'])

        width = 10
        print(f'Current weather for {result_city}:')
        print(f'Weather description: {weather_description}')
        print(f'Temperature:')
        print(f'  Current: {Temps_F.current:{width}}')
        print(f'  High: {Temps_F.high:{width}}')
        print(f'  Low: {Temps_F.low:{width}}')
        print(f'Sunrise: {sunrise}')
        print(f'Sunset: {sunset}')


def convert_temps(temp_dict):
    current_temp_f = round((temp_dict['temp'] * (9 / 5) - 459.67), 2)
    max_temp_f = round((temp_dict['temp_max'] * (9 / 5) - 459.67), 2)
    min_temp_f = round((temp_dict['temp_min'] * (9 / 5) - 459.67), 2)
    Temps_F = namedtuple('Temps_F', ['current', 'high', 'low'])
    return Temps_F(current_temp_f, max_temp_f, min_temp_f)


def convert_timestamp(UTC_timestamp):
    time = datetime.fromtimestamp(UTC_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time



def main():
    parser = argparse.ArgumentParser(
        description='Get the weather in your terminal')
    parser.add_argument('city', help='The city for which you would like the \
                        weather')
    parser.add_argument('-f', '--forecast', dest='forecast',
                        action='store_true')
    parser.add_argument('-d', '--datetime', dest='datetime',
                        action='store_true', help='For development purposes \
                        only')
    args = parser.parse_args()
    if args.datetime:
        w = Weather(datetime(1970, 1, 1))
    else:
        w = Weather()
    w.get_weather_by_id(args.city, args.forecast)


if __name__ == '__main__':
    main()
