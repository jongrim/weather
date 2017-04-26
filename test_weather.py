import unittest
import datetime
from weather import Weather


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
        w = Weather(datetime.datetime(1970, 1, 1))
        self.assertTrue(w.check_if_within_limit())

    def test_api_limit_when_less_than_10min(self):
        w = Weather(datetime.datetime.now())
        self.assertFalse(w.check_if_within_limit())


class TestWeatherCityList(unittest.TestCase):

    def setUp(self):
        self.w = Weather()

    def test_get_id_by_city_name_where_name_is_included(self):
        city = self.w.get_city_id_by_name('Atlanta')
        self.assertEqual(city, 4180439)

    def test_get_id_by_city_name_where_name_isnot_included(self):
        city = self.w.get_city_id_by_name('ZZZZZ')
        self.assertEqual(city, None)


if __name__ == '__main__':
    unittest.main()
