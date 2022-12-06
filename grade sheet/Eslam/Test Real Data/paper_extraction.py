import cv2
import numpy as np
from crop_image import *


def extract_the_paper_from_image(image):
    paper = None
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('./zz333.jpg',gray_scale) 
    edged = cv2.Canny(gray_scale, 75, 200)
    cv2.imwrite('./zedge.jpg',edged) 
    contours, _ = cv2.findContours(edged,
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if (len(contours) > 0):
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        paper_contour = None
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            ratio = 0.01
            approx = cv2.approxPolyDP(cnt, ratio*peri, True)
            if (len(approx) == 4):
                paper_contour = approx
                break
        paper = four_point_transform(image, paper_contour.reshape(4, 2))
    return paper