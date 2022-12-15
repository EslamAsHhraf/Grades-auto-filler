import cv2
import numpy as np 
from paper_extraction import *
from bubble_sheet_answer import *
import glob


for name in glob.glob('./testCases/*'):
    print(name)
    image= cv2.imread(name) 

    paper=extract_the_paper_from_image(image)

    answers=get_student_answer(paper,200,(15,50))

    print(answers,len(answers))

# image= cv2.imread('omr.jpg') 
# paper=extract_the_paper_from_image(image)
# paper=extract_the_paper_from_image(paper)
# answers=get_student_answer(paper,150,(15,50))

# print(answers,len(answers))
