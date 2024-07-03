import cv2
import mediapipe as mp
import numpy as np
from enum import Enum
import random
import time
import Hand
import MoveVideoBlocksTest as mvbt
import helper as hlp
import State
import Buttons

# program states
class MainState(Enum):
    PRE_START = 0
    START = 1
    IN_USE = 2
    CREDITS = 3
    DIFFICULTY_SELECT = 4

current_state = MainState.PRE_START

puzzle_started = False
puzzle_diff = State.PuzzleDifficulty.NONE

show = False # show lines
changes_to_videoblock_order = []
selected_square = None
pinch_active = False
difficultyChoice = 0 # 0 = no choice, 1 = normal, 2 = hard, 3 = impossible

hand_x_old, hand_y_old = 0, 0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8)

print("Kamera 1 wird initialisiert")
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Kamera 1 konnte nicht initialisiert werden \n Kamera 0 wird initialisiert")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

window_name = 'Webcam Feed'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # camera dimensions
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

hand_x, hand_y = random.randint(0, width - 1), random.randint(0, height - 1) # random position for distortion

# Dictionary zur Speicherung der Mausposition und Wiederherstellungsstatus
hand_data = {'hand_position': (hand_x, hand_y), 'restore': False}
distortion_map = np.ones((height, width), dtype=np.uint8)  # Verzerrte Bereiche initialisieren

# Load GIF and corresponding stuff
wave_gif = 'images\waving-hand-cropped.gif'
wave_gif_frames = hlp.resize_and_load_gif(wave_gif)
wave_gif_length = len(wave_gif_frames)
frame_index = 0

pinch_gif = "images\pinch_transparent.gif"
pinch_gif_frames = hlp.load_gif(pinch_gif)
pinch_gif_length = len(pinch_gif_frames)

end_screen_image = cv2.imread('images\end_screen.jpg')
credits_image = cv2.imread('images\Credit_screen.png')

no_landmarks_start_time = None

# Timer for resetting the game without detecting landmaigos
reset_timer = 30

while True:
    ret, frame = cap.read() # Read the frame
    frame = cv2.flip(frame, 1) # Flip the frame horizontally
    original_frame = frame.copy() # original frame for win-condition
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # frame to RGB

    results = hands.process(frame_rgb) # Mediapipe detect hands
    hand_mask = np.zeros_like(frame) # Create a mask for hand landmarks    
    landmarks_list_each_hand = Hand.landmarks(hand_mask, results, show) # Draw landmarks and ger list


    # Check for landmarks and manage timer
    if not results.multi_hand_landmarks:
        if no_landmarks_start_time is None:
            no_landmarks_start_time = time.time()  # Start timer
        elif time.time() - no_landmarks_start_time > reset_timer:
            no_landmarks_start_time = None  # Reset timer

            # Reset the game
            distortion_map = np.ones((height, width), dtype=np.uint8)
            changes_to_videoblock_order = []

            current_state = MainState.PRE_START
    else:
        no_landmarks_start_time = None  # Reset timer if landmarks are detected

               

    ##### STATE PRE_START #####
    if current_state == MainState.PRE_START:
        reset_timer = 30
        hand_x, hand_y = hand_data['hand_position']
        restore = hand_data['restore']
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw a white circle centered at landmark 9
                mask = hlp.draw_white_circle(frame.shape, hand_landmarks, distortion_map)
        for landmarks_list in landmarks_list_each_hand:
            hand_x, hand_y = landmarks_list[9][0], landmarks_list[9][1]
            pass
            
        # Handposition und Wiederherstellungsstatus aus dem Dictionary abrufen
        if restore:
            # Update the distortion map to mark areas as restored
            hand_data['restore'] = False

        hand_x = (hand_x_old * 7 + hand_x + 4) // 8
        hand_y = (hand_y_old * 7 + hand_y + 4) // 8
        hand_x_old = hand_x
        hand_y_old = hand_y

        #Verzerrtes Bild erstellen
        shifted_frame = hlp.radial_shift(frame, (hand_x, hand_y), amplitude=10, wavelength=50)

        #Bereiche ohne Verzerrung (wo die Hand sich bewegt hat) auf das verzerrte Bild anwenden
        mask = distortion_map
        restored_area = cv2.bitwise_and(frame, frame, mask=1 - mask)
        distorted_area = cv2.bitwise_and(shifted_frame, shifted_frame, mask=mask)
        result_frame = cv2.add(restored_area, distorted_area)
        
        combined_frame = cv2.addWeighted(result_frame, 1, hand_mask, 2, 0)
        cv2.imshow(window_name, combined_frame)

        images_compared = mvbt.compareImages(original_frame, result_frame, 50)
        
        if images_compared:
            current_state = MainState.START
            frame_index = 0


    ##### STATE START #####
    if current_state == MainState.START:
        for landmarks_list in landmarks_list_each_hand:
            if Hand.detect_wave(landmarks_list, frame_index):
                current_state = MainState.DIFFICULTY_SELECT
                pass

        combined_frame = cv2.addWeighted(frame, 1, hand_mask, 2, 0)
        
        # Add GIF as overlay
        wave_gif_frame = wave_gif_frames[frame_index % wave_gif_length]
        combined_frame = hlp.overlay_gif_on_frame(combined_frame, wave_gif_frame, position=(50, 50))
        
        cv2.imshow(window_name, combined_frame)


    ##### STATE DIFFICULTY_SELECT #####
    elif current_state == MainState.DIFFICULTY_SELECT:
        frame_with_buttons = Buttons.draw_difficulty_buttons(frame)
        
        # Add GIF as overlay
        pinch_gif_frame = pinch_gif_frames[frame_index % pinch_gif_length]
        frame_with_buttons = hlp.overlay_gif_on_frame(frame_with_buttons, pinch_gif_frame, position=(50, 100))
        
        for landmarks_list in landmarks_list_each_hand:
            pinch_detected, dragging_point = Hand.detect_pinch(landmarks_list)
            
            if pinch_detected and not pinch_active:
                cv2.circle(frame_with_buttons, dragging_point, 10, (255, 255, 255), 2)  # Visual feedback for pinching
                
                # Return int value of difficulty choice
                difficultyChoice = Buttons.check_difficulty_select_coords(dragging_point)
                
                if difficultyChoice != 0: # switch to in_use state
                    current_state = MainState.IN_USE
                    frame_index = 0
                    break
    
        combined_frame = cv2.addWeighted(frame_with_buttons, 1, hand_mask, 2, 0)
        
        cv2.imshow(window_name, combined_frame)


    ##### STATE IN USE #####
    elif current_state == MainState.IN_USE:
        show = True
        puzzle_started = True
        
        # TODO: Choose difficulty of puzzle
        
        match difficultyChoice:
            case 1:
                puzzle_diff = State.PuzzleDifficulty.NORMAL
            case 2:
                puzzle_diff = State.PuzzleDifficulty.HARD
            case 3:
                puzzle_diff = State.PuzzleDifficulty.IMPOSSIBLE
            case 0:
                puzzle_diff = State.PuzzleDifficulty.NONE
                
        
        shuffleFrame = mvbt.split_frame(frame, height, width, puzzle_diff)
        
        shuffleFrame_comparison = mvbt.split_frame(original_frame, height, width, puzzle_diff)
        stitchFrame_comparison = mvbt.stitchBlocks(shuffleFrame_comparison, changes_to_videoblock_order, puzzle_diff)
        
        stitchFrame = mvbt.stitchBlocks(shuffleFrame, changes_to_videoblock_order, puzzle_diff)

        combined_frame = cv2.addWeighted(stitchFrame, 1, hand_mask, 2, 0)

        # HAND DETECTION
        for landmarks_list in landmarks_list_each_hand:
            pinch_detected, dragging_point = Hand.detect_pinch(landmarks_list)
            
            if pinch_detected and not pinch_active:
                cv2.circle(combined_frame, dragging_point, 10, (255, 255, 255), 2)  # Visual feedback for pinching
                square_index = hlp.get_square_index(dragging_point, height, width, puzzle_diff)
                
                if selected_square is None:
                    pinch_active = True
                    selected_square = square_index
                elif selected_square == square_index: # Deselect square
                    pinch_active = True
                    selected_square = None
                elif selected_square != square_index:
                    pinch_active = True
                    # Swap the squares
                    changes_to_videoblock_order.append((square_index, selected_square))
                    selected_square = None  # Reset
                    
            # reset this biatch
            if not pinch_detected:
                pinch_active = False
                
        if frame_index <= pinch_gif_length * 3: # show gif only three times
            # Add GIF as overlay
            pinch_gif_frame = pinch_gif_frames[frame_index % pinch_gif_length]
            combined_frame = hlp.overlay_gif_on_frame(combined_frame, pinch_gif_frame, position=(50, 100))

        # Indicator
        if selected_square is not None:
            hlp.highlight_square(combined_frame, selected_square, height, width, puzzle_diff)

        cv2.imshow(window_name, combined_frame)
        
        images_compared = mvbt.compareImages(original_frame, stitchFrame_comparison, 0)
        
        if images_compared:
            show = False
            current_state = MainState.CREDITS
            frame_index = 0
    
    
    ##### STATE CREDITS ######
    elif current_state == MainState.CREDITS:
        if frame_index < 90:
            cv2.imshow(window_name, end_screen_image)
        elif frame_index >= 90 and frame_index < 390:
            cv2.imshow(window_name, credits_image)
        else:
            distortion_map = np.ones((height, width), dtype=np.uint8)
            changes_to_videoblock_order = []
            current_state = MainState.PRE_START
            frame_index = 0

    frame_index += 1

    # Check if the user pressed ESC / closed the window
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        break
    elif key == 99:
        current_state = MainState.CREDITS

cap.release()
cv2.destroyAllWindows()