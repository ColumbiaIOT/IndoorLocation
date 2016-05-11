import picamera
from picamera.array import PiRGBArray
import time
import numpy as np
import cv2
import RPi.GPIO as gp

def get_distance(area):
    
    A = 14.8773194566 #15.7917186914
    t = -0.000411795356453 #-0.000145498314628
    y0 = 4.05229017348 #4.41289353291
    
    return A * np.exp(area * t) + y0


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


# Initialize camera
FPS = 32
#camera = picamera.PiCamera()
#camera.resolution = (640, 480)
camera.framerate = FPS
rawCapture = PiRGBArray(camera)

# For saving video
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter('output.avi', fourcc, FPS, (640, 480))

# Allow camera to initialize
time.sleep(0.1)

# Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    # Open captured image in OpenCV
    image = frame.array

    # Convert image BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])
    #upper_red = np.array([179, 255, 255])
    #lower_red = np.array([160, 100, 100])


    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    try:
 
        # find contours in the masked image and keep the largest one
        (_, cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts, key=cv2.contourArea)
        #c = np.sort(cbts, key=cv2.contourArea)
	#c = cnts[-3]
        # approximate the contour
        peri = 0.1*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
        
        # Compute center of countour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    
        # draw a green bounding box surrounding the red game
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
        # Predict distance
        cv2.putText(image, '%2.1f' % get_distance(cv2.contourArea(c)), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        
    except Exception as e:
        #print 'problem'
        pass
    
    # Save video
    #out.write(image)   

    # Display video
    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    
    if key == ord("q"):
        break

#out.release()
cv2.destroyAllWindows()
