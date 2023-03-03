from fastapi import FastAPI
import uvicorn
import numpy as np
import cv2
import depthai


class CamCapture:

    def __init__(self, save_path=str):
        self.pipeline = depthai.Pipeline()
        self.device = None
        self.img = None
        self.save_path = save_path
    def start(self):
        cam_rgb = self.pipeline.create(depthai.node.ColorCamera)
        cam_rgb.setPreviewSize(640, 640)
        cam_rgb.setInterleaved(False)

        #create output
        xout_rgb = self.pipeline.create(depthai.node.XLinkOut)
        xout_rgb.setStreamName("rgb")
        cam_rgb.preview.link(xout_rgb.input)
        
        with depthai.Device(self.pipeline) as device:
            self.device = device
            q_rgb = device.getOutputQueue('rgb')
            frame = None
            while True:
                in_rgb = q_rgb.tryGet()
                if in_rgb is not None:
                    frame = in_rgb.getCvFrame()
                    self.img = frame
                if frame is not None:
                    cv2.imshow('Preview', frame)
    
    def stop(self):
        if self.device:
            self.pipeline.stop()
            self.device.close()


    def capture(self):
        if self.img:
            cv2.imwrite(self.save_path, self.img)
        else:
            print("no streaming was found")



class MainServer(CamCapture):

    def __init__(self, path=str):
        # self.model_path =server_model_path
        # self.camera_source = server_cam_source
        self.camera_engine = CamCapture(save_path=path)

    def start(self):
        self.camera_engine.start()

    def stop(self):
        self.camera_engine.stop()

    def capture(self):
        self.camera_engine.capture()


app = FastAPI()
path = "H:\GITHUB"
camera_source = 0
main_machine = MainServer(path=path)


@app.post("/start")
async def start_inference():
    print('Start model inference')
    main_machine.start()


@app.post("/stop")
async def stop_inference():
    print('Stop model inference')
    main_machine.stop()


def generate():
    while True: # TODO: add logic to stop camera here
        image = main_machine.process()
        # red, image = cap.read()
        if image is not None:
            retval, image_encoded = cv2.imencode(".jpg", image)

            if image_encoded is not None:
                frame = image_encoded.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



@app.get("/preview")
async def get_images():
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")
    # print("Please look at here: https://stackoverflow.com/questions/65971081/stream-video-to-web-browser-with-fastapi")
    # pass

from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
if __name__ == "__main__":
    print("Model should be loaded only once")
    print("KEEP IT SIMPLE")
    print("start server from here")
    text = "OpenAPI Swagger link"
    target = "http://127.0.0.1:8000/docs"  ## CLICK HERE
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
