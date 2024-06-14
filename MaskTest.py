import cv2
import numpy as np
import mediapipe as mp

def draw_white_circle(image_shape, hand_landmarks):
    # Create a black mask image with the same size as the input image
    mask = np.zeros(image_shape[:2], dtype=np.uint8)

    # Extract the coordinates of landmark 9
    landmark_9 = hand_landmarks.landmark[9]
    landmark_x = int(landmark_9.x * image_shape[1])
    landmark_y = int(landmark_9.y * image_shape[0])

    # Draw a white circle centered at landmark 9 with a radius of 20 pixels
    cv2.circle(mask, (landmark_x, landmark_y), 50, 255, -1)

    return mask

def show_webcam_with_painting():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=2,
                           min_detection_confidence=0.7,
                           min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create a black canvas for painting
    canvas = np.zeros((480, 640, 3), dtype=np.uint8)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = hands.process(frame_rgb)

        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Draw a white circle centered at landmark 9
                mask = draw_white_circle(frame.shape, hand_landmarks)

                # Set all pixels in the canvas that are hit by the circle to white
                canvas[mask == 255] = [255, 255, 255]

        # Display the resulting frame
        cv2.imshow('Webcam Feed', frame)
        cv2.imshow('Canvas', canvas)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    show_webcam_with_painting()