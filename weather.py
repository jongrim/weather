#! /usr/bin/env python

import requests
import argparse
import json
from datetime import datetime, timedelta
import shelve
import os


class Weather:
    city_list = None
    api_key = ''
    api_limit = timedelta(minutes=10)
    last_call_time = None

    def __init__(self, last_call_time=None):
        with open('API_key.txt', 'r') as file:
            self.api_key = file.readline()

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

    def get_weather_data_using_id(self, id):
        params = {'id': id}
        base_url = 'api.openweathermap.org/data/2.5/weather'

        # check last call time to rate limit
        if self.check_if_within_limit:
            response = requests.get(base_url, params=params)
