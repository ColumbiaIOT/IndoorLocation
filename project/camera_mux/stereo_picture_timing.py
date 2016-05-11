import timeit

setup = """\
import RPi.GPIO as gp
import picamera
import io
import numpy as np
import cv2

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

camera = picamera.PiCamera()
camera.resolution = (640, 480)
streamL = io.BytesIO()
streamR = io.BytesIO()

def take_picture():

    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    camera.capture(streamL, format='yuv')
    
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    camera.capture(streamR, format='yuv')

    #dataL = np.fromstring(streamL.getvalue(), dtype=np.uint8)
    #dataR = np.fromstring(streamR.getvalue(), dtype=np.uint8)

    #imageL = cv2.imdecode(dataL, 1)
    #imageR = cv2.imdecode(dataR, 1)
"""
print timeit.timeit('take_picture()', setup=setup, number=1)
