import cv2
import mediapipe as mp
import numpy as np

import Hand

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

# Stuff for waving gesture
x_hand_offset_arr = np.zeros(0) # for 90 frames of x hand offset
waving_recognized = False

def detect_pinch(landmarks_list, hand_size):
    if Hand.normalized_distance(landmarks_list[4], landmarks_list[8], hand_size) < 0.25 and not Hand.detect_is_finger_down(landmarks_list, hand_size)['index_down']:
        # calc middle point between both tips
        dragging_point = ((landmarks_list[4][0] + landmarks_list[8][0]) // 2, (landmarks_list[4][1] + landmarks_list[8][1]) // 2)
        cv2.circle(frame, dragging_point, 10, (255, 255, 255), 2)  # Visual feedback for pinching
        return True
    else:
        return False
    
def draw_lines(i):
    if show:
        cv2.circle(frame, (x1, y1), 5, (0, 0, 255), -1)
                    
        cv2.putText(frame, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if i%4 != 0:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # Draw a line between the landmarks
            
            if i == 1 or i == 5 or i == 17:
                x0 = int(hand_landmarks.landmark[0].x * frame.shape[1])
                y0 = int(hand_landmarks.landmark[0].y * frame.shape[0])
                cv2.line(frame, (x1, y1), (x0, y0), (0, 255, 0), 2)
                

# Pinch state
is_pinching = False
# dragging_point = None // what do i want to drag and how

# show lines
show = True

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
                    # z1 = (landmark.z * frame.shape[2])
                    
                    landmarks_list.append((x1, y1))
                    
                    if i < 20:
                        landmark_next = hand_landmarks.landmark[i+1] # Get the next landmark
                    
                    x2 = int(landmark_next.x * frame.shape[1])
                    y2 = int(landmark_next.y * frame.shape[0])
                    # z2 = int(landmark_next.z * frame.shape[2])

                    draw_lines(i)
                    

            # if show:
            #     # 13 and 17
            #     cv2.line(frame, (landmarks_list[13][0], landmarks_list[13][1]), (landmarks_list[17][0], landmarks_list[17][1]), (0, 255, 0), 2)
            #     # 5 and 9
            #     cv2.line(frame, (landmarks_list[5][0], landmarks_list[5][1]), (landmarks_list[9][0], landmarks_list[9][1]), (0, 255, 0), 2)
            #     # 9 and 13
            #     cv2.line(frame, (landmarks_list[9][0], landmarks_list[9][1]), (landmarks_list[13][0], landmarks_list[13][1]), (0, 255, 0), 2)

            palm_center = Hand.calculate_palm_points(landmarks_list)
            # cv2.circle(frame, (int(palm_center[0]), int(palm_center[1])), 15, (255, 255, 255), 2)  # Visual feedback for palm center

            hand_size = Hand.calculate_hand_size(landmarks_list, palm_center)

            is_pinching = detect_pinch(landmarks_list, hand_size)
            handPositionX = Hand.detect_open_palm(landmarks_list, hand_size)
            
            if handPositionX != 0:
                x_hand_offset_arr = np.append(x_hand_offset_arr, handPositionX)
                print(x_hand_offset_arr)
                
            if len(x_hand_offset_arr) > 45:
                x_hand_offset_arr = np.zeros(0) # reset array
                
            waving_recognized = Hand.detect_wave(x_hand_offset_arr)
            if waving_recognized:
                print("WAVING GESTURE RECOGNIZED")
                x_hand_offset_arr = np.zeros(0)
                
            key = cv2.waitKey(1)
            if key == ord('p'):
                Hand.printHandCoords(landmarks_list, hand_size)

            
    # frame = cv2.resize(frame, (1280, 720)) // custom resolution
    
    cv2.imshow('Webcam Feed', frame)

    # Check if the user pressed ESC / closed the window / is mean and break the loop
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty('Webcam Feed', cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        break

cap.release()
cv2.destroyAllWindows()