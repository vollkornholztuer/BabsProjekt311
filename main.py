import cv2

from show import showImage
cap = cv2.VideoCapture(0)
showImage(cap)


cv2.destroyAllWindows() 