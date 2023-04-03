from ae_roi import AutoExposureRegion, asControl
import cv2  
import depthai as dai 
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

global streaming
streaming = False
pipeline = dai.Pipeline()

cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)

#create controller
camControlIn = pipeline.create(dai.node.XLinkIn)
camControlIn.setStreamName('camControl')
camControlIn.out.link(cam_rgb.inputControl)
#create output
xout_rgb = pipeline.create(dai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

app = FastAPI()
streaming = False

global roi
roi = AutoExposureRegion(position=(100,0),size=(100,100), maxDims=(640,480)) 

def generate_frames():
    # if pipeline:
    global device
    with dai.Device(pipeline) as device:
        qControl = device.getInputQueue(name="camControl")
        q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        frame = None  
        while streaming:
            in_rgb = q_rgb.tryGet()
            if in_rgb is not None:
                frame = in_rgb.getCvFrame()
            if frame is not None:
                global img
                img = frame.copy()

                cv2.rectangle(frame, roi.position, roi.endPosition(), (0,255,0),2)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_encoded = buffer.tobytes()
                qControl.send(asControl(roi.toRoi()))
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded + b'\r\n')
            # yield img


@app.get('/')
async def index():
    return {"message": "Welcome to the webcam streaming application!"}


@app.get('/video_feed')
async def video_feed():
    global streaming
    streaming = True
    return StreamingResponse(generate_frames(), 
                             media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/stop_stream')
async def stop_stream():
    global streaming, device
    streaming = False
    if device:
        device.close()
        device = None
    return {"message": "Streaming stopped successfully."}

@app.post('/move_roi/up')
async def move_roi_up():
    global roi
    roi.move(y=-roi.step)
    return {"message": "ROI moved up!"}

@app.post('/move_roi/down')
async def move_roi_down():
    global roi
    roi.move(y=roi.step)
    return {"message": "ROI moved down!"}

@app.post('/move_roi/left')
async def move_roi_left():
    global roi
    roi.move(x=-roi.step)
    return {"message": "ROI moved left!"}

@app.post('/move_roi/right')
async def move_roi_right():
    global roi
    roi.move(x=roi.step)
    return {"message": "ROI moved right!"}

@app.post('/move_roi/resize_up')
async def resize_roi_up():
    global roi
    roi.grow(x=10, y=10)
    return {"message": "ROI resized up!"}

@app.post('/move_roi/resize_down')
async def resize_roi_down():
    global roi
    roi.grow(x=-10, y=-10)
    return {"message": "ROI resized down!"}



if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)


