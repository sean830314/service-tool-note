import time

import requests
from flask import Flask

import elasticapm
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
apm = ElasticAPM(app, service_name="ServiceA")

@app.route("/")
def svc2a():
    with elasticapm.capture_span("Extract Items Comments", span_type="db.mysql.query", labels={"type": "read_data"}):
        time.sleep(1)
    with elasticapm.capture_span("Transform data into RDD", span_type="spark.rdd", labels={"type": "transform_data"}):
        time.sleep(5)
    return "ServiceA"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
