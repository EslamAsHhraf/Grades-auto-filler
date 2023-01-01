import os
import cv2
import numpy as np 
from paper_extraction import *
from bubble_sheet_answer import *
import glob
from xlwt import Workbook
from openpyxl import load_workbook

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
