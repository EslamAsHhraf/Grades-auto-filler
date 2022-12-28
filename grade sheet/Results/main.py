## import nessary library

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation as inter
from contour_sort import *
from commonfunctions import *
from Fix_Image_Orientation import *
from find_counters import *
from pathlib import Path
####################################### Main ##########################################################
warpedImgs = cv2.imread('../Walid/imgs/6.jpg')
Image_Orientation_output =Image_Orientation(img_original=img_original)


## make image gray and make threshold on image
img_output = cv2.cvtColor(Image_Orientation_output,cv2.COLOR_BGR2GRAY)
img_output= cv2.adaptiveThreshold(img_output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 51, 4)

img= img_output.copy()

img_final=kernal(img=img)

print_contours(img_final_bin=img_final,orignal_img=Image_Orientation_output)