#/usr/bin/env python3

import cv2
from matplotlib import pyplot as plt
import numpy

im = cv2.imread('examples/input/210216_Nouvel_0435_13_14_CanonEOS_img-4311.jpg')

B = im[,, 2]
Y = 255-B

thresh = cv2.adaptiveThreshold(Y, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 35, 5)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

x = []

for i in range(0, len(contours)):
	if cv2.contourArea(contours[i]) > 100:
		x.append(contours[i])

cv2.drawContours(im, x, -1, (255,0,0), 2)

plt.savefigure('return.png', dpi=300)


