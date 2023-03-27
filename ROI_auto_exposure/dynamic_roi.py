from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

class AutoExposureRegion:
    def __init__(self, position=(0, 0), size=(100, 100), maxDims=(640, 480)):
        self.position = position
        self.size = size
        self.maxDims = maxDims

    def grow(self, x=0, y=0):
        self.size = (
            clamp(x + self.size[0], 1, self.maxDims[0]),
            clamp(y + self.size[1], 1, self.maxDims[1])
        )

    def move(self, x=0, y=0):
        self.position = (
            clamp(x + self.position[0], 0, self.maxDims[0] - self.size[0]),
            clamp(y + self.position[1], 0, self.maxDims[1] - self.size[1])
        )

    def endPosition(self):
        return (
            self.position[0] + self.size[0],
            self.position[1] + self.size[1]
        )

    def toRoi(self):
        roi = np.array([*self.position, *self.size])
        return roi
