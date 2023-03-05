import cv2
import asyncio
import numpy as np
from fastapi import FastAPI, WebSocket
from starlette.responses import StreamingResponse

app = FastAPI()

async def video_feed(websocket: WebSocket):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not start camera.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame to reduce network bandwidth usage
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _, jpeg = cv2.imencode('.jpg', frame)

            # Send frame over WebSocket
            await websocket.send_bytes(jpeg.tobytes())
    finally:
        cap.release()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await video_feed(websocket)

@app.get("/")
async def read_root():
    return StreamingResponse(video_feed_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

def video_feed_generator():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not start camera.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame to reduce network bandwidth usage
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _, jpeg = cv2.imencode('.jpg', frame)

            # Yield frame to browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    finally:
        cap.release()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
