"""
This module is responsible for fetching weather data from
Openweathermap using api key provided in environment variables.
"""

import json
import os
import time
import tempfile
import requests
from logger import error_log, info_log
from notifications import new_notification
from text_to_speech import tts

tmpdir = tempfile.gettempdir()

def get_api_key() -> str:
    """
    This function fetches the OpenWeatherMap API key
    from environment variables.
    """
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        raise ValueError("API key for OpenWeatherMap not found in environment variables.")
    return api_key

def get_weather(tts_enabled: bool) -> None:
    """
    This function fetches the weather data from OpenWeatherMap using
    the API key provided in environment variables and stores the data in
    "weather.json".
    A new Notification and info log is created each time new data is fetched.
    """
    # location
    location = 'New Delhi'
    api_key = get_api_key()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(location, api_key)
    new_weather = requests.get(url).json()
    
    with open(tmpdir+'/weather.json', 'w') as weather_file:
        json.dump(new_weather, weather_file, indent=2)
        
    weather_notification = ({
        'timestamp': time.strftime('%H:%M:%S'),
        'type': 'Weather',
        'title': 'Current temperature in ' + new_weather['name'] + ' is ' + str(new_weather['main']['temp']) +
                 "\n Minimum Temperature is " + str(new_weather['main']['temp_min']) +
                 "\n and Maximum Temperature is " + str(new_weather['main']['temp_max']),
        'description': ''
    })
    
    weather_log = ({
        'timestamp': time.strftime('%H:%M:%S'),
        'type': 'weather',
        'description': 'Current Weather in ' + new_weather['name'] + ' has been updated.',
        'error': ''
    })
    
    new_notification(weather_notification)
    info_log(weather_log)
    
    if tts_enabled:
        try:
            tts('Current temperature in ' + new_weather['name'] +
                ' is ' + str(new_weather['main']['temp']) +
                " Minimum Temperature is " + str(new_weather['main']['temp_min']) +
                " and Maximum Temperature is " + str(new_weather['main']['temp_max']))
        except RuntimeError:
            error_log(RuntimeError)

def clearAllWeather():
    """
    This function is responsible for clearing data in
    "weather.json" each time the reset button on UI
    is pressed.
    """
    clearWeather = []
    with open(tmpdir+'/weather.json', 'w') as weather_file:
        json.dump(clearWeather, weather_file, indent=2)