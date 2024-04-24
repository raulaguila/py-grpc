import base64
import math
import time
from typing import Optional, List

import cv2

from . import camera_pb2
from . import camera_pb2_grpc


class CameraService(camera_pb2_grpc.CameraServicer):
    __video_capture: Optional[cv2.VideoCapture] = None
    __params: List[int] = [cv2.IMWRITE_JPEG_QUALITY, 100, cv2.IMWRITE_JPEG_OPTIMIZE, 1]
    __clients: int = 0

    def Stream(self, request, context):
        self.__clients = self.__clients + 1
        if self.__video_capture is None or not self.__video_capture.isOpened():
            self.__video_capture = cv2.VideoCapture(0)
            # self.__video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            # self.__video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            # self.__video_capture.set(cv2.CAP_PROP_FPS, 60)
            # self.__video_capture.set(cv2.CAP_PROP_FRAME_COUNT, 3)
            # self.__video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.5)
            # self.__video_capture.set(cv2.CAP_PROP_EXPOSURE, 0.5)

        try:
            while context.is_active():
                start = time.time()
                ret, frame = self.__video_capture.read()

                if frame is not None:
                    cv2.putText(
                        frame,
                        f"fps: {math.ceil(1 / (time.time() - start))}",
                        (7, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                        cv2.LINE_8,
                    )

                    _, buffer = cv2.imencode('.jpg', frame, self.__params)
                    yield camera_pb2.CameraResponse(base64image=base64.b64encode(buffer).decode('utf-8'))
        finally:
            self.__clients = self.__clients - 1
            if self.__clients == 0:
                self.__video_capture.release()
