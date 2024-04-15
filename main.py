import cv2

# Create a VideoCapture object to access the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read the current frame from the webcam
    ret, frame = cap.read()

    # Display the frame in a window
    cv2.imshow('Webcam Feed', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()