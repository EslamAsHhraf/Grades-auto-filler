import cv2
import numpy as np
import imutils
from imutils import contours as imcnts
from crop_image import *

colors=[(255,0,0)
,(0,255,0)
,(0,0,255)
,(0,255,255)
,(255,255,0)
,(0,0,255)
,(0,255,255)
,(255,0,255)
,(192,192,192)
,(128,128,128)
,(128,0,0)
,(128,128,0)
,(0,128,0)
,(128,0,128)
,(0,128,128)
,(0,0,128),
       (255,215,0)]

def get_student_answer(paper,threshold_value,bubble_size):
    # Get the gray scale paper 
    gray_scale_paper = cv2.cvtColor(paper,cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',gray_scale_paper)
    cv2.waitKey(0)

    # Histogram Equalization
    equalized_gray_scale_paper=cv2.equalizeHist(gray_scale_paper)

    # Get binary paper
    _,thresholded=cv2.threshold(equalized_gray_scale_paper,30,255, cv2.THRESH_BINARY_INV)
    cv2.imshow('image',thresholded)
    cv2.waitKey(0)

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

    # Detect the number of choices and the number of columns
    xs_set=set()
    for cnt in question_cnts:
        (x,y,w,h)=cv2.boundingRect(cnt)
        if(all([ x-i not in xs_set and x+i not in xs_set for i in np.arange(0,5)])):
            xs_set.add(x)
    number_of_bubbles=len(xs_set)
    print(number_of_bubbles)
    xs=np.array(list(sorted(xs_set)))
    dist=np.append(xs[1:],xs[-1])-xs
    distance_set=[]
    for diff in dist:
        if(len(distance_set)==0 or all([ diff-i != distance_set[-1] and diff+i != distance_set[-1] for i in np.arange(0,5)])):
            distance_set.append(diff)
    distance_set.pop()
    number_of_columns=sum([x > distance_set[i] and x > distance_set[i+2] for i, x in enumerate(distance_set[1:-1])])+1
    number_of_choices=number_of_bubbles//number_of_columns

    print(number_of_columns,number_of_choices)

    # Get student answers
    answers=[]

    # Iterate over each row
    qs=0
    for (_,i) in enumerate(np.arange(0,len(question_cnts),number_of_columns*number_of_choices)):
        # Get all bubbles of the current row which has (number_of_columns) questions
        curr_row_cnts,_=imcnts.sort_contours(question_cnts[i:i+number_of_columns*number_of_choices])
        
        # Iterate over each question
        for k in np.arange(0,len(curr_row_cnts),number_of_choices):

            # Current Question answers
            curr_ques_cnts=curr_row_cnts[k:k+number_of_choices]
            color1=colors[qs%len(colors)]
            qs=qs+1
            cv2.drawContours(paper,curr_ques_cnts,-1,color1, 1)

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
    cv2.imshow('image',paper)
    cv2.waitKey(0)
    return answers