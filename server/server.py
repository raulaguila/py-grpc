import os
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger

from .camgrpc import camera_pb2, camera_pb2_grpc, CameraService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    camera_pb2_grpc.add_CameraServicer_to_server(CameraService(), server)
    reflection.enable_server_reflection((
        camera_pb2.DESCRIPTOR.services_by_name['Camera'].full_name,
        reflection.SERVICE_NAME,
    ),
        server,
    )

    server.add_insecure_port(f'[::]:50051')
    server.start()
    logger.info(f'Listening on port 50051')
    server.wait_for_termination()
