from fastapi import FastAPI
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

region = AutoExposureRegion()

async def video_feed(websocket):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        roi = region.toRoi()
        cv2.rectangle(frame, roi.position, roi.endPosition(), (0, 255, 0), 2)

        # roi_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]
        jpeg_roi = cv2.imencode('.jpg', frame)[1].tobytes()
        await websocket.send_bytes(jpeg_roi)
        await asyncio.sleep(0)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await video_feed(websocket)

@app.post("/move_roi")
async def move_roi(delta_x: int, delta_y: int):
    region.move(delta_x, delta_y)
    return {"message": "ROI moved successfully"}

@app.post("/grow_roi")
async def grow_roi(delta_w: int, delta_h: int):
    region.grow(delta_w, delta_h)
    return {"message": "ROI grown successfully"}

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)