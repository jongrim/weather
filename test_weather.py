import unittest
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
