import cv2
import numpy as np
from skimage.morphology import skeletonize
from imutils import contours as imcnts
import xlwt

def detact_square(img):
    ret, img = cv2.threshold(img, 127, 255, 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=np.invert(img)

    kernel_length = np.array(img).shape[1]//20
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    verticle_lines_img = cv2.erode(img, verticle_kernel, iterations=2)
    verticle_lines_img = cv2.dilate(verticle_lines_img, verticle_kernel, iterations=5)
  
    lines_ver = cv2.HoughLinesP(verticle_lines_img,2,np.pi/180,30,minLineLength=5,maxLineGap=10)
    if not(lines_ver is None):
        for line  in lines_ver:
            for x1, y1, x2, y2 in line:

                 verticle_lines_img=cv2.line(verticle_lines_img,(x1,0),(x2,verticle_lines_img.shape[0]),(255,255,255),1)
  
    horizontal_lines_img = cv2.erode(img, hori_kernel, iterations=2)
    horizontal_lines_img = cv2.dilate(horizontal_lines_img, hori_kernel, iterations=3)
    
   
    lines_hor = cv2.HoughLinesP(horizontal_lines_img,2,np.pi/180,35,minLineLength=5,maxLineGap=10)

    if not(lines_hor is None):
        for line  in lines_hor:
            for x1, y1, x2, y2 in line:

                horizontal_lines_img=cv2.line(horizontal_lines_img,(0,y1),(horizontal_lines_img.shape[1],y2),(255,255,255),1)
    
    img_final_bin=cv2.bitwise_and(verticle_lines_img, horizontal_lines_img)
    img_final_bin = cv2.dilate(img_final_bin, hori_kernel, iterations=3)
    
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    img_final_bin = cv2.dilate(img_final_bin, kernel, iterations=2)
    
    cnt = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    if(len(cnt)==4):
        
        return 0
    else:
        return -1

def deatact_Vertical_lines(img):
    ret, img = cv2.threshold(img, 127, 255, 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=np.invert(img)
    kernel_length = np.array(img).shape[1]//20
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))
    img = cv2.erode(img, kernel, iterations=1)
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    horizontal_lines_img = cv2.erode(img, hori_kernel, iterations=2)
    horizontal_lines_img = cv2.dilate(horizontal_lines_img, hori_kernel, iterations=6)
    
    
    lines_hor = cv2.HoughLinesP(horizontal_lines_img,2,np.pi/180,40,minLineLength=5,maxLineGap=10)
    if not(lines_hor is None):
        return -1
    contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    if(len(contours) == 0):
        return -1
    return len(contours)


def deatact_Horizontal_lines(img):
    ret, img = cv2.threshold(img, 127, 255, 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=np.invert(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 2))
    img = cv2.erode(img, kernel, iterations=2)
    kernel_length = np.array(img).shape[1]//20
  
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    
    verticle_lines_img = cv2.erode(img, verticle_kernel, iterations=2)
    verticle_lines_img = cv2.dilate(verticle_lines_img, verticle_kernel, iterations=6)
    lines_ver = cv2.HoughLinesP(verticle_lines_img,2,np.pi/180,40,minLineLength=10,maxLineGap=10)
    if not(lines_ver is None):
        return -1
    contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    number=len(contours)
  
    if(number == 1):
        x1, y1, w1, h1 = cv2.boundingRect(contours[0])
        if(w1> img.shape[1]//2):
            return 5-number
        else:
            return 0
    else:
        return 5-number
    
def deatact_Empty_cell(img):
    ret, img = cv2.threshold(img, 127, 255, 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=np.invert(img)
  
   
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img = cv2.erode(img, kernel, iterations=2)

    contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    number=len(contours)
    if(number == 0):
        return ''
    else:
        return -1

colors=[(255,0,0)
,(0,255,0)
,(0,0,255)
,(255,255,192)
,(0,128,128)
,(255,215,0)
,(255,0,0)
,(0,255,0)
,(0,0,255)
,(0,255,0)
,(255,0,0)

,(225,255,128)
,(128,0,0)
,(128,128,0)
,(0,128,0)
,(128,0,128)

,(0,0,128)
,(255,215,0)]


def filter_squares_from_check_mark(img):
    pap_cnts,_=cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    check_mark_cnts,_=imcnts.sort_contours(pap_cnts,method='top-to-bottom')
    cnt = check_mark_cnts[0]
    peri = cv2.arcLength(cnt, True)
    check_mark_cnt_area=cv2.contourArea(cnt)
    return check_mark_cnt_area>1.5*peri

def detect_check_mark(img):
    temp=np.zeros_like(img)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
             cv2.THRESH_BINARY_INV, 51, 15)
 
    
    img_copy=img.copy()
    img=skeletonize(img,method='lee')
    
    # Filter Question Mark
    is_question_mark = cv2.HoughLinesP(img,1,np.pi/300,threshold=25,maxLineGap=15)
    if(is_question_mark is None):
        return False
    
    # Filter Squares
    img_copy=cv2.dilate(img_copy, np.ones((5,5)), iterations=1)
    img_copy=skeletonize(img_copy,method='lee')
    if(filter_squares_from_check_mark(img) or filter_squares_from_check_mark(img_copy)):
    
        return False
    
    lines = cv2.HoughLinesP(img,1,np.pi/300,threshold=4,maxLineGap=20)
    slopes=[]
    for index,line  in enumerate(lines):
        for x1, y1, x2, y2 in line:
            slopes.append((y2-y1)/(x2-x1))
            temp=cv2.line(temp,(x1,y1),(x2,y2),colors[index%len(colors)],1)
    slopes=np.sort(np.degrees(np.arctan(slopes)))
    ver_error=(slopes>=-90) & (slopes<=-83)
    slopes[ver_error]*=-1
    pos_ang=slopes[slopes>0]
    neg_ang=np.abs(slopes[slopes<0])


    # Filter Check Mark
    if(not len(pos_ang) or not len(neg_ang)):
        if(len(slopes)<2):
            #print(f'{num} Failed With Filter Check Marks')
            return False
        right_line = np.amax(slopes)
        left_line = np.amin(slopes)
        diff_ang=right_line-left_line 
        return diff_ang>30 and diff_ang<100
    else:
        right_line = np.mean(neg_ang) if len(neg_ang)<=2 else np.median(neg_ang) 
        left_line = np.mean(pos_ang) if len(pos_ang)<=2 else np.median(pos_ang)
        diff_ang=left_line+right_line 
        return diff_ang>80 and diff_ang<150
    
def detect_question_mark(img):
    img = cv2.bilateralFilter(img, 20, 30, 30)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img= cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
             cv2.THRESH_BINARY_INV, 51, 15)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img = cv2.erode(img, kernel, iterations=2)
    img=skeletonize(img,method='lee')
    
    kernel = np.ones((4,4),np.uint8)
    kernel2 = np.ones((1,1),np.uint8)
    rows = img.shape[0]


    lines_ver = cv2.HoughLinesP(img,1,np.pi/300,threshold=25,maxLineGap=15)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, rows/8,
                               param1=30, param2= 10,
                               minRadius=10, maxRadius=20)

    if circles is None:
        rows+=1
    else:
        circles = np.uint16(np.around(circles))
        
        pap_cnts,_=cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        question_cnts,_=imcnts.sort_contours(pap_cnts,method='top-to-bottom')
        cnt = question_cnts[0]
        (x,y,w,h)=cv2.boundingRect(cnt)
        aspect_ratio=w/h
        peri = cv2.arcLength(cnt, True)
        if(cv2.contourArea(cnt)<1.5*peri):
            return True
        
    return False


def detact_symbols(sheet,row,col):
    img=cv2.imread('./contours/'+str(col)+'/'+str(row)+'.jpg')
    result=deatact_Empty_cell(img=img)
    if(result!=-1):
        sheet.write(row, col,'')
        return
    result=detact_square(img=img)
    if(result!=-1):
        sheet.write(row, col,'square '+ str(result))
        return
    result=detect_question_mark(img=img)
    if(result):
        cell_format = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
        sheet.write(row, col,'?')
        return
    result=detect_check_mark(img=img)
    if(result):
       
        sheet.write(row, col,5)
        return
    result=deatact_Vertical_lines(img=img)
    if(result!=-1):
        sheet.write(row, col,'Vertical_lines '+ str(result))
        return
    result=deatact_Horizontal_lines(img=img)
    if(result!=-1):
        sheet.write(row, col,'Horizontal_lines '+ str(result))
        return
  
    sheet.write(row, col,'undefined')