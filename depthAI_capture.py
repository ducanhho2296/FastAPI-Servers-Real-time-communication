import cv2  
import depthai  
import uvicorn
import numpy as np
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse

global streaming
streaming = False
pipeline = depthai.Pipeline()

cam_rgb = pipeline.create(depthai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 640)
cam_rgb.setInterleaved(False)

#create output
xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)


# #initialize DepthAI
# with depthai.Device(pipeline) as device:
#     q_rgb = device.getOutputQueue("rgb")
#     frame = None   
#     while True:
#         in_rgb = q_rgb.tryGet()
#         if in_rgb is not None:
#             frame = in_rgb.getCvFrame()
        
#         if frame is not None:
#             cv2.imshow("preview", frame)
#             if cv2.waitKey(1) == ord('q'):
#                 break
app = FastAPI()
streaming = False


def generate_frames():
    # if pipeline:
                global img
                img = frame.copy()
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
    global streaming, pipeline
    streaming = False
    if device:
        device.close()
        global device
        device = None
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
