import subprocess
#from PIL import Image
import cv2
import numpy as np 
import os

import sys

sys.path.insert(0, '/home/lukic/Desktop/FaceDetection/Simple-Flask-ML-APP/object-detection-opencv')

from yolo_as_import import main

#saves new images in detected/...
main('object-detection-opencv/dog.jpg','object-detection-opencv/yolov3.txt', 'object-detection-opencv/yolov3.weights', 'object-detection-opencv/yolov3.cfg')    



