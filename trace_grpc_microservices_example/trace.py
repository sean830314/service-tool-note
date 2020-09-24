from __future__ import print_function

import grpc

from trace_grpc_microservices_example.DataService import db_service_pb2_grpc as data_pb2_grpc
from trace_grpc_microservices_example.DataService import db_service_pb2 as data_pb2
from trace_grpc_microservices_example.AiService import ai_service_pb2_grpc as ai_pb2_grpc
from trace_grpc_microservices_example.AiService import ai_service_pb2 as ai_pb2
import elasticapm
from elasticapm.traces import execution_context
import google.protobuf.empty_pb2
client = elasticapm.Client(service_name="movie_comment_predict")
elasticapm.instrument()

def get_data(trace_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = data_pb2_grpc.DataServiceStub(channel)
    metadata = [('apm_trace_parent_id', trace_id)]
    response = stub.GetCommentsData(google.protobuf.empty_pb2.Empty() ,metadata=metadata)
    print("DataService client received: " + response.data)
    return response.data

def predict_data(trace_id, data):
    channel = grpc.insecure_channel('localhost:50052')
    stub = ai_pb2_grpc.AiServiceStub(channel)
    metadata = [('apm_trace_parent_id', trace_id)]
    response = stub.PredictComment(ai_pb2.PredictCommentRequest(data=data) ,metadata=metadata)
    print("AiService client received: " + response.data)
    return response.data
def run():
    print("start")
    try:
        client.begin_transaction("main")
        transaction = execution_context.get_transaction()
        trace_parent = transaction.trace_parent
        trace_parent_str = trace_parent.to_string()
        data = get_data(trace_parent_str)
        data = predict_data(trace_parent_str, data)
        client.end_transaction("main")
    except Exception as e:
        print("Exception")
        client.capture_exception()
    print("Done")
if __name__ == '__main__':
    run()
