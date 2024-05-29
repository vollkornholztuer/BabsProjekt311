import cv2
import mediapipe as mp
import Hand
import numpy as np
from enum import Enum
import MoveVideoBlocksTest as mvbt
import threading

# program states
class State(Enum):
    IDLE = 1
    IN_USE = 2
    SAVE_SCREENSHOT = 3

changes_to_videoblock_order = []

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

window_name = 'Webcam Feed'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WINDOW_AUTOSIZE, cv2.WINDOW_NORMAL)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# show lines
show = True

def async_input_videoblock_changes():
    while True:
        index_to_swap1 = input("Enter index to swap 1: ")
        index_to_swap2 = input("Enter index to swap 2: ")
        swap = (int(index_to_swap1), int(index_to_swap2))
        
        changes_to_videoblock_order.append(swap)

# Creating threads
thread2 = threading.Thread(target=async_input_videoblock_changes)
thread2.daemon = True
thread2.start()


while True:
    ret, frame = cap.read() # Read the frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # frame to RGB

    results = hands.process(frame_rgb) # Mediapipe detect hands

    # Create a mask for hand landmarks
    hand_mask = np.zeros_like(frame)

    # Draw landmarks
    Hand.landmarks(hand_mask, results, show)

    shuffleFrame = mvbt.split_frame(frame, height, width)
    stitchFrame = mvbt.stitchBlocks(shuffleFrame, changes_to_videoblock_order)

    combined_frame = cv2.addWeighted(stitchFrame, 1, hand_mask, 2, 0)

    cv2.imshow(window_name, combined_frame)

    # Check if the user pressed ESC / closed the window / is mean and break the loop
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        break

cap.release()
cv2.destroyAllWindows()