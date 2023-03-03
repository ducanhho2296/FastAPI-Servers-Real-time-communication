from fastapi import FastAPI, WebSocket
import cv2
import base64

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        jpeg_bytes = base64.b64encode(buffer)
        await websocket.send_bytes(jpeg_bytes)
