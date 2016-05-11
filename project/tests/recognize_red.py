import picamera
import cv2
import numpy as np

# Get image from raspi camera
camera = picamera.PiCamera()
camera.capture('image.png')
img = cv2.imread('image.png')

# Find color red in image
upper = np.array([65, 65, 225])
lower = np.array([0, 0, 200])
mask = cv2.inRange(img, lower, upper)

# Find contours in the masked image and keep the largest one
(_, cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = max(cnts, key=cv2.contourArea)

# Approximate the contour
peri = cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, 0.05*peri, True)

# Draw a green bounding box surrounding the red game
cv2.drawContours(img, [approx], -1, (0, 225, 0), 4)
cv2.imshow("Image", img)
cv2.waitKey(0)
