import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    ret, frame = cap.read()


    # frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    # Mediapipe hands
    results = hands.process(frame_rgb)


    # Draw landmarks
    if results.multi_hand_landmarks: # Check if there are hands detected
        for hand_landmarks in results.multi_hand_landmarks: # Iterate through the hands
            for i, landmark in enumerate(hand_landmarks.landmark): # Iterate through the landmarks
                if i < 20: 
                    x1 = int(landmark.x * frame.shape[1]) 
                    y1 = int(landmark.y * frame.shape[0])

                    if i == 0: # Check if the landmark is the wrist
                        cv2.circle(frame, (x1, y1), 5, (255, 0, 0), -1)
                    else:
                        cv2.circle(frame, (x1, y1), 5, (0, 0, 255), -1)
                        
                    landmark_next = hand_landmarks.landmark[i+1] # Get the next landmark
                    x2 = int(landmark_next.x * frame.shape[1])
                    y2 = int(landmark_next.y * frame.shape[0])
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # Draw a line between the landmarks
                    if i == 17:
                        x0 = int(hand_landmarks.landmark[0].x * frame.shape[1])
                        y0 = int(hand_landmarks.landmark[0].y * frame.shape[0])
                        cv2.line(frame, (x1, y1), (x0, y0), (0, 255, 0), 2)
                    if i == 5:
                        x0 = int(hand_landmarks.landmark[0].x * frame.shape[1])
                        y0 = int(hand_landmarks.landmark[0].y * frame.shape[0])
                        cv2.line(frame, (x1, y1), (x0, y0), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)


    # Check if the user pressed ESC and break the loop
    key = cv2.waitKey(1)
    if key == 27:  # Check if the pressed key is ESC
        break


    # Check if the user closed the window and break the loop
    if cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
        break


cap.release()
cv2.destroyAllWindows()