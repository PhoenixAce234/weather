from flask import Flask, render_template, request
import requests
import configparser
from datetime import datetime

app = Flask(__name__)
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    tempf = "{0:.2f}".format(data["main"]["temp"])
    tempc = (float(tempf)-32)*5/9
    tempc = "{0:.2f}".format(tempc)
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data["weather"][0]["icon"]
    iconurl = "http://openweathermap.org/img/w/" + icon + ".png"
    now = datetime.now()
    print(now)
    return render_template('results.html', location=location, tempf=tempf, tempc=tempc, feels_like=feels_like, weather=weather, iconurl=iconurl, now=now)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


print(get_weather_results("10001", get_api_key()))


if __name__ == '__main__':
    app.run()


