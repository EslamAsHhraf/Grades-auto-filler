import os
import cv2
import numpy as np
from paper_extraction import *
from bubble_sheet_answer import *
import glob
import pickle
# Writing to an excel 
# sheet using Python
import xlwt
from xlwt import Workbook
  
# Workbook is created
wb = Workbook()
  
# add_sheet is used to create sheet.
answer_sheet = wb.add_sheet('Answer Sheet')
answer_sheet.write(0, 0, 'id') 
  





def load_models():
    loaded_svc = pickle.load(open('./Train/SVC.sav', 'rb'))
    loaded_knn = pickle.load(open('./Train/KNN.sav', 'rb'))
    loaded_rf = pickle.load(open('./Train/RF.sav', 'rb'))
    loaded_lr = pickle.load(open('./Train/LR.sav', 'rb'))

    return loaded_svc, loaded_knn, loaded_rf, loaded_lr


#####################################################################
loaded_svc, loaded_knn, loaded_rf, loaded_lr = load_models()



path = './id_test/'
dir_list = os.listdir(path)
if not os.path.isdir(f'./{path}/answers/'):
    os.mkdir(f'./{path}/answers/')
for i,name in enumerate(dir_list):
    print(name)

    image = cv2.imread(path+name)
    cv2.imshow('h',image)
    cv2.waitKey(0)
    paper = extract_the_paper_from_image(image, name)

    answers, id = get_student_answer(paper, name, loaded_svc, loaded_knn, loaded_rf, loaded_lr)
    answer_sheet.write(0, 1, id)
    for i, ans in enumerate(answers):
        answer_sheet.write(i+1, 0, 'question'+str(i))
        answer_sheet.write(i+1, 1, ans)
    answers = [(i+1, j) for i, j in enumerate(answers)]
    # answer_sheet.write(2, 0, answers)
    full_path = path+"answers/"+os.path.splitext(name)[0]+".txt"
    open(full_path, 'w').close()
    f = open(full_path, "a")
    for ans in answers:
        f.write("%s\n" % ':'.join((str(ans[0]), ans[1])))
    f.close()
wb.save('xlwt example.xls')