import cv2
import asyncio
import numpy as np
from fastapi import FastAPI, WebSocket
from starlette.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return HTMLResponse('''
        <html>
            <head>
                <title>Video Streaming Test</title>
            </head>
            <body>
                <h1>Video Streaming Test</h1>
                <img src="#" id="video-feed" width="640" height="480" />
                <script>
                    var ws = new WebSocket('ws://' + window.location.host + '/ws');
                    ws.binaryType = 'arraybuffer';
                    ws.onmessage = function(event) {
                        var img = document.getElementById('video-feed');
                        var arrayBuffer = event.data;
                        var byteArray = new Uint8Array(arrayBuffer);
                        var blob = new Blob([byteArray], { type: 'image/jpeg' });
                        var urlCreator = window.URL || window.webkitURL;
                        var imageUrl = urlCreator.createObjectURL(blob);
                        img.src = imageUrl;
                    };
                </script>
            </body>
        </html>
    ''')

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
            _, jpeg = cv2.imencode('.jpg', frame)

            # Send frame over WebSocket
            await websocket.send_bytes(jpeg.tobytes())
    finally:
        cap.release()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await video_feed(websocket)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
