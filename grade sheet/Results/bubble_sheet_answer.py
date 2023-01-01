import cv2
import numpy as np
import imutils
from imutils import contours as imcnts
from crop_image import *
import os
from detect_handwritten_ID_Bubble import *

colors=[(255,0,0)
,(0,255,0)
,(0,0,255)
,(255,0,0)
,(0,255,0)
,(0,0,255)
,(0,255,0)
,(255,0,0)
,(255,255,192)
,(225,255,128)
,(128,0,0)
,(128,128,0)
,(0,128,0)
,(128,0,128)
,(0,128,128)
,(0,0,128),
       (255,215,0)]

def get_student_answer_without_ID(paper,imageName):
    # Get the gray scale paper 
    gray_scale_paper = cv2.cvtColor(paper,cv2.COLOR_BGR2GRAY)
    dirname = './Results/gray scale images'
    if not os.path.isdir(f'./{dirname}'):
        os.mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, imageName),gray_scale_paper)

    # Get binary paper
    thresholded=cv2.adaptiveThreshold(gray_scale_paper, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 73, 5)
    dirname = './Results/adaptive thresholded images'
    if not os.path.isdir(f'./{dirname}'):
        os.mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, imageName),thresholded)

    # Get The Eroded Image To Be Used In Calculations Of Answers
    eroded=cv2.erode(thresholded,np.ones((3,3)),iterations=1)
    dirname = './Results/eroded images'
    if not os.path.isdir(f'./{dirname}'):
        os.mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, imageName),eroded)

    #Get Average Area
    areas=[]
    # Get the external contours
    pap_cnts,_=cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Check if there are no contours
    if(len(pap_cnts)==0):
        print("No external contours found")

    # Get the bubbles contours
    pre_question_cnts=[]
    for cnt in pap_cnts:
        (x,y,w,h)=cv2.boundingRect(cnt)
        aspect_ratio=w/h
        peri = cv2.arcLength(cnt, True)
        ratio = 0.01
        approx = cv2.approxPolyDP(cnt, ratio*peri, True)
        curr_cnt_area=cv2.contourArea(cnt)
        if(aspect_ratio>=0.8 and aspect_ratio<=1.2 and len(approx)>=4 and curr_cnt_area>30 and curr_cnt_area>1.5*peri):
            areas.append(curr_cnt_area)
            pre_question_cnts.append(cnt)

    # Check if there are no contours
    if(len(pre_question_cnts)==0):
        print("No bubbles contours found")

    temp=paper.copy()
    cv2.drawContours(temp,pre_question_cnts,-1,(0,255,0), 5)
    dirname = './Results/all circles contours'
    if not os.path.isdir(f'./{dirname}'):
        os.mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, imageName),temp)

    # Get Only Bubbles
    bubble_area=np.median(areas)
    question_cnts_copy=[]
    for i,area  in enumerate(areas):
        if(abs(area-bubble_area)<=bubble_area*.3):
            question_cnts_copy.append(pre_question_cnts[i])
    pre_question_cnts= question_cnts_copy

    temp=paper.copy()
    cv2.drawContours(temp,pre_question_cnts,-1,(0,255,0), 5)
    dirname = './Results/bubbles contours'
    if not os.path.isdir(f'./{dirname}'):
        os.mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, imageName),temp)

    if(len(pre_question_cnts)):
        # Sort the contours from top to bottom
        question_cnts,_=imcnts.sort_contours(pre_question_cnts,method='top-to-bottom')

        # Detect the number of choices and the number of columns
        xs_set=np.array([])
        (_,__,bubble_width,___)=cv2.boundingRect(pre_question_cnts[0])
        for cnt in question_cnts:
            (x,y,w,h)=cv2.boundingRect(cnt)
            xs_set=np.append(xs_set,x)
        xs_set=np.sort(xs_set)
        number_of_bubbles=0
        number_of_xs=len(xs_set)
        number_of_columns=1
        for i in range(1,number_of_xs):
            if(xs_set[i]-xs_set[i-1]>=0.5*bubble_width and xs_set[i]-xs_set[i-1]<=2*bubble_width):
                number_of_bubbles+=1
            elif(xs_set[i]-xs_set[i-1]>2.5*bubble_width):
                number_of_columns+=1
        number_of_bubbles+=number_of_columns
        number_of_choices=number_of_bubbles//number_of_columns
        print(number_of_columns,number_of_choices,number_of_bubbles)

    def detect_number_of_contours(cnts):
        (_,prev_y,___,bubble_height)=cv2.boundingRect(cnts[0])
        #print("height",bubble_height)
        for i,cnt in enumerate(cnts):
            (x,y,w,h)=cv2.boundingRect(cnt)
            if(abs(y-prev_y)>0.4*bubble_height):
                return 1
        return 0

    number_of_questions=len(pre_question_cnts)//number_of_choices
    cut_row=number_of_questions*(number_of_choices+1)
    is_cut=0
    temp=paper.copy()
    if(len(pre_question_cnts)):
        qs=0
        # Get student answers
        answers=[]

        temp_number_of_columns=number_of_columns
        # Iterate over each row
        i=0
        while (i<len(question_cnts)):
            
            # detect number of contours in row
            if(not is_cut):
                is_cut=detect_number_of_contours(question_cnts[i:i+temp_number_of_columns*number_of_choices])
                if(is_cut):
                    temp_number_of_columns-=1
                cut_row=i
            number_of_conts=temp_number_of_columns*number_of_choices

            # Get all bubbles of the current row which has (number_of_columns) questions
            curr_row_cnts,_=imcnts.sort_contours(question_cnts[i:i+number_of_conts])
            
            # Iterate over each question
            for k in np.arange(0,len(curr_row_cnts),number_of_choices):

                # Current Question answers
                curr_ques_cnts=curr_row_cnts[k:k+number_of_choices]
                color1=colors[qs%len(colors)]
                qs=qs+1
                cv2.drawContours(temp,curr_ques_cnts,-1,color1, 5)

                mask_ones=[]
                bubbles=[]
                for j,c in enumerate(curr_ques_cnts):

                    # Get the maximum shaded bubble
                    mask = np.zeros(thresholded.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    mask_ones.append(cv2.countNonZero(mask))
                    mask= cv2.bitwise_and(eroded, mask)
                    total= cv2.countNonZero(mask)
                    bubbles.append(total)
                
                mask_mean=np.mean(mask_ones)
                bubbles=np.array(bubbles)/mask_mean
                bubbled=np.argmax(bubbles)
                total=np.amax(bubbles)
                count_chosen=0
                if(total>0.7):
                    count_chosen=((total-bubbles)<=0.3).sum()
                else:
                    count_chosen=((total-bubbles)<=0.15).sum()
                final_ans=(ord('X')-ord('A')) if(count_chosen!=1) else bubbled
                answers.append(chr(final_ans+ord('A')))
            i+=(temp_number_of_columns*number_of_choices)
    
    # Draw The Questions Contours

    dirname = './Results/questions'
    if not os.path.isdir(f'./{dirname}'):
        os.mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, imageName),temp)

    # Get Number Of Rows
    number_of_rows=0
    x_sorted_conts,_=imcnts.sort_contours(question_cnts)
    (prev_x,_,bubble_width,__)=cv2.boundingRect(x_sorted_conts[0])
    for i,cnt in enumerate(x_sorted_conts):
        (x,y,w,h)=cv2.boundingRect(cnt)
        if(abs(prev_x-x)>=2.5*bubble_width):
            number_of_rows=i
            break
        elif i+1==len(x_sorted_conts):
            number_of_rows=i+1
        prev_x=x
    number_of_rows=number_of_questions if not number_of_rows else number_of_rows//number_of_choices

    # Map The Given Answers To Real Ones
    cut_row=cut_row//(number_of_choices*number_of_columns)
    curr_cnt=0
    final_answers=[0] * number_of_questions
    for i in range(0,number_of_rows):
        for j in range(0,number_of_columns-int(i>=cut_row and is_cut)):
            #print(j*number_of_rows+i+1,curr_cnt+1,int(i>=cut_row and cut_row!=number_of_rows-1))
            final_answers[j*number_of_rows+i]=answers[curr_cnt]
            curr_cnt+=1
    return final_answers


def get_student_answer(paper, loaded_svc, loaded_knn, loaded_rf, loaded_lr):
    # Get the gray scale paper
    gray_scale_paper = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)

    # Get binary paper
    thresholded = cv2.adaptiveThreshold(
        gray_scale_paper, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 73, 5)

    # extract id box from image
    cntr, h = cv2.findContours(
        thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(cntr, key=cv2.contourArea, reverse=True)
    for c in cnt:
        peri = cv2.arcLength(c, True)
        ratio = 0.01
        approx = cv2.approxPolyDP(c, ratio*peri, True)
        if (len(approx) == 4):
            idBoxContour = c
            [intX, intY, intW, intH] = cv2.boundingRect(idBoxContour)
            idBoxImage = paper[intY:intY+intH, intX:intX+intW]
            thresholded[intY:intY+intH, intX:intX+intW] = 0
            break
    id = detect_id(idBoxImage, loaded_svc, loaded_knn, loaded_rf, loaded_lr)

    # Get The Eroded Image To Be Used In Calculations Of Answers
    eroded = cv2.erode(thresholded, np.ones((3, 3)), iterations=1)

    # Get Average Area
    areas = []
    # Get the external contours
    pap_cnts, _ = cv2.findContours(
        thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Check if there are no contours
    if (len(pap_cnts) == 0):
        print("No external contours found")

    # Get the bubbles contours
    pre_question_cnts = []
    for cnt in pap_cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        aspect_ratio = w/h
        peri = cv2.arcLength(cnt, True)
        ratio = 0.01
        approx = cv2.approxPolyDP(cnt, ratio*peri, True)
        curr_cnt_area = cv2.contourArea(cnt)
        if (aspect_ratio >= 0.8 and aspect_ratio <= 1.2 and len(approx) >= 4 and curr_cnt_area > 30 and curr_cnt_area > 1.5*peri):
            areas.append(curr_cnt_area)
            pre_question_cnts.append(cnt)

    # Check if there are no contours
    if (len(pre_question_cnts) == 0):
        print("No bubbles contours found")

    temp = paper.copy()
    cv2.drawContours(temp, pre_question_cnts, -1, (0, 255, 0), 5)

    # Get Only Bubbles
    bubble_area = np.median(areas)
    question_cnts_copy = []
    for i, area in enumerate(areas):
        if (abs(area-bubble_area) <= bubble_area*.3):
            question_cnts_copy.append(pre_question_cnts[i])
    pre_question_cnts = question_cnts_copy

    temp = paper.copy()
    cv2.drawContours(temp, pre_question_cnts, -1, (0, 255, 0), 5)

    if (len(pre_question_cnts)):
        # Sort the contours from top to bottom
        question_cnts, _ = imcnts.sort_contours(
            pre_question_cnts, method='top-to-bottom')

        # Detect the number of choices and the number of columns
        xs_set = np.array([])
        (_, __, bubble_width, ___) = cv2.boundingRect(pre_question_cnts[0])
        for cnt in question_cnts:
            (x, y, w, h) = cv2.boundingRect(cnt)
            xs_set = np.append(xs_set, x)
        xs_set = np.sort(xs_set)
        number_of_bubbles = 0
        number_of_xs = len(xs_set)
        number_of_columns = 1
        for i in range(1, number_of_xs):
            if (xs_set[i]-xs_set[i-1] >= 0.5*bubble_width and xs_set[i]-xs_set[i-1] <= 2*bubble_width):
                number_of_bubbles += 1
            elif (xs_set[i]-xs_set[i-1] > 2.5*bubble_width):
                number_of_columns += 1
        number_of_bubbles += number_of_columns
        number_of_choices = number_of_bubbles//number_of_columns
        print(number_of_columns, number_of_choices, number_of_bubbles)

    def detect_number_of_contours(cnts):
        (_, prev_y, ___, bubble_height) = cv2.boundingRect(cnts[0])
        # print("height",bubble_height)
        for i, cnt in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(cnt)
            if (abs(y-prev_y) > 0.4*bubble_height):
                return 1
        return 0

    number_of_questions = len(pre_question_cnts)//number_of_choices
    cut_row = number_of_questions*(number_of_choices+1)
    is_cut = 0
    temp = paper.copy()
    if (len(pre_question_cnts)):
        qs = 0
        # Get student answers
        answers = []

        temp_number_of_columns = number_of_columns
        # Iterate over each row
        i = 0
        print(len(question_cnts))
        while (i < len(question_cnts)):

            # detect number of contours in row
            if (not is_cut):
                is_cut = detect_number_of_contours(
                    question_cnts[i:i+temp_number_of_columns*number_of_choices])
                if (is_cut):
                    temp_number_of_columns -= 1
                cut_row = i
            number_of_conts = temp_number_of_columns*number_of_choices

            # Get all bubbles of the current row which has (number_of_columns) questions
            print('length of contours',len( question_cnts[i:i+number_of_conts]))
            curr_row_cnts, _ = imcnts.sort_contours(
                question_cnts[i:i+number_of_conts])
            


            # Iterate over each question
            for k in np.arange(0, len(curr_row_cnts), number_of_choices):

                # Current Question answers
                curr_ques_cnts = curr_row_cnts[k:k+number_of_choices]
                color1 = colors[qs % len(colors)]
                qs = qs+1
                cv2.drawContours(temp, curr_ques_cnts, -1, color1, 5)

                mask_ones = []
                bubbles = []
                for j, c in enumerate(curr_ques_cnts):

                    # Get the maximum shaded bubble
                    mask = np.zeros(thresholded.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    mask_ones.append(cv2.countNonZero(mask))
                    mask = cv2.bitwise_and(eroded, mask)
                    total = cv2.countNonZero(mask)
                    bubbles.append(total)

                mask_mean = np.mean(mask_ones)
                bubbles = np.array(bubbles)/mask_mean
                bubbled = np.argmax(bubbles)
                total = np.amax(bubbles)
                count_chosen = 0
                if (total > 0.7):
                    count_chosen = ((total-bubbles) <= 0.3).sum()
                else:
                    count_chosen = ((total-bubbles) <= 0.15).sum()
                final_ans = (ord('X')-ord('A')
                             ) if (count_chosen != 1) else bubbled
                answers.append(chr(final_ans+ord('A')))
            i += (temp_number_of_columns*number_of_choices)

    # Get Number Of Rows
    number_of_rows = 0
    x_sorted_conts, _ = imcnts.sort_contours(question_cnts)
    (prev_x, _, bubble_width, __) = cv2.boundingRect(x_sorted_conts[0])
    for i, cnt in enumerate(x_sorted_conts):
        (x, y, w, h) = cv2.boundingRect(cnt)
        if (abs(prev_x-x) >= 2.5*bubble_width):
            number_of_rows = i
            break
        elif i+1 == len(x_sorted_conts):
            number_of_rows = i+1
        prev_x = x
    number_of_rows = number_of_questions if not number_of_rows else number_of_rows//number_of_choices

    # Map The Given Answers To Real Ones
    cut_row = cut_row//(number_of_choices*number_of_columns)
    curr_cnt = 0
    final_answers = [0] * number_of_questions
    for i in range(0, number_of_rows):
        for j in range(0, number_of_columns-int(i >= cut_row and is_cut)):
            # print(j*number_of_rows+i+1,curr_cnt+1,int(i>=cut_row and cut_row!=number_of_rows-1))
            final_answers[j*number_of_rows+i] = answers[curr_cnt]
            curr_cnt += 1
    return final_answers, id

