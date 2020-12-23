import time

import requests
from flask import Flask

import elasticapm
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
apm = ElasticAPM(app, service_name="ServiceB")

@app.route("/")
def svc2a():
    with elasticapm.capture_span("Update sales ranking to Redis", span_type="db.mysql.query", labels={"type": "write_data"}):
        time.sleep(1)
    return "ServiceB"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
