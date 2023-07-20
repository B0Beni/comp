import datetime
import requests
from flask import Flask, request, redirect, abort, jsonify
from flask import render_template, make_response, session
from flask_login import LoginManager, login_user, login_required
from flask_login import logout_user, current_user
from flask_restful import Api


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'too short key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/news.sqlite'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)  # год


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/')
@app.route('/index')
def it_doctor():
    return 'IT Doctor!'


@app.route('/weather_form', methods=['GET', 'POST'])
def weather_form():
    if request.method == 'GET':
        return render_template('weather_form.html',
                               title='Выбор города')
    elif request.method == 'POST':
        town = request.form.get('town')
        if not town.strip():
            town = 'Москва'
        data = {}
        key = 'c747bf84924be997ff13ac5034fa3f86'
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': key, 'q': town, 'units': 'metric'}
        result = requests.get(url, params=params)
        weather = result.json()
        code = weather['cod']
        icon = weather['weather'][0]['icon']
        temperature = weather['main']['temp']
        data['code'] = code
        data['icon'] = icon
        data['temp'] = temperature
        return render_template('weather.html',
                               title=f'Погода в городе {town}',
                               town=town, data=data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)