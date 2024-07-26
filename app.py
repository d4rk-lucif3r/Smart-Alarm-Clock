"""
This api  is a smart alarm clock intended to be run 24/7. It enables
the user to schedule alarms. The user is notified when
an alarm is up via text to speech and a notification
which is displayed in the notifications column. 
If the user has selected news and weather checkbox at the
time of setting an alarm then Each time alarm goes off
Latest news and weather update is played using text to speech
Covid news is played every time alarm goes off
"""
from flask import Flask, redirect, render_template, request
import json
import tempfile

from alarms import add_alarm, alarmTobeDeleted, clearAlarms, get_alarms
from covid_notifications import clear_covid_news, get_covid_data
from logger import clearLogs, info_log
from news import clearNews, get_news
from notifications import (clearAllNotification, notification_clear,
                           update_notifications)
from weather import clearAllWeather, get_weather

app = Flask(__name__)

tmpdir = tempfile.gettempdir()
ideas_filename = pathlib.Path(tmpdir + '/ideas.json')

@app.route('/')
def home():
    """
    This function is responsible for fetching a list of alarms, current
    weather, latest news and latest covid data. This data is
    fetched to be displayed on the main page.
    Whenever the html page refreshes news , weather and covid information
    is also fetched.
    """
    favicon = 'static/images/logo.ico'
    get_news(False)
    get_weather(False)
    get_covid_data(False)
    title = "Smart Alarm Clock"
    alarm_list = get_alarms()
    notification_list = update_notifications()
    return render_template('home.html', alarm_list=alarm_list, notification_list=notification_list, favicon=favicon, title=title)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """
    This function is responsible for getting the details for an alarm
    stores alarm time , news and weather checkbox values in "title,isNews and is Weather"
    respectively and formats that into a dictionary and passes that into add_alarm function 
    alarms.py
    """
    title = request.args.get('alarm')
    if title:
        title = title.replace('T', '-')
        title = title + ":00"

    label = request.args.get('two')
    isNews = request.args.get('news')
    isWeather = request.args.get('weather')

    isNews = "News Enabled" if isNews == "news" else "News Not enabled"
    isWeather = "Weather Enabled" if isWeather == "weather" else "Weather Not enabled"

    if title:
        alarm = {'title': title,
                 'label': label,
                 'news': isNews,
                 'weather': isWeather}
        add_alarm(alarm)
        return redirect('/')


@app.route('/delete_alarm', methods=['GET', 'POST'])
def delete_alarm():
    """
    Refer to delete alarm docstring in alarms.py
    """
    alarmTobeDeleted()
    return redirect('/')


@app.route('/notification-clear', methods=['GET', 'POST'])
def notification_clear_function():
    """Refer to clear notification docstring in notifications.py"""
    notification_clear()
    return redirect('/')


@app.route('/clear', methods=['GET', 'POST'])
def clearAll():
    """
    This function calls all clearing functions from all modules
    """
    clearAllNotification()
    clearAllWeather()
    clearNews()
    clearAlarms()
    clear_covid_news()
    clearLogs()
    info_log("Cleared all .json files")
    return redirect('/')


@app.route('/merge_ideas', methods=['POST'])
def merge_ideas():
    """
    This function combines similar ideas from the ideas.json file,
    merging duplicates into a single entry and storing the merged
    result back into the file.
    """
    if ideas_filename.is_file():
        with open(tmpdir + '/ideas.json', 'r') as ideas_file:
            try:
                ideas_list = json.load(ideas_file)
            except (json.JSONDecodeError, Exception):
                ideas_list = []
        
        # Logic to merge duplicate ideas
        merged_ideas = {}
        for idea in ideas_list:
            if idea['title'] in merged_ideas:
                merged_ideas[idea['title']]['count'] += 1
            else:
                merged_ideas[idea['title']] = {'details': idea['details'], 'count': 1}
        
        # Creating the final merged list
        new_ideas_list = [{'title': title, 'details': details['details'], 'count': details['count']} for title, details in merged_ideas.items()]
        
        with open(tmpdir + '/ideas.json', 'w') as ideas_file:
            json.dump(new_ideas_list, ideas_file, indent=2)

        info_log("Merged ideas and updated ideas.json")
    return redirect('/')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)