import cv2
import numpy as np 
from paper_extraction import *

Answer_key= {0:1, 1:4, 2:0, 3:2, 4:0}

image= cv2.imread("omr.png")

paper=extract_the_paper_from_image(image)

cv2.imshow('result',paper)
cv2.waitKey(0)