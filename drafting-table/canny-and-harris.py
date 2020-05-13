import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('colortestfile.bmp')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

edges = cv.Canny(img,50,200)

##NEU
dst = cv.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv.imshow('dst',img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()

cv.imwrite('out.png', edges)
