from __future__ import print_function

import grpc

from trace_grpc_microservices_example.AiService import service_pb2_grpc, service_pb2


def run():
    channel = grpc.insecure_channel('localhost:50052')
    stub = service_pb2_grpc.AiServiceStub(channel)
    response = stub.PredictComment(service_pb2.PredictCommentRequest(apm_trace_parent_id='00-307c754fcda76e9adf106a4613032044-c27509b920ed7f32-01', data="the movie is bad"))
    print("AiService client received: " + response.data)


if __name__ == '__main__':
    run()
