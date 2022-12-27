import cv2
import numpy as np
import math
from commonfunctions import *
from scipy.ndimage import interpolation as inter
import os

def biggest_contour(contours):
    biggest = np.array([])
    biggest2 = np.array([])
    max_area = 0
    max_area2 = 0
    for i in contours:
        area = cv2.contourArea(i)
        peri = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.1 * peri, True)
        if area > max_area and len(approx) == 4:
            biggest = approx
            max_area = area
    return biggest

def Image_Orientation(img_original):
    img =img_original.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 20, 30, 30)

    # grad_x = cv2.Sobel(gray, -1, 1, 0)
    # # Gradient-Y

    # grad_y = cv2.Sobel(gray, -1, 0, 1)


    # abs_grad_x = cv2.convertScaleAbs(grad_x)
    # abs_grad_y = cv2.convertScaleAbs(grad_y)


    # grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    edged = cv2.Canny(gray, 20, 120)
    edged = cv2.dilate(edged.copy(), None, 2)
#     show_images([img, gray, edged], ['original', 'gray','edged'])




    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
#     for c in contours:
#         cv2.drawContours(img, [c], -1, (0, 255, 0), 3) #######################################
#     x, y, w, h = cv2.boundingRect(c)
#     new_img = img[y:y+h, x:x+w]
    
#     show_images([new_img])

    biggest = biggest_contour(contours[2:10])
    if(biggest.size!=8):
        biggest = biggest_contour(contours[0:1])
    
    points = biggest.reshape(4, 2)
    input_points = np.zeros((4, 2), dtype="float32")


    #Biggest Contour Points
    points_sum = points.sum(axis=1)

    top_left = points[np.argmin(points_sum)]
    bottom_right = points[np.argmax(points_sum)]

    points_diff = np.diff(points, axis=1)
    top_right = points[np.argmin(points_diff)]
    bottom_left = points[np.argmax(points_diff)]


    #Image Dimensions
    bottom_width = np.sqrt(pow((bottom_right[0] - bottom_left[0]), 2) + (pow((bottom_right[1] - bottom_left[1]), 2)))
    top_width = np.sqrt(pow((top_right[0] - top_left[0]), 2) + (pow((top_right[1] - top_left[1]), 2)))
    right_height = np.sqrt(pow((top_right[0] - bottom_right[0]), 2) + (pow((top_right[1] - bottom_right[1]), 2)))
    left_height = np.sqrt(pow((top_left[0] - bottom_left[0]), 2) + (pow((top_left[1] - bottom_left[1]), 2)))


    # Output image size
    width = max(int(bottom_width), int(top_width))
    height = max(int(right_height), int(left_height))
    print(width)
    print(height)
    # Points with new Coordinates 
    converted_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Warping
    arr = np.float32([top_left, top_right, bottom_left, bottom_right])
    matrix = cv2.getPerspectiveTransform(arr, converted_points)
    img_output = cv2.warpPerspective(img_original, matrix, (width, height))

#     show_images([img_original, gray, edged, img], ['original','gray','edged','contours'])


#     show_images([img_output], ['Warped'])

    cv2.imwrite('Image_Orientation.jpg', img_output)
    return img_output