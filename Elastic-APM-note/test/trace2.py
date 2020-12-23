import time
import elasticapm
from elasticapm.contrib.flask import ElasticAPM

def test():
    with elasticapm.capture_span("span1"):
         time.sleep(8)
if __name__ == "__main__":
    client = elasticapm.Client(service_name="service 888")
    parent = elasticapm.trace_parent_from_string('00-307c754fcda76e9adf106a4613032044-c27509b920ed7f32-01')
    client.begin_transaction("test_trace", trace_parent=parent)
    test()
    client.end_transaction("test_trace")
