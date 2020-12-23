import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# or configure to use ELASTIC_APM in your application's settings
from elasticapm.contrib.flask import ElasticAPM
app = Flask(__name__)
app.config['ELASTIC_APM'] = {
  # Set required service name. Allowed characters:
  # a-z, A-Z, 0-9, -, _, and space
  'SERVICE_NAME': 'python-flask',

  # Use if APM Server requires a token
  'SECRET_TOKEN': '',

  # Set custom APM Server URL (default: http://localhost:8200)
  'SERVER_URL': 'http://localhost:8200',
}

apm = ElasticAPM(app)

#app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/beijing', methods=['GET'])
def getBeijing():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    city = "beijing"
    weather_data = []
    r = requests.get(url.format(city)).json()

    weather = {
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
    }

    weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    print([city.name for city in cities])
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()

        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
    #app.run(host='0.0.0.0', port=5002)

