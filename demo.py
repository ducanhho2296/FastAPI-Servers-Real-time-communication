import uvicorn
import numpy as np
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
import sys

app = FastAPI()
camera = cv2.VideoCapture(0)
streaming = False


def generate_frames():
    while streaming:
        success, frame = camera.read()
        global img
        img = frame.copy()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # yield img

