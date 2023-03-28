from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np

# Press WASD to move a manual ROI window for auto-exposure control.
# Press N to go back to the region controlled by the NN detections.

previewSize = (1920, 1080)

# Create pipeline
pipeline = dai.Pipeline()

# Define source and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setPreviewSize(previewSize)
camRgb.setInterleaved(False)

camControlIn = pipeline.create(dai.node.XLinkIn)
camControlIn.setStreamName('camControl')
camControlIn.out.link(camRgb.inputControl)

