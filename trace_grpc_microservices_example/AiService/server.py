from concurrent import futures
import time

import grpc

from trace_grpc_microservices_example.AiService import service_pb2_grpc, service_pb2
import elasticapm
from elasticapm.contrib.flask import ElasticAPM
import time
client = elasticapm.Client(service_name="AiServicer")
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

@elasticapm.capture_span("preprocess data",span_type="python.numpy", labels={"type": "preprocess_data"})
def preprocess_data():
    time.sleep(2)
    client.capture_message(message="AiServicer preprocess ok")

@elasticapm.capture_span("read model",span_type="python.tensorflow", labels={"type": "read_model"})
def read_model():
    time.sleep(3)
    client.capture_message(message="AiServicer read model ok")

@elasticapm.capture_span("predict",span_type="python.transformers", labels={"type": "predict"})
def predict():
    time.sleep(10)
    client.capture_message(message="AiServicer predict data ok")

class AiServicer(service_pb2_grpc.AiServiceServicer):
    def PredictComment(self, request, context):
        try:
            parent = elasticapm.trace_parent_from_string(request.apm_trace_parent_id)
            client.begin_transaction("predict movice comments", trace_parent=parent)
            preprocess_data()
            read_model()
            predict()
            client.end_transaction("finish predict movice comments")
            return service_pb2.PredictCommentReply(data='Predict: {}'.format(request.data))
        except Exception as e:
            client.capture_exception()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_AiServiceServicer_to_server(AiServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
