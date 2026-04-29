# import OpenCV, an essential computer vision library
# in terminal, write "pip install opencv-python"
import cv2

import numpy as np
import matplotlib.pyplot as plt

# the image path
path = 'images/gate_img.png'

# read the image
img = cv2.imread(path)

########### ADD CODE HERE ################################
# this task involves analyzing an image taken from the Robosub
# competition. Please fill in the code based on the comments
# using the OpenCV documentation.

# convert to grayscale (why?)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# blur the image (why?)
kernel_size = (5,5)
gray_blur = cv2.GaussianBlur(gray, kernel_size, 0)

# get the edges 
edges = cv2.Canny(gray_blur, 50, 150)

# Hough Circle detection 
# https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html
circles = cv2.HoughCircles(
    gray_blur,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=50,
    param1=100,
    param2=30,
    minRadius=15,
    maxRadius=30
)

##########################################################

# copy image for drawing
output = img.copy()

# draw circles
if circles is not None:
    # fix datatype
    circles = np.uint16(np.around(circles))

    for x, y, r in circles[0, :]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 2)

# convert back to RGB
output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

# plot it
plt.figure(figsize=(24, 8))

plt.subplot(1, 3, 1)
plt.title("Original image")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Edges")
plt.imshow(edges, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("Hough Circles")
plt.imshow(output_rgb)
plt.axis("off")

plt.tight_layout()
plt.show()