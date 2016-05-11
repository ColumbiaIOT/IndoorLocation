import picamera
import sys
import numpy as np
import cv2

import RPi.GPIO as gp
from matplotlib import pyplot as plt


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

gp.output(7, False)
gp.output(11, False)
gp.output(12, True)
#camera.capture('right.png')

sizes = ['A0.25', 'A0.5', 'A1', 'A1.5']
# Get image name from command line arguments
if len(sys.argv) != 2:
    print "ERROR, Number of arguments = 1 (image name)"
    exit()

IMAGE = sys.argv[1]
#camera = picamera.PiCamera()

# Capture and save picture
try:
    camera.capture('{}'.format(IMAGE))
except Exception as e:
    print "ERROR: " + str(e)
    exit()

# Open captured image in OpenCV
image = cv2.imread(IMAGE)

# Convert image BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_red = np.array([0,100,100])
upper_red = np.array([20,255,255])
#lower_red = np.array([160,100,100])
#upper_red = np.array([179,255,255])

# Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lower_red, upper_red)
 
# find contours in the masked image and keep the largest one
(_, cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
#print np.type(cnts)
#print np.shape(cnts)
c = max(cnts, key=cv2.contourArea)
#print c
#c = cnts[]
# contour size
print cv2.contourArea(c)
f =  open ('piCam_calib/Try/5ft.txt', 'w')
f.write(str(cv2.contourArea(c)))
f.close()
 
# approximate the contour
peri = cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, 0.05 * peri, True)
 
# draw a green bounding box surrounding the red game
cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
cv2.imshow(IMAGE, image)
cv2.waitKey(0)
