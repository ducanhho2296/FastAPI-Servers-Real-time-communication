import cv2
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

@app.get('/')
async def index():
    return {"message": "Welcome to the webcam streaming application!"}


@app.get('/video_feed')
async def video_feed():
    global streaming
    streaming = True
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/stop_stream')
async def stop_stream():
    global streaming, camera
    streaming = False
    if camera:
        camera.release()
        camera = None
    return {"message": "Streaming stopped successfully."}

@app.get('/restart_stream')
async def restart_stream():
    global streaming
    streaming = True
    return {"message": "Streaming restarted successfully."}

@app.get('/save_frame')
async def save_frame(filename:str):
    cv2.imwrite(filename, img)


####demo using @app.post to receive request from client(web browser)
@app.post('/demo')
async def demo_getvalue(value:str):
    global demo_value 
    demo_value = value
    return demo_value

@app.get('/rundemo')
async def rundemo():
    return {"message": "the value was received as value = {}".format(demo_value)}

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
