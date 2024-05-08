import cv2

cap = cv2.VideoCapture(0)
def showImage(cap):
    

    while True:
        ret, frame = cap.read()
        
        frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        
        # show images 
        cv2.imshow('Input', frame)
        #cv2.imshow("second Input", frame)
        
        c = cv2.waitKey(1)
        if c == 27:
            break
        
def showTwoImage(cap1, cap2):
        
    
    while True:
        ret, frame1 = cap1.read()
        ret, frame2 = cap2.read()
        frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        
        # show images 
        cv2.imshow('Input', frame1)
        cv2.imshow("second Input", frame2)
        
        c = cv2.waitKey(1)
        if c == 27:
            break