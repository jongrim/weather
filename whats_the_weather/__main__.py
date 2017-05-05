from datetime import datetime
import argparse
import pprint
from whats_the_weather.helpers import convert_temps, convert_timestamp
from whats_the_weather.weather import Weather


def display_weather(city_name, forecast=None, indent=2, show_json=False,
                    dt=None):
    '''Makes a Weather object'''
    w = Weather(dt)

    city_id = w.get_weather_by_id(city_name, forecast)
    cur_city = w.wthr_data_dict[city_id]

    if forecast:
        # Get data out of forecast dict
        weather_dict = cur_city['forecast'].get('json', None)
        if not weather_dict:
            print('No cached forecast weather information \
            for this location')
            return
        if show_json:
            pprint.pprint(weather_dict)
            return
    else:
        # Get data out of current dict
        weather_dict = cur_city['current'].get('json', None)
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
                        printed of course')
    # TODO add option to colorize output
    # TODO add option for ascii art
    args = parser.parse_args()
    if args.datetime:
        dt = datetime(1970, 1, 1)
    else:
        dt = None
    display_weather(args.city, args.forecast, args.indent, args.json, dt)


if __name__ == '__main__':
    main()
