## import nessary library

import cv2
from contour_sort import *
from commonfunctions import *
from Fix_Image_Orientation import *
from find_counters import *
import shutil
import os
import pickle
from paper_extraction import *
from bubble_sheet_answer import *
from xlwt import Workbook

def load_models():
    loaded_svc = pickle.load(open('./Train/SVC.sav', 'rb'))
    loaded_knn = pickle.load(open('./Train/KNN.sav', 'rb'))
    loaded_rf = pickle.load(open('./Train/RF.sav', 'rb'))
    loaded_lr = pickle.load(open('./Train/LR.sav', 'rb'))
    
    return loaded_svc, loaded_knn, loaded_rf, loaded_lr

####################################### Main ##########################################################
loaded_svc, loaded_knn, loaded_rf, loaded_lr = load_models()

def GradesSheet(path,OCR_flag):
    print(OCR_flag)
    #MODELS INITIALIZATION
    
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

def run_all_bubble_sheets():
    path='./testCases/'
    results_path='./Results/'
    dir_list = os.listdir(path)
    if not os.path.isdir(results_path):
        os.mkdir(results_path)
    if not os.path.isdir(results_path+'answers/'):
        os.mkdir(results_path+'answers/')
    for name in dir_list:
        print(name)
        image= cv2.imread(path+name) 
        paper=extract_the_paper_from_image(image,name)
        answers=get_student_answer_without_ID(paper,name)
        answers= [(i+1,j) for i,j in enumerate(answers)]
        wb=Workbook() 
        full_path=results_path+"answers/"+os.path.splitext(name)[0]+".xls"
        if os.path.isfile(full_path):
            print('sheet1 exists')
            os.remove(full_path)
        sheet = wb.add_sheet(name,cell_overwrite_ok=True)
        for ans in answers:
            sheet.write(0, 0,'Question')
            sheet.write(ans[0], 0,'Q'+str(ans[0]))
            sheet.write(0, 1,'Answer')
            sheet.write(ans[0],1, ans[1])
        wb.save(full_path)

# try:
#     run_all_bubble_sheets()
# except:
#     print("error")