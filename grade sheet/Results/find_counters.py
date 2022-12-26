## import nessary library

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation as inter
from contour_sort import *
from commonfunctions import *
from pathlib import Path


def kernal (img):
    
    (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Invert the image
    img_bin = 255-img_bin
    # Defining a kernel length

    kernel_length = np.array(img).shape[1]//40
    
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))

    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Draw verticle lines
    verticle_lines_img = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(verticle_lines_img, verticle_kernel, iterations=3)
    cv2.imwrite('./kernal/verticle_lines_img.jpg',verticle_lines_img)

    # Draw horizontal lines
    horizontal_lines_img = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(horizontal_lines_img, hori_kernel, iterations=3)
    cv2.imwrite('./kernal/horizontal_lines_img.jpg',horizontal_lines_img)


    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=3)
    
    (thresh, img_final_threshold) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) 
    second_kernal=np.ones((3,3))

    #dia=cv2.erode(img_final_bin,kernal_two,iterations=1)
    img_output=cv2.dilate(img_final_threshold,second_kernal,iterations=2)
   
    cv2.imwrite('./kernal/img_final_threshold.jpg',img_output)

    return img_output

def print_contours(img_final_bin,orignal_img):
    contours = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted_counter(contours)
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (cnts, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), key=lambda b:b[1][0]))
    idx = 0
    for c in contours:
            # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
    # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
        if (w>10 and h>10 and h <300 and w<1000 ):
            idx += 1
            new_img = orignal_img[y:y+h, x:x+w]
            #show_images([new_img], ['./croped2/'+str(idx)+'.jpg'])
            cv2.imwrite('./contours/'+str(idx)+'.jpg',new_img)


####################################### Main ##########################################################

## Read image 
img_original = cv2.imread('../Walid/warpedImgs/3.jpg')
# show_images([img_original], ['original'])


## make image gray and make threshold on image 
img_output = cv2.cvtColor(img_original,cv2.COLOR_BGR2GRAY)
img_output= cv2.adaptiveThreshold(img_output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 51, 12)
# show_images([img_output], ['Warped'])
cv2.imwrite('./Warped.jpg',img_output)

img= img_output.copy()
# show_images([img],['threshold image'])

img_final=kernal(img=img)
Path("contours").mkdir(parents=True, exist_ok=True)
print_contours(img_final_bin=img_final,orignal_img=img)