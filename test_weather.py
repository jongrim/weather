import unittest
import datetime
from weather import Weather, convert_temps, convert_timestamp
from unittest.mock import patch


class TestWeather(unittest.TestCase):

    def test_make_weather_object(self):
        w = Weather()
        self.assertTrue(isinstance(w, Weather))

    def test_weather_has_API(self):
        w = Weather()
        self.assertTrue(w.api_key)

    def test_weather_has_city_list(self):
        w = Weather()
        self.assertTrue(w.city_list)

    def test_weather_has_last_call_time_of_datetime(self):
        w = Weather()
        self.assertTrue(isinstance(w.last_call_time, datetime.datetime))

    def test_weather_has_api_rate_limit_of_timedetla(self):
        w = Weather()
        self.assertTrue(isinstance(w.api_limit, datetime.timedelta))

    def test_api_limit_when_greater_than_10min(self):
        '''
        A Weather object with last call time greater than 10 mins should return
        True
        '''
        w = Weather(datetime.datetime(1970, 1, 1))
        self.assertTrue(w.check_if_within_limit())

    def test_api_limit_when_less_than_10min(self):
        '''
        A Weather object with last call time less than 10 mins should return
        False
        '''
        w = Weather(datetime.datetime.now())
        self.assertFalse(w.check_if_within_limit())

    @patch('requests.get')
    def test_successful_request_to_api(self, mock_request):
        '''
        A Weather object whose last call time is greater than the rate limit
        should be able to make an api call
        '''
        w = Weather(datetime.datetime(1970, 1, 1))
        id = 1
        api_key = w.api_key
        w.request_weather_with_id(id)
        arg = f'http://api.openweathermap.org/data/2.5/weather?id=1&APPID={api_key}'
        assert mock_request.called_with(arg)
        self.assertTrue(w.WeatherData)

    @patch('requests.get')
    def test_unsuccessful_request_to_api(self, mock_request):
        '''
        A Weather object whose last call time should not be able to make an
        api request
        '''
        w = Weather(datetime.datetime.now())
        w.WeatherData = False
        id = 1
        api_key = w.api_key
        w.request_weather_with_id(id)
        arg = f'http://api.openweathermap.org/data/2.5/weather?id=1&APPID={api_key}'
        self.assertFalse(w.WeatherData)

    def test_unsuccessful_weather_request_with_id(self):
        w = Weather(datetime.datetime.now())
        with self.assertRaises(KeyError):
            w.get_weather_by_id('zzzzzz')

    # @patch('requests.get')
    # def test_successful_weather_request_with_id(self, mock_request):
    #     w = Weather(datetime.datetime(1970, 1, 1))
    #     result = w.request_weather_with_id('Atlanta')
    #     self.assertTrue(result)


class TestWeatherCityList(unittest.TestCase):

    def setUp(self):
        self.w = Weather()

    def test_get_id_by_city_name_where_name_is_included(self):
        city = self.w.get_city_id_by_name('Atlanta')
        self.assertEqual(city, 4180439)

    def test_get_id_by_city_name_where_name_isnot_included(self):
        city = self.w.get_city_id_by_name('ZZZZZ')
        self.assertEqual(city, None)


class TestWeatherConversions(unittest.TestCase):

    def test_convert_kelvin_to_fahrenheiht(self):
        temps = {'temp': 280.32, 'temp_min': 279.15, 'temp_max': 281.15}
        Temps_F = convert_temps(temps)
        self.assertEqual(Temps_F.current, 44.91)
        self.assertEqual(Temps_F.high, 46.4)
        self.assertEqual(Temps_F.low, 42.8)

    def test_convert_UTC_timestamp(self):
        time = convert_timestamp(1485762037)
        self.assertEqual(time, '2017-01-30 02:40:37')


if __name__ == '__main__':
    unittest.main()
