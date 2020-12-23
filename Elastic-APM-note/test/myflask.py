from flask import Flask, render_template
import time
from elasticapm.contrib.flask import ElasticAPM
import elasticapm
app = Flask(__name__)
app.config['ELASTIC_APM'] = {
          'SERVICE_NAME': 'FlaskApp',
          'SECRET_TOKEN': '',
          'SERVER_URL': 'http://localhost:8200'
}
apm = ElasticAPM(app)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/divbyzero')
def divbyzero():
    num = 2 / 0
    return "hello world - " + str(num)

@app.route('/')
def index():
    return "Hello World!"

@elasticapm.capture_span("read_data",span_type="read_db", span_action="read", labels={"type": "read_data"})
def read_user_data(uid):
    try:
        time.sleep(5)
        apm.capture_message(message="read data success")
    except Exception as e:
        apm.capture_exception()

@elasticapm.capture_span("process_data",span_type="process_data", labels={"type": "process_data"})
def process_data(data):
    try:
        time.sleep(10)
        apm.capture_message(message="process data success")
    except Exception as e:
        apm.capture_exception()

@elasticapm.capture_span("write_data",span_type="write_db", span_action="write", labels={"type": "write_data"})
def write_user_info(uid,data):
    try:
        time.sleep(1)
        apm.capture_message(message="write data success")
    except Exception as e:
        apm.capture_exception()

@app.route('/update')
def update_user_info():
    user_info = read_user_data(uid=None)
    data = process_data(data=None)
    write_user_info(uid=None, data=None)
    return "Hello World!"

if __name__ == '__main__':
 app.run(host='127.0.0.1', port=5000)
