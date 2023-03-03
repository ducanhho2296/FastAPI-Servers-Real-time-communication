from fastapi import FastAPI
import uvicorn
import cv2

app = FastAPI()
cap = cv2.VideoCapture(0)

@app.post("/start")
async def start_inference():
    print('Start model inference')
 
    pass


@app.post("/stop")
async def stop_inference():
    print('Stop model inference')



def generate():
    while True: # TODO: add logic to stop camera here
        ret, image = cap.read()
        if image is not None:
            retval, image_encoded = cv2.imencode(".jpg", image)

            if image_encoded is not None:
                frame = image_encoded.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.get("/preview")
async def get_images():
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

app.mount("/", StaticFiles(directory="static"), name="static")

@app.get("/stop-streaming.js")
async def read_item():
    return FileResponse("static/stop-streaming.js")

app.mount("/", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_item():
    return """
    <html>
        <body>
            <video autoplay></video>
            <button id="stopButton">Stop Streaming</button>
            <script src="/docs/swagger-ui/stop-streaming.js"></script>
            <script>
                const stopButton = document.getElementById('stopButton');
                
                stopButton.addEventListener('click', () => {
                  stopStreaming();
                });
                
                const constraints = {
                    audio: false,
                    video: true
                };
                
                navigator.mediaDevices.getUserMedia(constraints)
                    .then((stream) => {
                        const video = document.querySelector('video');
                        video.srcObject = stream;
                        video.onloadedmetadata = (e) => {
                            video.play();
                        };
                    })
                    .catch((err) => {
                        console.log(err.name + ": " + err.message);
                    });
            </script>
        </body>
    </html>
    """





from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
if __name__ == "__main__":
    text = "OpenAPI Swagger link"
    target = "http://127.0.0.1:8000/preview"  ## CLICK HERE
    print(f"\u001b{text}\u001b\\{target}\u001b\u001b")
    uvicorn.run(app, host="0.0.0.0", port=8000)

    origins = ["*",
                "http://localhost",
                "http://localhost:8000",
                ]

    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
