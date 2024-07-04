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

current_state = MainState.PRE_START # initial state

puzzle_started = False 
puzzle_diff = State.PuzzleDifficulty.NONE

show = False # show lines of hand detection
changes_to_videoblock_order = [] # initialize list of changes to videoblock order
selected_square = None # initialize selected square for swapping
pinch_active = False # initialize pinch active state
difficultyChoice = 0 # 0 = no choice, 1 = normal, 2 = hard, 3 = impossible

hand_x_old, hand_y_old = 0, 0 # initialize old hand position for smoothing

mp_hands = mp.solutions.hands # import mediapipe hand module
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8) # initialize hand detection and detect only one hand

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # initialize webcam capture

window_name = 'Webcam Feed'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # camera dimensions
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

hand_x, hand_y = random.randint(0, width - 1), random.randint(0, height - 1) # random position for distortion

# Dictionary zur Speicherung der Handposition und Wiederherstellungsstatus
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

# Load images
end_screen_image = cv2.imread('images\end_screen.jpg')
credits_image = cv2.imread('images\Credit_screen.png')

no_landmarks_start_time = None # initialize timer for resetting the game without detecting landmarks

reset_timer = 30 # Timer for resetting the game without detecting landmarks

# Main loop
while True:
    ret, frame = cap.read() # Read the frame
    frame = cv2.flip(frame, 1) # Flip the frame horizontally
    original_frame = frame.copy() # original frame for win-condition
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # frame to RGB

    results = hands.process(frame_rgb) # Mediapipe detect hands
    hand_mask = np.zeros_like(frame) # Create a mask for hand landmarks    
    landmarks_list_each_hand = Hand.landmarks(hand_mask, results, show) # Draw landmarks and ger list


    # Check for landmarks and manage timer
    if not results.multi_hand_landmarks: # if no hands are detected
        if no_landmarks_start_time is None: # if timer is not running
            no_landmarks_start_time = time.time()  # Start timer
        elif time.time() - no_landmarks_start_time > reset_timer: # if timer is running and time is up
            no_landmarks_start_time = None  # Reset timer

            # Reset the game
            distortion_map = np.ones((height, width), dtype=np.uint8) # Reset distortion map
            changes_to_videoblock_order = [] # Reset changes to videoblock order

            current_state = MainState.PRE_START # Reset state
    else:
        no_landmarks_start_time = None  # Reset timer if landmarks are detected

               

    ##### STATE PRE_START #####
    if current_state == MainState.PRE_START:
        reset_timer = 30 # Reset timer for resetting the game without detecting landmarks
        hand_x, hand_y = hand_data['hand_position'] # Retrieve hand position from the dictionary
        restore = hand_data['restore'] # Retrieve restore status from the dictionary
        if results.multi_hand_landmarks: # if hands are detected
            for hand_landmarks in results.multi_hand_landmarks: # iterate through detected hands
                mask = hlp.draw_white_circle(frame.shape, hand_landmarks, distortion_map) # Draw a white circle centered at landmark 9 (masking)
        for landmarks_list in landmarks_list_each_hand: # iterate through detected hands
            hand_x, hand_y = landmarks_list[9][0], landmarks_list[9][1] # Get the x and y coordinates of landmark 9 (base of middle finger)
            pass
            
        # Retrieve hand position and restore status from the dictionary
        if restore:
            hand_data['restore'] = False # Update the distortion map to mark areas as restored

        # Smoothing of hand position for less jitter when hand is detected
        hand_x = (hand_x_old * 7 + hand_x + 4) // 8
        hand_y = (hand_y_old * 7 + hand_y + 4) // 8
        hand_x_old = hand_x
        hand_y_old = hand_y

        shifted_frame = hlp.radial_shift(frame, (hand_x, hand_y), amplitude=10, wavelength=50) # create radial shift effect

        # Apply areas without distortion (where the hand has moved) to the distorted image
        mask = distortion_map # Create a mask for the restored area
        restored_area = cv2.bitwise_and(frame, frame, mask=1 - mask) # Apply the mask to the original frame
        distorted_area = cv2.bitwise_and(shifted_frame, shifted_frame, mask=mask) # Apply the mask to the shifted frame
        result_frame = cv2.add(restored_area, distorted_area) # Combine the restored and distorted areas
        
        combined_frame = cv2.addWeighted(result_frame, 1, hand_mask, 2, 0) # Add the hand mask to the frame
        cv2.imshow(window_name, combined_frame) # Display the frame

        images_compared = mvbt.compareImages(original_frame, result_frame, 50) # Compare the original frame with the distorted frame (50% must match)
        
        if images_compared: # if the images match
            current_state = MainState.START # switch to start state
            frame_index = 0 # reset frame index for further use


    ##### STATE START #####
    if current_state == MainState.START:
        for landmarks_list in landmarks_list_each_hand: # iterate through detected hands
            if Hand.detect_wave(landmarks_list, frame_index): # if wave gesture is detected
                current_state = MainState.DIFFICULTY_SELECT # switch to difficulty select state
                pass

        combined_frame = cv2.addWeighted(frame, 1, hand_mask, 2, 0) # Add the hand mask to the frame
        
        # Add GIF as overlay
        wave_gif_frame = wave_gif_frames[frame_index % wave_gif_length] # Get the current GIF frame
        combined_frame = hlp.overlay_gif_on_frame(combined_frame, wave_gif_frame, position=(50, 50)) # Overlay the GIF on the frame at position (50, 50)
        
        cv2.imshow(window_name, combined_frame) # Display the frame


    ##### STATE DIFFICULTY_SELECT #####
    elif current_state == MainState.DIFFICULTY_SELECT:
        frame_with_buttons = Buttons.draw_difficulty_buttons(frame) # Draw the difficulty buttons on top of the frame
        
        # Add GIF as overlay
        pinch_gif_frame = pinch_gif_frames[frame_index % pinch_gif_length] # Get the current GIF frame
        frame_with_buttons = hlp.overlay_gif_on_frame(frame_with_buttons, pinch_gif_frame, position=(50, 100)) # Overlay the GIF on the frame at position (50, 100)
        
        for landmarks_list in landmarks_list_each_hand: # iterate through detected hands
            pinch_detected, dragging_point = Hand.detect_pinch(landmarks_list) # detect pinch gesture and get dragging point
            
            if pinch_detected and not pinch_active:
                cv2.circle(frame_with_buttons, dragging_point, 10, (255, 255, 255), 2)  # Visual feedback for pinching
                
                difficultyChoice = Buttons.check_difficulty_select_coords(dragging_point) # Return int value of difficulty choice
                
                if difficultyChoice != 0: # if a difficulty choice is made
                    current_state = MainState.IN_USE # switch to in use state
                    frame_index = 0 # reset frame index for further use
                    break
    
        combined_frame = cv2.addWeighted(frame_with_buttons, 1, hand_mask, 2, 0) # Add the hand mask to the frame
        
        cv2.imshow(window_name, combined_frame) # Display the frame


    ##### STATE IN USE #####
    elif current_state == MainState.IN_USE:
        show = True # show lines of hand detection
        puzzle_started = True # puzzle has started
        
        #Choose difficulty of puzzle
        
        match difficultyChoice:
            case 1:
                puzzle_diff = State.PuzzleDifficulty.NORMAL
            case 2:
                puzzle_diff = State.PuzzleDifficulty.HARD
            case 3:
                puzzle_diff = State.PuzzleDifficulty.IMPOSSIBLE
            case 0:
                puzzle_diff = State.PuzzleDifficulty.NONE
                
        
        shuffleFrame = mvbt.split_frame(frame, height, width, puzzle_diff) # Split the frame into blocks
        
        shuffleFrame_comparison = mvbt.split_frame(original_frame, height, width, puzzle_diff) # Split the original frame into blocks for comparison
        stitchFrame_comparison = mvbt.stitchBlocks(shuffleFrame_comparison, changes_to_videoblock_order, puzzle_diff) # Stitch the blocks together for comparison
        
        stitchFrame = mvbt.stitchBlocks(shuffleFrame, changes_to_videoblock_order, puzzle_diff) # Stitch the blocks of shuffled frame together

        combined_frame = cv2.addWeighted(stitchFrame, 1, hand_mask, 2, 0) # Add the hand mask to the frame

        # HAND DETECTION
        for landmarks_list in landmarks_list_each_hand: # iterate through detected hands
            pinch_detected, dragging_point = Hand.detect_pinch(landmarks_list) # detect pinch gesture and get dragging point
            
            if pinch_detected and not pinch_active:
                cv2.circle(combined_frame, dragging_point, 10, (255, 255, 255), 2)  # Visual feedback for pinching
                square_index = hlp.get_square_index(dragging_point, height, width, puzzle_diff) # Get the video block index based on the dragging point
                
                if selected_square is None: # Select square
                    pinch_active = True
                    selected_square = square_index
                elif selected_square == square_index: # Deselect square
                    pinch_active = True
                    selected_square = None
                elif selected_square != square_index: # Swap squares
                    pinch_active = True
                    # Swap the squares
                    changes_to_videoblock_order.append((square_index, selected_square)) # Append the changes to the videoblock order (for display)
                    selected_square = None  # Reset
                    
            if not pinch_detected: # if pinch is not detected
                pinch_active = False # reset pinch active state
          
        # Add GIF as overlay      
        if frame_index <= pinch_gif_length * 3: # show gif only three times
            pinch_gif_frame = pinch_gif_frames[frame_index % pinch_gif_length] # Get the current GIF frame
            combined_frame = hlp.overlay_gif_on_frame(combined_frame, pinch_gif_frame, position=(50, 100)) # Overlay the GIF on the frame at position (50, 100)

        # Highlight selected square
        if selected_square is not None: # if a square is selected
            hlp.highlight_square(combined_frame, selected_square, height, width, puzzle_diff) # Highlight the selected square

        cv2.imshow(window_name, combined_frame)
        
        images_compared = mvbt.compareImages(original_frame, stitchFrame_comparison, 0) # Compare the original frame with the stitched frame (100% must match)
        
        # WIN CONDITION
        if images_compared: # if the images match
            show = False # hide lines of hand detection
            current_state = MainState.CREDITS # switch to credits state
            frame_index = 0 # reset frame index for further use
    
    
    ##### STATE CREDITS ######
    elif current_state == MainState.CREDITS: 
        if frame_index < 90: # show end screen for 90 frames
            cv2.imshow(window_name, end_screen_image)
        elif frame_index >= 90 and frame_index < 390: # show credits for 300 frames
            cv2.imshow(window_name, credits_image)
        else: # reset the game
            distortion_map = np.ones((height, width), dtype=np.uint8) # Reset distortion map
            changes_to_videoblock_order = [] # Reset changes to videoblock order
            current_state = MainState.PRE_START # switch to pre start state
            frame_index = 0 # reset frame index for further use
            pinch_active = False # reset pinch active state
            selected_square = None # reset selected square

    frame_index += 1

    # Check if the user pressed ESC / closed the window
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:  # Check if the pressed key is ESC
        break
    elif key == 99:
        current_state = MainState.CREDITS

cap.release()
cv2.destroyAllWindows()