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
    weather_data_dict = {}

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
                self.weather_data_dict = file['weather_data']

    def store_current_info(self):
        '''Store the last call time and weather data for future reference'''
        now = datetime.now()
        with shelve.open('weather') as file:
            file['last_call_time'] = now
            file['weather_data'] = self.weather_data_dict
        self.last_call_time = now

    def request_weather_with_id(self, id, forecast):
        '''Request current weather conditions for the supplied city id and
        update the instance variables last_call_time and weather_data_dict.
        '''
        params = {'APPID': self.api_key, 'id': id}
        base_url = 'http://api.openweathermap.org/data/2.5/weather'

        # check last call time to rate limit
        if self.check_if_within_limit():
            response = requests.get(base_url, params=params)
            self.weather_data_dict['json'] = response.json()
            self.weather_data_dict['response'] = response
            self.store_current_info()

    def get_weather_by_id(self, city_name, forecast=False, indent=2):
        '''Links together the other methods to retrieve the weather data.

        Raises:
            KeyError: raised when city_name does not match any in the
                city.list.json file.
        '''
        city_id = self.get_city_id_by_name(city_name)
        if not city_id:
            raise KeyError(f'No city found matching {city_name}')
        self.request_weather_with_id(city_id, forecast)
        self.display_weather(forecast, indent)

    def display_weather(self, forecast, indent):
        '''Display the json in a pleasing manner'''
        weather_dict = self.weather_data_dict['json']
        result_city = weather_dict['name']
        weather_description = weather_dict['weather'][0]['description']
        Temps_F = convert_temps(weather_dict['main'])
        sunrise = convert_timestamp(weather_dict['sys']['sunrise'])
        sunset = convert_timestamp(weather_dict['sys']['sunset'])
        rain = weather_dict.get('rain', None)
        clouds = weather_dict.get('clouds', None)
        wind = weather_dict.get('wind', None)
        snow = weather_dict.get('snow', None)

        space = ' ' * indent

        if forecast:
            pass
        else:
            print(f'Current weather for {result_city}:')
            print(f'{space}Weather description: {weather_description}')
            print(f'{space}Temperatures:')
            print(f'{space}{space}Current: ', f'{Temps_F.current}'.rjust(5))
            print(f'{space}{space}Max: ', f'{Temps_F.max}'.rjust(9))
            print(f'{space}{space}Min: ', f'{Temps_F.min}'.rjust(9))
            print(f"{space}Humidity: {weather_dict['main']['humidity']}%")
            print(f'{space}Sunrise: {sunrise}')
            print(f'{space}Sunset: {sunset}')
            if rain:
                print(f"{space}Rain volume for last 3 hours: {rain['3h']}")
            if clouds:
                print(f"{space}Cloudiness: {clouds['all']}")
            if wind:
                print(f"{space}Wind speed: {wind['speed']} meter/sec")
                print(f"{space}Wind direction: {wind['deg']} degrees")
            if snow:
                print(f"{space}Snow volume for last 3 hours: {snow['3h']}")


def convert_temps(temp_dict):
    current_temp_f = round((temp_dict['temp'] * (9 / 5) - 459.67), 2)
    max_temp_f = round((temp_dict['temp_max'] * (9 / 5) - 459.67), 2)
    min_temp_f = round((temp_dict['temp_min'] * (9 / 5) - 459.67), 2)
    Temps_F = namedtuple('Temps_F', ['current', 'max', 'min'])
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
                        action='store_true', help='Specifies that the forecast \
                        should be returned instead of current conditions.')
    parser.add_argument('-i', '--indent', dest='indent', type=int, default=2,
                        help='The indentation setting for output.')
    parser.add_argument('-d', '--datetime', dest='datetime',
                        action='store_true', help='For development purposes \
                        only.')
    args = parser.parse_args()
    if args.datetime:
        w = Weather(datetime(1970, 1, 1))
    else:
        w = Weather()
    w.get_weather_by_id(args.city, args.forecast, args.indent)


if __name__ == '__main__':
    main()
