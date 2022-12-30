## import nessary library

import cv2
from contour_sort import *
from commonfunctions import *
from Fix_Image_Orientation import *
from find_counters import *
import shutil
import os
####################################### Main ##########################################################
warpedImgs = cv2.imread('../Walid/imgs/1.jpg')
if( os.path.isdir('./contours')):
    shutil.rmtree('./contours')

Image_Orientation_output =Image_Orientation(img_original=warpedImgs)


## make image gray and make threshold on image
img_output = cv2.cvtColor(Image_Orientation_output,cv2.COLOR_BGR2GRAY)
img_output= cv2.adaptiveThreshold(img_output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 51, 12)

img= img_output.copy()

img_final=kernal(img=img)

print_contours(img_final_bin=img_final,orignal_img=img_output)