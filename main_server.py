from fastapi import FastAPI
import uvicorn
import numpy as np
import cv2
from demo import 

# TODO: write your webcam capturing from here
# COPY PASTE WEBCAM CODE HERE

    def open(self):
        cameraID = self.camera_source
        try:
            self.video_capture = cv2.VideoCapture(cameraID)
        except RuntimeError:
            self.video_capture.release()
            print("Unable to open camera")
            return
        # Grab the first frame to start the video capturing
        self.grabbed, self.img = self.video_capture.read()
        return True

    def start(self):
        try:
            if self.running:
                print('Video capturing is already running')
                return None
                # create a thread to read the camera image
            if self.video_capture is not None:
                self.running = True
                self.read_thread = threading.Thread(target=self._updateCamera, daemon=True)
                self.read_thread.start()
            return self
        except Exception as e:
            print(e)
            return False

    def read(self):
        with self.read_lock:
            img = self.img
        return img

    def _updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, img = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.img = img
            except RuntimeError:
                print("Could not read image from camera")

    def stop(self):
        try:
            self.running = False
        except Exception as e:
            print(e)

    def release(self):
        if self.video_capture is not None:
            self.video_capture.release()



class MainServer(CamCapture):

    def __init__(self, server_model_path, server_cam_source=0):
        # self.model_path =server_model_path
        # self.camera_source = server_cam_source
        self.inference_engine = ModelServer(model_path=server_model_path)
        self.camera_engine = CamCapture(source=server_cam_source)

    def start(self):
        pass

    def stop(self):
        pass

    def process(self):
        self.camera_engine.open()
        self.camera_engine.start()

        frame = self.camera_engine.read()
        img = self.inference_engine.infer(image=frame)
        pred, proto_mask = self.inference_engine.load_network()
        preview_img = self.inference_engine.draw_segmentation(im0=frame, img=img, pred=pred, proto_mask=proto_mask)
        return preview_img


app = FastAPI()
model_path = "H:\GITHUB\yolov5\yolov5s-seg.onnx"
camera_source = 0
main_machine = MainServer(server_model_path=model_path, server_cam_source=camera_source)


@app.post("/start")
async def start_inference():
    print('Start model inference')
    main_machine.start()
    pass


@app.post("/stop")
async def stop_inference():
    print('Stop model inference')
    main_machine.stop()
    pass


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
