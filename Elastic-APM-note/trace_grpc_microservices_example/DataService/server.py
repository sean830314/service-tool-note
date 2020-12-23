from concurrent import futures
import time

import grpc

from trace_grpc_microservices_example.DataService import db_service_pb2_grpc, db_service_pb2
import elasticapm
from elasticapm.contrib.flask import ElasticAPM
import time
client = elasticapm.Client(service_name="DataServicer")

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

@elasticapm.capture_span("query data",span_type="db.mysql.query", labels={"type": "query_data"})
def query_comments():
    time.sleep(2)
    client.capture_message(message="DataServicer query comments ok")

@elasticapm.capture_span("process data",span_type="python.pandas", labels={"type": "process_data"})
def process_comments():
    time.sleep(5)
    client.capture_message(message="DataServicer process comments ok")

class DataServicer(db_service_pb2_grpc.DataServiceServicer):
    def GetCommentsData(self, request, context):
        try:
            #parent = elasticapm.trace_parent_from_string(request.apm_trace_parent_id)
            parent = elasticapm.trace_parent_from_string(dict(context.invocation_metadata())['apm_trace_parent_id'])
            client.begin_transaction("get movice comments", trace_parent=parent)
            query_comments()
            process_comments()
            client.end_transaction("finish get movice comments")
            return db_service_pb2.GetCommentsDataReply(data='the movie is bad')
        except Exception as e:
            client.capture_exception()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_service_pb2_grpc.add_DataServiceServicer_to_server(DataServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
