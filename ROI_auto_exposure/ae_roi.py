from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np

# Press WASD to move a manual ROI window for auto-exposure control.
# Press N to go back to the region controlled by the NN detections.

previewSize = (1920, 1080)

