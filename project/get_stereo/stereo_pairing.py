import numpy as np
import cv2

import matplotlib.pyplot as plt

#from sklearn.neighbors import KNeighborsClassifier

# Load images
left_img = cv2.imread("8ft_L_masked.jpg", 0)
right_img = cv2.imread("8ft_R_masked.jpg", 0)

#left_img = cv2.imread("images/baby/view1_4000.png", 0)
#right_img = cv2.imread("images/baby/view5_4000.png", 0)

# Sharpen images
#kernel_sharpen = np.array([[-1,-1,-1,-1,-1],
#                             [-1,2,2,2,-1],
#                             [-1,2,8,2,-1],
#                             [-1,2,2,2,-1],
#                             [-1,-1,-1,-1,-1]]) / 8.0
#left_img = cv2.filter2D(left_img, -1, kernel_sharpen)
#right_img = cv2.filter2D(right_img, -1, kernel_sharpen)

# Initialize detector
detector = cv2.FeatureDetector_create("HARRIS")
extractor = cv2.DescriptorExtractor_create("SIFT")
matcher = cv2.DescriptorMatcher_create("BruteForce")

# detect
left_kp = detector.detect(left_img)
right_kp = detector.detect(right_img)
l_kp, l_d = extractor.compute(left_img, left_kp)
r_kp, r_d = extractor.compute(right_img, right_kp)
matches = matcher.match(l_d, r_d)
sel_matches = [m for m in matches if abs(l_kp[m.queryIdx].pt[1] - r_kp[m.trainIdx].pt[1])]

# This is a guess
triangulation_constant = left_img.shape[1]

# To store points
left_pts = []
right_pts = []
zs = []

# Iterate through matches
max_dist = 20 # Feet
for m in sel_matches:
    left_pt = l_kp[m.queryIdx].pt
    right_pt = r_kp[m.trainIdx].pt
    dispartity = abs(left_pt[0] - right_pt[0])
    try:
        z = triangulation_constant / dispartity
        if z > max_dist:
            continue
    except:
        continue
    # Save points and z to display on image
    left_pts.append(left_pt)
    right_pts.append(right_pt)
    zs.append(z)

# Plot left image
#plt.figure()
#plt.imshow(left_img)
#plt.show()

# Plot distances on blank image
blank_img = left_img
#blank_img = cv2.cv.fromarray(blank, 0)
max_pts = 25
num_pts = 0
for pt,z_ in zip(left_pts,zs):
    org = (int(pt[0]), int(pt[1]))
    cv2.putText(img=blank_img, text="%2.1f" % z_, org=org, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=10, thickness=10, color=(0, 0, 0))
    num_pts += 1
    if num_pts > max_pts:
        break

# Plot distances
plt.figure()
plt.imshow(blank_img)
plt.show()

'''
# Do Classification

# Initialize Classifier
classifier = KNeighborsClassifier(n_neighbors=3)
# Round distances to nearest int
zs_i = [int(z_) for z_ in zs]
# Fit model to distances
classifier.fit(left_pts, zs_i)

# Test input
x_in = []
append = x_in.append
for i in range(left_img.shape[0]):
    for j in range(right_img.shape[1]):
        append((i,j))
# Make predictions
preds = classifier.predict(x_in)
# Distances
dists = np.array(preds).reshape(left_img.shape[0], left_img.shape[1])

# Plot
plt.figure()
plt.imshow(dists)
plt.show()
'''
