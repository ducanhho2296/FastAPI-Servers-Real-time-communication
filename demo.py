import numpy as np  # numpy - manipulate the packet data returned by depthai
import cv2  # opencv - display the video stream
import depthai  # depthai - access the camera and its data packets

pipeline = depthai.Pipeline()

cam_rgb = pipeline.create(depthai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 640)
cam_rgb.setInterleaved(False)

#create output
xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)


#initialize DepthAI
with depthai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("rgb")
    frame = None   
    while True:
        in_rgb = q_rgb.tryGet()
        if in_rgb is not None:
            frame = in_rgb.getCvFrame()
        
        if frame is not None:
            cv2.imshow("preview", frame)
            if cv2.waitKey(1) == ord('q'):
                break