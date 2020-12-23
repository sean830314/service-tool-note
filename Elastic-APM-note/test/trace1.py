
import time

import requests

import elasticapm


def main():
    sess = requests.Session()
    time.sleep(30)

if __name__ == "__main__":
    client = elasticapm.Client(service_name="service 1")
    elasticapm.instrument()
    client.begin_transaction("main")
    from elasticapm.traces import execution_context

    # get current transaction
    transaction = execution_context.get_transaction()
    trace_parent = transaction.trace_parent
    trace_parent_str = trace_parent.to_string()
    print(transaction)
    print(trace_parent_str)
    main()
    client.end_transaction("main")
