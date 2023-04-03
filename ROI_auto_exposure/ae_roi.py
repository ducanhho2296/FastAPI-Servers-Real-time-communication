from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np

# Press WASD to move a manual ROI window for auto-exposure control.
# Press N to go back to the region controlled by the NN detections.

previewSize = (640,480)

# Create pipeline
pipeline = dai.Pipeline()

# Define source and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setPreviewSize(previewSize)
camRgb.setInterleaved(False)

camControlIn = pipeline.create(dai.node.XLinkIn)
camControlIn.setStreamName('camControl')
camControlIn.out.link(camRgb.inputControl)


# Linking
xoutRgb = pipeline.create(dai.node.XLinkOut)
xoutRgb.setStreamName("rgb")
camRgb.preview.link(xoutRgb.input)




def clamp(num, v0, v1):
    return max(v0, min(num, v1))

def asControl(roi):
    camControl = dai.CameraControl()
    camControl.setAutoExposureRegion(*roi)
    return camControl

class AutoExposureRegion:
    def __init__(self, position=(0,0),size = (200, 200),maxDims=previewSize):
        self.step = 10
        self.position = position
        self.size = size
        self.resolution = camRgb.getResolutionSize()
        self.maxDims = maxDims

    def grow(self, x=0, y=0):
        self.size = (
            clamp(x + self.size[0], 1, self.maxDims[0]),
            clamp(y + self.size[1], 1, self.maxDims[1])
        )

    def move(self, x=0, y=0):
        self.position = (
            clamp(x + self.position[0], 0, self.maxDims[0]),
            clamp(y + self.position[1], 0, self.maxDims[1])
        )

    def endPosition(self):
        return (
            clamp(self.position[0] + self.size[0], 0, self.maxDims[0]),
            clamp(self.position[1] + self.size[1], 0, self.maxDims[1]),
        )

    def toRoi(self):
        roi = np.array([*self.position, *self.size])
        # Convert to absolute camera coordinates
        #use denominator as resolution[1]
        if self.maxDims[0] != self.maxDims[1]:
            roi = roi * self.resolution[1] // self.maxDims[1]

        elif self.maxDims[0] == self.maxDims[1]:
            #move the ROI if we have cropped image
            roi = roi * self.resolution[1] // self.maxDims[1]
            roi[0] += (self.resolution[0] - self.resolution[1]) // 2  # x offset for device crop 
        return roi


if __name__ == "__main__":
# Connect to device and start pipeline
    with dai.Device(pipeline) as device:

        # Output queues will be used to get the rgb frames and nn data from the outputs defined above
        qControl = device.getInputQueue(name="camControl")
        qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        frame = None
        detections = []

        nnRegion = True
        region = AutoExposureRegion()

        def displayFrame(name, frame):
            if not nnRegion:
                cv2.rectangle(frame, region.position, region.endPosition(), (0, 255, 0), 2)
            cv2.imshow(name, frame)
        while True:
            # Instead of get (blocking), we use tryGet (non-blocking) which will return the available data or None otherwise
            inRgb = qRgb.tryGet()

            if inRgb is not None:
                frame = inRgb.getCvFrame()

            if frame is not None:
                displayFrame("rgb", frame)

            key = cv2.waitKey(1)
            if key == ord('n'):
                print("AE ROI controlled by NN")
                nnRegion = True
            elif key in [ord('w'), ord('a'), ord('s'), ord('d'), ord('+'), ord('-')]:
                nnRegion = False
                if key == ord('a'):
                    region.move(x=-region.step)
                if key == ord('d'):
                    region.move(x=region.step)
                if key == ord('w'):
                    region.move(y=-region.step)
                if key == ord('s'):
                    region.move(y=region.step)
                if key == ord('+'):
                    region.grow(x=10, y=10)
                    region.step = region.step + 1
                if key == ord('-'):
                    region.grow(x=-10, y=-10)
                    region.step = max(region.step - 1, 1)
                print(f"Setting static AE ROI: {region.toRoi()} (on frame: {[*region.position, *region.endPosition()]})")
                qControl.send(asControl(region.toRoi()))
            elif key == ord('q'):
                break


