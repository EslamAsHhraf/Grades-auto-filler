import cv2
import numpy as np
from crop_image import *


def extract_the_paper_from_image(image,imageName):
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptively_thresholded = cv2.adaptiveThreshold(gray_scale,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imwrite(f'./first adptive thresholding/{imageName}',adaptively_thresholded)
    contours, _ = cv2.findContours(adaptively_thresholded,
                                    cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if (len(contours) > 0):
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        paper_contour = None
        paper = image
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            ratio = 0.01
            approx = cv2.approxPolyDP(cnt, ratio*peri, True)
            #print(len(approx),cv2.contourArea(cnt), image.shape[0]*image.shape[1])
            if (len(approx) == 4 and cv2.contourArea(cnt)>0.2*image.shape[0]*image.shape[1]):
                paper_contour = approx
                paper = four_point_transform(image, paper_contour.reshape(4, 2))
            else:
                break
    return paper