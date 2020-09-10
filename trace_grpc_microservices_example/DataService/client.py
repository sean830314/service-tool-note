from __future__ import print_function

import grpc

from trace_grpc_microservices_example.DataService import service_pb2_grpc, service_pb2


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.DataServiceStub(channel)
    response = stub.GetCommentsData(service_pb2.GetCommentsDataRequest(apm_trace_parent_id='00-307c754fcda76e9adf106a4613032044-c27509b920ed7f32-01'))
    print("DataService client received: " + response.data)


if __name__ == '__main__':
    run()
