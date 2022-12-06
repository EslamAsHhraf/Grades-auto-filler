import cv2
import numpy as np
import imutils
from imutils import contours as imcnts
from crop_image import *

def get_student_answer(paper,threshold_value,bubble_size,number_of_columns,number_of_choices):
    # Get the gray scale paper 
    gray_scale_paper = cv2.cvtColor(paper,cv2.COLOR_BGR2GRAY)

    # Get binary paper
    _,thresholded=cv2.threshold(gray_scale_paper,threshold_value,255, cv2.THRESH_BINARY_INV)

    # Get the external contours
    pap_cnts,_=cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if there are no contours
    if(len(pap_cnts)==0):
        return "No external contours found"

    # Get the bubbles contours
    pre_question_cnts=[]
    for cnt in pap_cnts:
        (x,y,w,h)=cv2.boundingRect(cnt)
        aspect_ratio=w/h
        if(w>=bubble_size[0] and w<=bubble_size[1] and h>=bubble_size[0] and h<=bubble_size[1] and aspect_ratio>=0.9 and aspect_ratio<=1.1):
            pre_question_cnts.append(cnt)

    # Check if there are no contours
    if(len(pre_question_cnts)==0):
        return "No bubbles contours found"
    
    # Sort the contours from top to bottom
    question_cnts,_=imcnts.sort_contours(pre_question_cnts,method='top-to-bottom')

    # Get student answers
    answers=[]

    # Iterate over each row
    for (_,i) in enumerate(np.arange(0,len(question_cnts),number_of_columns*number_of_choices)):

        # Get all bubbles of the current row which has (number_of_columns) questions
        curr_row_cnts,_=imcnts.sort_contours(question_cnts[i:i+number_of_columns*number_of_choices])
        
        # Iterate over each question
        for k in np.arange(0,len(curr_row_cnts),number_of_choices):

            # Current Question answers
            curr_ques_cnts=curr_row_cnts[k:k+number_of_choices]

            bubbled=None

            for (j,c) in enumerate(curr_ques_cnts):

                # Get the maximum shaded bubble
                mask = np.zeros(thresholded.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                mask= cv2.bitwise_and(thresholded, mask)
                total= cv2.countNonZero(mask)

                if bubbled is None or total > bubbled[0]:
                    bubbled= (total, j)

            answers.append(chr(bubbled[1]+ord('A')))
    return answers