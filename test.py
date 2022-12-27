import os
import cv2
import numpy as np 
from paper_extraction import *
from bubble_sheet_answer import *
import glob

path='./testCases0/'
dir_list = os.listdir('./testCases0/')
for name in dir_list:
    print(name)
    image= cv2.imread(path+name) 

    paper=extract_the_paper_from_image(image,name)

    answers=get_student_answer(paper,name)

    #print(answers,len(answers))
    answers= [(i+1,j) for i,j in enumerate(answers)]
    print(answers)

# image= cv2.imread('omr2.png') 
# paper=extract_the_paper_from_image(image)
# answers=get_student_answer(paper,150,(15,50))

# print(answers,len(answers))
