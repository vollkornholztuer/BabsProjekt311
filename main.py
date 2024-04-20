import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

# todo:
# - norm threshold so that distance to the cam doesnt matter!!!!

# ingertips for clarity
# middle_tip = landmarks_list[12]
# wrist = landmarks_list[0]
# pinky_tip = landmarks_list[20]
# ring_tip = landmarks_list[16]
# thumb_tip = landmarks_list[4]
# index_tip = landmarks_list[8]

# Function to calculate distance
def calculate_distance(p1, p2):
    # p = x, y of landmark
    # sqrt((x2 - x1)^2 + (y2 - y1)^2) distance between 2 points
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def detect_is_finger_down(landmarks_list):
    finger_status = {
        'thumb_down': calculate_distance(landmarks_list[4], landmarks_list[0]) < 200,
        'index_down': calculate_distance(landmarks_list[8], landmarks_list[0]) < 200,
        'middle_down': calculate_distance(landmarks_list[12], landmarks_list[0]) < 300,
        'ring_down': calculate_distance(landmarks_list[16], landmarks_list[0]) < 200,
        'pinky_down': calculate_distance(landmarks_list[20], landmarks_list[0]) < 200
    }
    return finger_status

def detect_pinch(landmarks_list):
    if calculate_distance(landmarks_list[4], landmarks_list[8]) < 100 and not detect_is_finger_down(landmarks_list)['thumb_down'] and not detect_is_finger_down(landmarks_list)['index_down']:  # Threshold for pinch
        is_pinching = True
        # calc middle point between both tips
        dragging_point = ((landmarks_list[4][0] + landmarks_list[8][0]) // 2, (landmarks_list[4][1] + landmarks_list[8][1]) // 2)
        cv2.circle(frame, dragging_point, 10, (0, 0, 0), 2)  # Visual feedback for pinching
    else:
        is_pinching = False

# Pinch state
is_pinching = False
# dragging_point = None // what do i want to drag and how

# don't be mean
fu = False

while True:
    # Read the frame
    ret, frame = cap.read()


    # frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # Mediapipe hands
    results = hands.process(frame_rgb)

    # Draw landmarks
    if results.multi_hand_landmarks: # Check if there are hands detected
        for hand_landmarks in results.multi_hand_landmarks: # Iterate through the hands
            landmarks_list = []
            for i, landmark in enumerate(hand_landmarks.landmark): # Iterate through the landmarks
                if i <= 20: 
                    x1 = int(landmark.x * frame.shape[1]) 
                    y1 = int(landmark.y * frame.shape[0])
                    
                    landmarks_list.append((x1, y1))
                    
                    cv2.circle(frame, (x1, y1), 5, (0, 0, 255), -1)
                    
                    cv2.putText(frame, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    if i < 20:
                        landmark_next = hand_landmarks.landmark[i+1] # Get the next landmark
                    
                    x2 = int(landmark_next.x * frame.shape[1])
                    y2 = int(landmark_next.y * frame.shape[0])
                    
                    if i%4 != 0:
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # Draw a line between the landmarks
                        
                    if i == 1 or i == 5 or i == 17:
                        x0 = int(hand_landmarks.landmark[0].x * frame.shape[1])
                        y0 = int(hand_landmarks.landmark[0].y * frame.shape[0])
                        cv2.line(frame, (x1, y1), (x0, y0), (0, 255, 0), 2)

            # 13 and 17
            cv2.line(frame, (landmarks_list[13][0], landmarks_list[13][1]), (landmarks_list[17][0], landmarks_list[17][1]), (0, 255, 0), 2)
            # 5 and 9
            cv2.line(frame, (landmarks_list[5][0], landmarks_list[5][1]), (landmarks_list[9][0], landmarks_list[9][1]), (0, 255, 0), 2)
            # 9 and 13
            cv2.line(frame, (landmarks_list[9][0], landmarks_list[9][1]), (landmarks_list[13][0], landmarks_list[13][1]), (0, 255, 0), 2)

            detect_pinch(landmarks_list)

            if calculate_distance(landmarks_list[12], landmarks_list[0]) > 200 and detect_is_finger_down(landmarks_list)['pinky_down'] and detect_is_finger_down(landmarks_list)['ring_down'] and detect_is_finger_down(landmarks_list)['index_down']:
                fu = True


    # frame = cv2.resize(frame, (1280, 720)) // custom resolution
    
    cv2.imshow('Webcam Feed', frame)


    # Check if the user pressed ESC / closed the window / is mean and break the loop
    key = cv2.waitKey(1)
    if key == 27 or fu == True or cv2.getWindowProperty('Webcam Feed', cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        break


cap.release()
cv2.destroyAllWindows()