"""
This module is responsible for fetching news data from
newsapi using api key provided in environment variables
"""

import json
import os
import time
import tempfile
import requests
from logger import error_log, info_log, warning_log
from notifications import new_notification
from text_to_speech import tts

tmp_dir = tempfile.gettempdir()

def get_api_key() -> dict:
    """Fetches the newsapi api key from the environment variables."""
    return os.getenv('NEWSAPI_API_KEY')

def get_news(tts_enabled: bool) -> None:
    """
    This function fetches the news data from newsapi using
    api key provided in environment variables and stores the data in 
    "news.json" 
    New Notification and info log is created each time new data is fetched
    """
    api_key = get_api_key()
    country = 'in'
    url = 'https://newsapi.org/v2/top-headlines?country={}&apiKey={}'.format(country, api_key)
    new_news = requests.get(url).json()
    
    with open(tmp_dir + '/news.json', 'w') as news_file:
        json.dump(new_news, news_file, indent=2)

    for i in range(3):
        news_notification = {
            'timestamp': time.strftime('%H:%M:%S'),
            'type': 'News',
            'title': new_news['articles'][i]['title'],
            'description': ''
        }
        news_log = {
            'timestamp': time.strftime('%H:%M:%S'),
            'type': 'news',
            'description': 'New news articles ' + new_news['articles'][i]['title'],
            'error': ''
        }
        new_notification(news_notification)
        info_log(news_log)
        
        if tts_enabled:
            try:
                tts('New news story: ' + new_news['articles'][i]['title'])
            except RuntimeError:
                error_log(RuntimeError)

    with open(tmp_dir + '/news.json', 'w') as news_file:
        json.dump(new_news, news_file, indent=2)

def clearNews():
    """
    This function is responsible for clearing data in
    "news.json" each time reset button on UI 
    is pressed
    """
    clearAllNews = []
    with open(tmp_dir + '/news.json', 'w') as news_file:
        json.dump(clearAllNews, news_file, indent=2)