# -*- coding: utf-8 -*-
"""houghtrans.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jLcf23cIIX-GGj97JrqI29OqiFkYTd81
"""

# Commented out IPython magic to ensure Python compatibility.
# to find the execution time of each cell 
!pip install ipython-autotime
# %load_ext autotime

"""**scratch code**"""

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

img = cv2.imread('/content/road-line-detection-0.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
height, width = edges.shape
hough_space = np.zeros((180, int(np.sqrt(height**2 + width**2))), dtype=np.uint8)

# Populate the Hough space
for y in range(height):
    for x in range(width):
        if edges[y, x] != 0:
            for theta in range(0, 180):
                rho = int(x * np.cos(theta*np.pi/180) + y * np.sin(theta*np.pi/180))
                hough_space[theta, rho] += 1

threshold = 200
lines = []
# Detect lines from the Hough space
for theta in range(0, 180):
    for rho in range(hough_space.shape[1]):
        if hough_space[theta, rho] > threshold:
            a = np.cos(theta*np.pi/180)
            b = np.sin(theta*np.pi/180)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            lines.append([(x1, y1), (x2, y2)])

# Draw the detected lines on a copy of the original image
img_copy = img.copy()
for line in lines:
    pt1, pt2 = line[0], line[1]
    cv2.line(img_copy, pt1, pt2, (0, 0, 255), 2)

# Display the original and the detected lines side by side
cv2_imshow(img)
cv2_imshow(img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""**cv2.HoughLines()**"""

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# Load the image
img = cv2.imread('/content/road-line-detection-0.jpeg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection to the grayscale image
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply HoughLines function to the edge-detected image
lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=200)

# Draw the detected lines on the original image
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the result
cv2_imshow(img)
cv2.waitKey(0)
cv2.destroyAllWindows()

