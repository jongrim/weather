from collections import namedtuple
from datetime import datetime


def convert_temps(temp_dict):
    current_temp_f = round((temp_dict['temp'] * (9 / 5) - 459.67), 2)
    max_temp_f = round((temp_dict['temp_max'] * (9 / 5) - 459.67), 2)
    min_temp_f = round((temp_dict['temp_min'] * (9 / 5) - 459.67), 2)
    Temps_F = namedtuple('Temps_F', ['current', 'max', 'min'])
    return Temps_F(current_temp_f, max_temp_f, min_temp_f)


def convert_timestamp(UTC_timestamp):
    time = datetime.fromtimestamp(UTC_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time
