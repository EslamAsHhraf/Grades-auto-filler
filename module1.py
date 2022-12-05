import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('bubble sheet\omr.png')
cv2.imshow('image',image)
cv2.waitKey(0)