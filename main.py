import cv2
import mediapipe as mp

# Initialize the Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe hands
    results = hands.process(frame_rgb)

    # Draw landmarks on the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i, landmark in enumerate(hand_landmarks.landmark):
                if i < 20:
                    x1 = int(landmark.x * frame.shape[1])
                    y1 = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x1, y1), 5, (0, 0, 255), -1)
                    landmark_next = hand_landmarks.landmark[i+1]
                    x2 = int(landmark_next.x * frame.shape[1])
                    y2 = int(landmark_next.y * frame.shape[0])
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Frame', frame)

    # Check for key press event
    key = cv2.waitKey(1)
    if key == 27:  # Check if the pressed key is ESC
        break

    # Check if the window is closed
    if cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()