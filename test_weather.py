import unittest
from weather import Weather


class TestWeather(unittest.TestCase):

    def test_make_weather_object(self):
        w = Weather()
        self.assertTrue(isinstance(w, Weather))


if __name__ == '__main__':
    unittest.main()
