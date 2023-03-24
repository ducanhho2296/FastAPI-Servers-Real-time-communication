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
