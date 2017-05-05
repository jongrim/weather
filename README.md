# What's the weather?

What's the Weather (wtw) is an easy to use command line tool written in Python for getting current or forecast weather reports. It uses the openweathermap API to retrieve weather data.

Installation makes What's the Weather available from in your terminal using the command `wtw`. It requires an openweathermap API key, which you can obtain for free from [OpenWeatherMap](http://openweathermap.org/appid).

## Installation
It is recommended that What's the Weather be installed in your global site packages so that it can be available without having to activate a python virtual environment. However, if you would rather not install in the global site packages, you can absolutely install WTW in a virtual environment.

To install follow these steps:
1. Clone the project files into a directory of your choosing using `git clone https://github.com/jongrim/whats-the-weather.git`
2. Change into the new project directory, `whats-the-weather`
2. (B) If using a virtual environment, create the virtual environment now
3. Install using the supplied setup.py file by executing `$ pip3 install .`
- - This will install What's the Weather, as well as its dependency, requests. It also make What's the Weather available within bash using 'wtw'
4. Run WTW by typing `$ wtw <your city here>`. The first time you run it, you'll be prompted for your openweatherapi key.

## Sample usage
Using the tool is as easy as calling it from your command line and telling it which city you'd like the weather for:
`$ wtw Atlanta`

Help can be displayed with `$ wtw -h`.
