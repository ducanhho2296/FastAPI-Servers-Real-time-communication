import cv2
import uvicorn
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

# Mount the "static" directory as a static file directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the HTML page served by the root URL
@app.get("/")
async def read_root():
    with open("index.html") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)

# Define a WebSocket endpoint to stream video to the web browser
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        try:
            # Convert the frame to JPEG format
            _, jpeg = cv2.imencode(".jpg", frame)
            jpeg_bytes = jpeg.tobytes()
            # Send the frame to the web browser
            await websocket.send_bytes(jpeg_bytes)
        except WebSocketDisconnect:
            break
    capture.release()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
