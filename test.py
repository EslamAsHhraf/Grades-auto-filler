import cv2
import numpy as np 
from paper_extraction import *

Answer_key= {0:1, 1:4, 2:0, 3:2, 4:0}

image= cv2.imread("1.jpg") 
#image=cv2.resize(image, (image.shape[0]//2,image.shape[1]//2 ))
#cv2.imshow('image',image)
#cv2.waitKey(0)
paper=extract_the_paper_from_image(image)

#cv2.imshow('result',paper)
cv2.imwrite('./result333.jpg',paper) 
cv2.waitKey(0)
_,thresholded=cv2.threshold(gray_scale_paper,55,255,cv2.THRESH_BINARY_INV)