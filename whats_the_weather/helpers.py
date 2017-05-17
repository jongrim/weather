from collections import namedtuple
from datetime import datetime


def convert_temps(temp_dict):
    current_temp_f = convert_kelvin_to_f(temp_dict['temp'])
    max_temp_f = convert_kelvin_to_f(temp_dict['temp_max'])
    min_temp_f = convert_kelvin_to_f(temp_dict['temp_min'])
    Temps_F = namedtuple('Temps_F', ['current', 'max', 'min'])
    return Temps_F(current_temp_f, max_temp_f, min_temp_f)


def convert_kelvin_to_f(temp):
    return round(((temp * (9/5)) - 459.67), 2)


def convert_timestamp_to_string(UTC_timestamp):
    time = datetime.fromtimestamp(UTC_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time


def convert_timestamp_to_datetime(UTC_timestamp):
    return datetime.fromtimestamp(UTC_timestamp)
