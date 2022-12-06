import cv2
import numpy as np 
from paper_extraction import *
from bubble_sheet_answer import *

image= cv2.imread("omr.png") 

paper=extract_the_paper_from_image(image)

print(get_student_answer(paper,200,(15,50),1,5))
