import cv2
import numpy as np 
from paper_extraction import *
from bubble_sheet_answer import *

image= cv2.imread("omr.png") 
# cv2.imshow('image',image)
# cv2.waitKey(0)

paper=extract_the_paper_from_image(image)

answers=get_student_answer(paper,200,(15,50),1,5)

print(answers,len(answers))
