import pytesseract

def detact_digit_ocr(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    custom_config = '-c tessedit_char_whitelist=0123456789'
    out = pytesseract.image_to_string(img ,lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    return out