import cv2
import mediapipe as mp
import Hand
import numpy as np
from enum import Enum
import MoveVideoBlocksTest as mvbt
import helper as hlp

# program states
class State(Enum):
    START = 1
    IN_USE = 2
    CREDITS = 3

current_state = State.START
puzzle_started = False
show = True # show lines
changes_to_videoblock_order = []
selected_square = None
pinch_active = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

window_name = 'Webcam Feed'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WINDOW_AUTOSIZE, cv2.WINDOW_NORMAL)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read() # Read the frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # frame to RGB

    results = hands.process(frame_rgb) # Mediapipe detect hands

    # Create a mask for hand landmarks
    hand_mask = np.zeros_like(frame)

    # Draw landmarks and ger list
    landmarks_list_each_hand = Hand.landmarks(hand_mask, results, show)

    if current_state == State.START:
        for landmarks_list in landmarks_list_each_hand:
            if Hand.detect_wave(landmarks_list):
                current_state = State.IN_USE

        combined_frame = cv2.addWeighted(frame, 1, hand_mask, 2, 0)
        cv2.imshow(window_name, combined_frame)

    elif current_state == State.IN_USE:
        puzzle_started = True

        shuffleFrame = mvbt.split_frame(frame, height, width)
        stitchFrame = mvbt.stitchBlocks(shuffleFrame, changes_to_videoblock_order)

        combined_frame = cv2.addWeighted(stitchFrame, 1, hand_mask, 2, 0)

        for landmarks_list in landmarks_list_each_hand:
            pinch_detected, dragging_point = Hand.detect_pinch(landmarks_list)
            if pinch_detected and not pinch_active:
                cv2.circle(combined_frame, dragging_point, 10, (255, 255, 255), 2)  # Visual feedback for pinching
                square_index = hlp.get_square_index(dragging_point, height, width)
                if selected_square is None:
                    pinch_active = True
                    selected_square = square_index
                    print("Square 1 selected")
                # add deselect?? if selected_square == square_square
                elif selected_square != square_index:
                    pinch_active = True
                    # Swap the squares
                    changes_to_videoblock_order.append((square_index, selected_square))
                    print("Swapped squre 1 with square 2")
                    selected_square = None  # Reset
                    
            # reset this biatch
            if not pinch_detected:
                pinch_active = False
        
        # Indicator
        if selected_square is not None:
            hlp.highlight_square(combined_frame, selected_square, height, width)

        cv2.imshow(window_name, combined_frame)

    # Check if the user pressed ESC / closed the window
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        break

cap.release()
cv2.destroyAllWindows()