import cv2
import numpy as np

dists = [5, 8, 11, 14]

for dist in dists:
    image = cv2.imread('{}ft_L.jpg'.format(str(dist)))
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    upper_red = np.array([179, 255, 255])
    lower_red = np.array([160, 100, 100])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    output = cv2.bitwise_and(image, image, mask=mask)
    cv2.imwrite('{}ft_L_masked.jpg'.format(str(dist)), output)

    image = cv2.imread('{}ft_R.jpg'.format(str(dist)))
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    upper_red = np.array([179, 255, 255])
    lower_red = np.array([160, 100, 100])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    output = cv2.bitwise_and(image, image, mask=mask)
    cv2.imwrite('{}ft_R_masked.jpg'.format(str(dist)), output)    
