import cv2
import numpy as np 
from paper_extraction import *
from bubble_sheet_answer import *

image= cv2.imread("omr.png") 

paper=extract_the_paper_from_image(image)

answers=get_student_answer(paper,200,(15,50))

print(answers,len(answers))

image= cv2.imread("mo3ed1.png") 

paper=extract_the_paper_from_image(image)

answers=get_student_answer(paper,200,(15,50))

print(answers,len(answers))

image= cv2.imread("omr2.png") 

paper=extract_the_paper_from_image(image)

answers=get_student_answer(paper,200,(15,50))

print(answers,len(answers))
