import pytesseract
import cv2
import numpy as np

def detact_digit_ocr(row,col):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    custom_config = '-c tessedit_char_whitelist=0123456789'

    img=cv2.imread('./contours/'+str(col)+'/'+str(row)+'.jpg')
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    ## make image gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ## make threshold on image
    ret, img = cv2.threshold(img, 127, 255, 0)
    img=np.invert(img)
    out = pytesseract.image_to_string(img ,lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    return out