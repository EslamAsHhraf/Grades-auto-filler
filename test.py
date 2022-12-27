import os
import cv2
import numpy as np 
from paper_extraction import *
from bubble_sheet_answer import *
import glob

path='./testCases/'
dir_list = os.listdir(path)
for name in dir_list:
    try:
        print(name)
        
        image= cv2.imread(path+name) 

        paper=extract_the_paper_from_image(image,name)

        answers=get_student_answer(paper,name)
        answers= [(i+1,j) for i,j in enumerate(answers)]
        f = open(path+"answers/"+os.path.splitext(name)[0]+".txt", "a")
        for ans in answers:
            f.write("%s\n" % ':'.join((str(ans[0]),ans[1])))
        f.close()
    except:
        print("error hena")
