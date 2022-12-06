import cv2

# sort left to right && bottom to top
def contour_sort(a, b):

    br_a = cv2.boundingRect(a)
    br_b = cv2.boundingRect(b)

    if abs(br_a[1] - br_b[1]) <= 15:
        return br_a[0] - br_b[0]

    return br_a[1] - br_b[1]