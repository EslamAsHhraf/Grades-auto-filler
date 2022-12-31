import pytesseract
import cv2
import numpy as np

def detact_digit_ocr(row,col):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    custom_config = '--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789'

    img=cv2.imread('./contours/'+str(col)+'/'+str(row)+'.jpg')
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img=np.invert(img)
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    ## make threshold on image

    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, sharpen_kernel)
    out = pytesseract.image_to_string(img ,lang='eng',config=custom_config)
    return out