#! /usr/bin/env python

import requests
import argparse
import json


class Weather:
    city_list = None
    api_key = ''

    def __init__(self):
        # build a dictionary of all the cities
        # read the api key
        with open('API_key.txt', 'r') as file:
            self.api_key = file.readline()

        with open('city.list.json', 'r') as file:
            self.city_list = json.load(file)

    def get_city_id_by_name(self, name):
        for city in self.city_list:
            if city["name"] == name:
                return city["id"]
        return None
