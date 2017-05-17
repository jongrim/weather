import argparse
import pprint
from datetime import datetime

from whats_the_weather.helpers import (convert_kelvin_to_f, convert_temps,
                                       convert_timestamp_to_datetime,
                                       convert_timestamp_to_string)
from whats_the_weather.weather import Weather


def get_weather(city_name, forecast=None, indent=2, show_json=False, dt=None):
    '''Makes a Weather object'''
    w = Weather(dt)

    cur_city = w.get_the_weather(city_name, forecast)

    visual_space = ' ' * indent
    if forecast:
        display_forecast_weather(cur_city, visual_space, show_json)
    else:
        display_current_weather(cur_city, visual_space, show_json)


def display_forecast_weather(data_dict, space, show_json):
    # Get data out of forecast dict
    weather_dict = data_dict['forecast'].get('json', None)
    if not weather_dict:
        print('No cached forecast weather information \
        for this location')
        return
    if show_json:
        pprint.pprint(weather_dict)
        return

    frcst_wthr = process_forecast_data(weather_dict)
    # pprint.pprint(frcst_wthr)
    max_temp = 'max_temp'
    min_temp = 'min_temp'
    wthr_conds = 'wthr_conds'
    for (day, conds) in frcst_wthr.items():
        print(f"Weather for {conds['month']}-{day}:")
        print(f'{space}', f'High: {conds[max_temp]}')
        print(f'{space}', f'Low: {conds[min_temp]}')
        print(f'{space}', 'Weather conditions: ', ', '.join(conds[wthr_conds]))


def process_forecast_data(forecast_dict):
    '''Loop through the forecast data and build up a summary'''
    data_list = forecast_dict['list']
    daily_weather = {}

    # Dict keys
    max_temp = 'max_temp'
    min_temp = 'min_temp'
    wthr_conds = 'wthr_conds'
    for measure in data_list:
        date = convert_timestamp_to_datetime(measure['dt'])
        day = date.day
        daily_weather.setdefault(day, {})
        day_d = daily_weather[day]

        day_d.setdefault('month', date.month)

        # Search for maximum temp of the day
        cur_max = convert_kelvin_to_f(measure['main']['temp_max'])
        day_d[max_temp] = max(day_d.get(max_temp, 0), cur_max)

        # Search for minimum temp of the day
        cur_min = convert_kelvin_to_f(measure['main']['temp_min'])
        day_d[min_temp] = min(day_d.get(min_temp, 150), cur_min)

        # Set and add weather conditions
        day_d.setdefault(wthr_conds, [])
        cur_cond = measure['weather'][0]['description']
        if cur_cond not in day_d[wthr_conds]:
            day_d[wthr_conds].append(cur_cond)

    return daily_weather


def display_current_weather(data_dict, space, show_json):
    # Get data out of current dict
    weather_dict = data_dict['current'].get('json', None)
    if not weather_dict:
        print('No cached current weather information \
        for this location')
        return
    if show_json:
        pprint.pprint(weather_dict)
        return
    result_city = weather_dict['name']
    weather_set = weather_dict['weather']
    Temps_F = convert_temps(weather_dict['main'])
    sunrise = convert_timestamp_to_string(weather_dict['sys']['sunrise'])
    sunset = convert_timestamp_to_string(weather_dict['sys']['sunset'])
    rain = weather_dict.get('rain', None)
    clouds = weather_dict.get('clouds', None)
    wind = weather_dict.get('wind', None)
    snow = weather_dict.get('snow', None)

    print(f'Current weather for {result_city}:')
    # print(f'{space}Weather description: ', end='')
    for x in weather_set:
        print(f"{space}{x['description'].capitalize()}")
    # print('')
    print(f'{space}Temperatures:')
    print(f'{space}{space}Current: ', f'{Temps_F.current}'.rjust(5))
    print(f'{space}{space}Max: ', f'{Temps_F.max}'.rjust(9))
    print(f'{space}{space}Min: ', f'{Temps_F.min}'.rjust(9))
    print(f"{space}Humidity: {weather_dict['main']['humidity']}%")
    print(f'{space}Sunrise: {sunrise}')
    print(f'{space}Sunset: {sunset}')
    if rain:
        if rain.get('3h'):
            print(f"{space}Rain volume for last 3 hours: {rain['3h']}")
    if clouds:
        if clouds.get('all'):
            print(f"{space}Cloudiness: {clouds['all']}%")
    if wind:
        if wind.get('speed'):
            print(f"{space}Wind speed: {wind['speed']} meters/ssec")
        if wind.get('deg'):
            print(f"{space}Wind direction: {wind['deg']} degrees")
        if wind.get('gust'):
            print(f'{space}', end='')
            print("Wind gust: {wind.get('gust')} meters/sec")
    if snow:
        if snow.get('3h'):
            print(f"{space}Snow volume for last 3 hours: {snow['3h']}")


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
    parser.add_argument('-j', '--json', dest='json',
                        action='store_true', help='Show me the JSON! (Pretty \
                        printed of course)')
    # TODO add option to colorize output
    # TODO add option for ascii art
    args = parser.parse_args()
    if args.datetime:
        dt = datetime(1970, 1, 1)
    else:
        dt = None
    get_weather(args.city, args.forecast, args.indent, args.json, dt)


if __name__ == '__main__':
    main()
