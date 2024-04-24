import asyncio
import base64

import cv2
import grpc
import numpy as np
from loguru import logger
from server import camera_pb2, camera_pb2_grpc

OPTIONS = [
    ('grpc.max_message_length', 1024 * 1024 * 1024),
    ('grpc.max_send_message_length', 1024 * 1024 * 1024),
    ('grpc.max_receive_message_length', 1024 * 1024 * 1024),
]


async def run():
    try:
        async with grpc.aio.insecure_channel("localhost:50051") as channel:
            stub = camera_pb2_grpc.CameraStub(channel)
            responses = stub.Stream(camera_pb2.Blank())

            app_exit = False
            while True:
                async for response in responses:
                    im_bytes = base64.b64decode(response.base64image)
                    im_array = np.frombuffer(im_bytes, dtype=np.uint8)
                    im_frame = cv2.imdecode(im_array, flags=cv2.IMREAD_COLOR)

                    if im_frame is not None:
                        cv2.imshow('web cam', im_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()
                            app_exit = True
                            break

                if app_exit:
                    break

    except Exception as e:
        logger.error(f"Exception occurred: {e}")


if __name__ == '__main__':
    asyncio.run(run())
