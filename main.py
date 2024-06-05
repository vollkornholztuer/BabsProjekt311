import cv2
import mediapipe as mp
import Hand
import numpy as np
from enum import Enum
import MoveVideoBlocksTest as mvbt
import helper as hlp
import State

# program states
class MainState(Enum):
    START = 1
    IN_USE = 2
    CREDITS = 3

current_state = MainState.START

puzzle_started = False
puzzle_diff = State.PuzzleDifficulty.NONE

show = True # show lines
changes_to_videoblock_order = []
selected_square = None
pinch_active = False 

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)
window_name = 'Webcam Feed'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Load GIF and corresponding stuff
wave_gif = 'images\waving-hand-cropped.gif'
wave_gif_frames = hlp.resize_and_load_gif(wave_gif)
wave_gif_length = len(wave_gif_frames)
frame_index = 0

pinch_image = cv2.imread('images\pinch.png')
credits_image = cv2.imread('images\credits.jpg')

while True:
    ret, frame = cap.read() # Read the frame
    frame = cv2.flip(frame, 1) # Flip the frame horizontally
    original_frame = frame.copy() # original frame for win-condition
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # frame to RGB

    results = hands.process(frame_rgb) # Mediapipe detect hands

    # Create a mask for hand landmarks
    hand_mask = np.zeros_like(frame)

    # Draw landmarks and ger list
    landmarks_list_each_hand = Hand.landmarks(hand_mask, results, show)


    ##### STATE START #####
    if current_state == MainState.START:
        for landmarks_list in landmarks_list_each_hand:
            if Hand.detect_wave(landmarks_list):
                current_state = MainState.IN_USE
                pass

        combined_frame = cv2.addWeighted(frame, 1, hand_mask, 2, 0)
        
        # Add GIF as overlay
        wave_gif_frame = wave_gif_frames[frame_index % wave_gif_length]
        combined_frame = hlp.overlay_gif_on_frame(combined_frame, wave_gif_frame, position=(50, 50))
        
        cv2.imshow(window_name, combined_frame)


    ##### STATE IN USE #####
    elif current_state == MainState.IN_USE:
        puzzle_started = True
        
        # TODO: Choose difficulty of puzzle
        difficultyChoice = 0 # 0 = easy, 1 = normal, 2 = hard
        
        match difficultyChoice:
            case 0:
                puzzle_diff = State.PuzzleDifficulty.EASY
            case 1:
                puzzle_diff = State.PuzzleDifficulty.NORMAL
            case 2:
                puzzle_diff = State.PuzzleDifficulty.HARD
                
        frame = hlp.indicator_image(frame, pinch_image, width)
        shuffleFrame = mvbt.split_frame(frame, height, width, puzzle_diff)
        
        shuffleFrame_comparison = mvbt.split_frame(original_frame, height, width, puzzle_diff)
        stitchFrame_comparison = mvbt.stitchBlocks(shuffleFrame_comparison, changes_to_videoblock_order, puzzle_diff)
        
        stitchFrame = mvbt.stitchBlocks(shuffleFrame, changes_to_videoblock_order, puzzle_diff)

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
                elif selected_square == square_index: # Deselect square
                    pinch_active = True
                    selected_square = None
                    print("Square 1 deselected")
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
        
        images_compared = mvbt.compareImages(original_frame, stitchFrame_comparison)
        
        if images_compared:
            print("YOU WIN")
            current_state = MainState.CREDITS
    
    
    ##### STATE CREDITS ######
    elif current_state == MainState.CREDITS:
        cv2.imshow(window_name, credits_image)

    frame_index += 1

    # Check if the user pressed ESC / closed the window
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        print('Pressed ESC or closed the window')
        break
    elif key == 99:
        print('State switched to credits')
        current_state = MainState.CREDITS

cap.release()
cv2.destroyAllWindows()