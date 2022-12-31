## import nessary library

import cv2
from contour_sort import *
from commonfunctions import *
from Fix_Image_Orientation import *
from find_counters import *
import shutil
import os
import pickle


def load_models():
    loaded_svc = pickle.load(open('./Train/SVC.sav', 'rb'))
    loaded_knn = pickle.load(open('./Train/KNN.sav', 'rb'))
    loaded_rf = pickle.load(open('./Train/RF.sav', 'rb'))
    loaded_lr = pickle.load(open('./Train/LR.sav', 'rb'))
    
    return loaded_svc, loaded_knn, loaded_rf, loaded_lr
    
####################################### Main ##########################################################
def GradesSheet(path,OCR_flag):
    print(OCR_flag)
    #MODELS INITIALIZATION
    loaded_svc, loaded_knn, loaded_rf, loaded_lr = load_models()
    warpedImgs = cv2.imread(path)
    if( os.path.isdir('./contours')):
        shutil.rmtree('./contours')

    Image_Orientation_output =Image_Orientation(img_original=warpedImgs)
    ## make image gray and make threshold on image
    img_output = cv2.cvtColor(Image_Orientation_output,cv2.COLOR_BGR2GRAY)
    img_output= cv2.adaptiveThreshold(img_output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 51, 12)

    img= img_output.copy()

    img_final=kernal(img=img)

    cut_contours(img_final_bin=img_final,orignal_img=img_output,loaded_svc=loaded_svc, loaded_knn=loaded_knn, loaded_rf=loaded_rf, loaded_lr=loaded_lr,OCR_flag=OCR_flag)