import time

import requests

import elasticapm


@elasticapm.capture_span("Predict sales ranking by Spark MLib", span_type="Spark.MLib", labels={"type": "read_data"})
def predict_itmes_comments():
    time.sleep(15)

def main():
    result = requests.get("http://localhost:8080")
    predict_itmes_comments()
    result = requests.get("http://localhost:8081")


if __name__ == "__main__":
    client = elasticapm.Client(service_name="service App")
    elasticapm.instrument()
    client.begin_transaction("main")
    main()
    client.end_transaction("main")
