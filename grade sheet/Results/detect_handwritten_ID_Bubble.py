import cv2
import numpy as np
from crop_image import *
import imutils
from imutils import contours as imcnts
from bubble_sheet_answer import *
from paper_extraction import *
from crop_image import *
import pickle
import statistics
from crop_image import *


def extract_hog_features(img):

    win_size = (28, 28)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)

    block_size = (block_size_in_cells[1] * cell_size[1],
                  block_size_in_cells[0] * cell_size[0])
    block_stride = (cell_size[1], cell_size[0])
    nbins = 9  # Number of orientation bins
    hog = cv2.HOGDescriptor(win_size, block_size,
                            block_stride, cell_size, nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h


def extract_the_paper_from_image_ID(image):
    paper = None
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if (len(contours) > 0):
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        paper_contour = None
        paper = image
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            ratio = 0.01
            approx = cv2.approxPolyDP(cnt, ratio*peri, True)
            if (len(approx) == 4 and cv2.contourArea(cnt) > 0.2*image.shape[0]*image.shape[1]):
                paper_contour = approx
                paper = four_point_transform(
                    image, paper_contour.reshape(4, 2))
            else:
                break
    [intX, intY, intW, intH] = cv2.boundingRect(paper)
    paper = paper[intY+2:intY+intH-2, intX+2:intX+intW-2]
    return paper


def classifier_algorithm(myc, median_width, image, loaded_svc, loaded_knn, loaded_rf, loaded_lr):
    ID_weights = [1, 7, 1, 1, 2, 1, 1, 22, 4, 1]
    strFinalString = ""
    classifiers_respond = np.zeros(10)

    [intX, intY, intW, intH] = cv2.boundingRect(myc)
    imgROI = image[intY:intY+intH, intX:intX+intW]

    if (cv2.contourArea(myc)):
        imgROIResized = cv2.resize(imgROI, (28, 28), cv2.INTER_NEAREST)

        finalResized = imgROIResized.reshape((-1, 1))

        # EXTRACTING FEATURES
        hog_of_img = np.asarray(extract_hog_features(imgROIResized))
        hog_of_img = hog_of_img.reshape(1, -1)
        knn_value = loaded_knn.predict(hog_of_img)
        rf_value = loaded_rf.predict(hog_of_img)
        svc_value = loaded_svc.predict(hog_of_img)
        lr_value = loaded_lr.predict(hog_of_img)
        classifiers_respond[int(knn_value)] = classifiers_respond[int(
            knn_value)] + ID_weights[int(knn_value)]
        classifiers_respond[int(rf_value)] = classifiers_respond[int(
            rf_value)] + ID_weights[int(rf_value)]
        classifiers_respond[int(svc_value)] = classifiers_respond[int(
            svc_value)] + ID_weights[int(svc_value)]
        classifiers_respond[int(lr_value)] = classifiers_respond[int(
            lr_value)] + ID_weights[int(lr_value)]
        final_value = str(np.argmax(classifiers_respond))

        tmpString = str(int(final_value))
        strFinalString = strFinalString + tmpString
    return strFinalString


def detect_id(img, loaded_svc, loaded_knn, loaded_rf, loaded_lr):
    # PRE-PROCESSING
    bf = cv2.bilateralFilter(img, 50, 100, 100)  # to remove noise
    imgGray = cv2.cvtColor(bf, cv2.COLOR_BGR2GRAY)

    th = cv2.adaptiveThreshold(
        imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 3)
#     th= cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  cv2.THRESH_BINARY, 51, 12)
    th = np.invert(th)

    imgDigit = th

    strFinalString = ""
    imgDigit = extract_the_paper_from_image_ID(imgDigit)
    imgDigit = cv2.dilate(imgDigit, np.ones((2, 2)), iterations=1)

    width_sum = []
    cntr, h = cv2.findContours(
        imgDigit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(cntr))
    for cnt in cntr:
        [intX, intY, intW, intH] = cv2.boundingRect(cnt)
        if (intW > 5):
            width_sum = np.append(width_sum, [intW])

    median_width = statistics.median(width_sum)
    cntr, _ = imcnts.sort_contours(cntr, method='left-to-right')
    for myc in cntr:
        [intX, intY, intW, intH] = cv2.boundingRect(myc)
        if (intH > 15 and intW*intH < 0.5*imgDigit.shape[0]*imgDigit.shape[1]):
            strFinalString = strFinalString + classifier_algorithm(
                myc, median_width, imgDigit, loaded_svc, loaded_knn, loaded_rf, loaded_lr)
    return strFinalString
