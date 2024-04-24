import cv2

cap = cv2.VideoCapture(0)
def showTracking(cap):
    while True:
        # Read the frame
        ret, frame = cap.read()

        cv2.imshow('Webcam Feed', frame)
        key = cv2.waitKey(1)
        if key == 27 :  # Check if the pressed key is ESC
            break

    cap.release()
    cv2.destroyAllWindows()

showTracking(cap)