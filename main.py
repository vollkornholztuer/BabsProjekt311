import cv2
import mediapipe as mp
import Hand
import numpy as np
from enum import Enum

# program states
class State(Enum):
    IDLE = 1
    IN_USE = 2
    SAVE_SCREENSHOT = 3


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

# Stuff for waving gesture
waving_recognized = False
x_hand_offset_arr = np.zeros(0) # for wave detection

# show lines
show = True

while True:
    ret, frame = cap.read() # Read the frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # frame to RGB

    results = hands.process(frame_rgb) # Mediapipe detect hands
    # Draw landmarks
    x_hand_offset_arr = Hand.landmarks(frame, results, show, x_hand_offset_arr)
            
    # frame = cv2.resize(frame, (1280, 720)) // custom resolution
    cv2.imshow('Webcam Feed', frame)

    # Check if the user pressed ESC / closed the window / is mean and break the loop
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty('Webcam Feed', cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        break

cap.release()
cv2.destroyAllWindows()