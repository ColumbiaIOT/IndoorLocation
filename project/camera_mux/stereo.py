import numpy as np
import cv2
from matplotlib import pyplot as plt
import RPi.GPIO as gp
import picamera

"""
Setup GPIO
"""

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7,  gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)
gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)

gp.output(11, True)
gp.output(12, True)
gp.output(15, True)
gp.output(16, True)
gp.output(21, True)
gp.output(22, True)

"""
Get Images
"""
camera = picamera.PiCamera()

# Left
gp.output(7, False)
gp.output(11, False)
gp.output(12, True)
camera.capture('left.png')

# Right
gp.output(7, False)
gp.output(11, True)
gp.output(12, False)
camera.capture('right.png')

imgL = cv2.imread('left.png',0)
imgR = cv2.imread('right.png',0)

"""
Process images
"""

stereo = cv2.StereoBM_create(numDisparities=64, blockSize=21) #16,15
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()
plt.savefig('stereo_test.png')
