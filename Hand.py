import numpy as np
import cv2
# Fingertips for clarity
# wrist = landmarks_list[0]
# thumb_tip = landmarks_list[4]
# index_tip = landmarks_list[8]
# middle_tip = landmarks_list[12]
# ring_tip = landmarks_list[16]
# pinky_tip = landmarks_list[20]

# Pinch state
is_pinching = False
x_hand_positions = []

# calculate middle point of palm
def calculate_palm_points(landmarks_list):
    wrist = np.array(landmarks_list[0])
    thumb_base = np.array(landmarks_list[2])
    index_base = np.array(landmarks_list[5])
    middle_base = np.array(landmarks_list[9])
    ring_base = np.array(landmarks_list[13])
    pinky_base = np.array(landmarks_list[17])

    return np.mean([wrist, thumb_base, index_base, middle_base, ring_base, pinky_base], axis=0) # return the mean of the points (palm center)

def calculate_hand_size(landmarks_list, palm_center): 
    return calculate_distance(landmarks_list[0], palm_center)
    # important for pinch detection according to hand size, and therefore distance between hand and camera (scaling factor)


# Function to calculate distance
def calculate_distance(p1, p2):
#     # p = x, y of landmark
#     # sqrt((x2 - x1)^2 + (y2 - y1)^2) distance between 2 points
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def normalized_distance(p1, p2, hand_size): # normalized distance between 2 points 
    raw_distance = calculate_distance(p1, p2) # calculate distance between 2 points
    return raw_distance / hand_size # return the distance divided by the hand size


def detect_is_finger_down(landmarks_list, hand_size):
    finger_status = {
        # 'thumb_down': normalized_distance(landmarks_list[4], landmarks_list[0], hand_size) < 0.25,
        'index_down': normalized_distance(landmarks_list[8], landmarks_list[0], hand_size) < 1.5,
        'middle_down': normalized_distance(landmarks_list[12], landmarks_list[0], hand_size) < 1.5,
        'ring_down': normalized_distance(landmarks_list[16], landmarks_list[0], hand_size) < 1.5,
        'pinky_down': normalized_distance(landmarks_list[20], landmarks_list[0], hand_size) < 1.5
    }
    return finger_status


def detect_wave(landmarks_list, frame_index): # detect wave motion
    if frame_index < 40: # cooldown period of 40 frames
        return False
    
    global x_hand_positions # global variable
    threshold = 3 # threshold for direction changes 
    min_distance = 2 # minimum distance for direction changes
    
    x_hand_positions.append(landmarks_list[12][0]) # append the x position of the middle finger
    
    # Keep only the last 50 positions
    if len(x_hand_positions) > 50:
        x_hand_positions.pop(0) # remove the first element if array length is greater than 50
    
    direction_changes = 0 # initialize direction changes
    
    # Check the number of direction changes
    for i in range(3, len(x_hand_positions) - 3):
        
        # Check if the distance between the current position and the previous and next positions is greater than the minimum distance
        if abs(x_hand_positions[i] - x_hand_positions[i - 3]) > min_distance and abs(x_hand_positions[i] - x_hand_positions[i + 3]) > min_distance:
            
            # Check if the current position is greater or less than the previous and next positions
            if (x_hand_positions[i] > x_hand_positions[i - 3] and x_hand_positions[i] > x_hand_positions[i + 3]) or \
                (x_hand_positions[i] < x_hand_positions[i - 3] and x_hand_positions[i] < x_hand_positions[i + 3]):
                direction_changes += 1

    if direction_changes >= threshold: # if direction changes are greater than threshold
        return True # wave detected
    return False # wave not detected
    
    
def getDraggingPoint(landmarks_list): # calc middle point between tip of thumb and index finger
    return ((landmarks_list[4][0] + landmarks_list[8][0]) // 2, (landmarks_list[4][1] + landmarks_list[8][1]) // 2)

    
def detect_pinch(landmarks_list): 
    palm_center = calculate_palm_points(landmarks_list) # calculate palm center
    hand_size = calculate_hand_size(landmarks_list, palm_center) # calculate hand size
    threshold = 0.2 # threshold for pinch detection

    # if the distance between the thumb tip and index tip is less than the threshold and the index finger is not down, return True and the middle point between the thumb tip and index tip
    if normalized_distance(landmarks_list[4], landmarks_list[8], hand_size) < threshold and not detect_is_finger_down(landmarks_list, hand_size)['index_down']:
        dragging_point = getDraggingPoint(landmarks_list)
        return True, dragging_point
    return False, (0,0)

# Draw lines between landmarks to show the hands
def draw_lines(i, x1, y1, x2, y2, hand_landmarks, frame, show):
    if show:
        cv2.circle(frame, (x1, y1), 5, (255, 255, 255), -1)  # Draw a circle for each landmark

        if i % 4 != 0:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 10) # Draw a black border line (thicker)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 6) # Draw a white inner line (thinner)

            if i == 1 or i == 5 or i == 17: # if the landmark is the wrist, thumb tip or pinky tip
                x0 = int(hand_landmarks.landmark[0].x * frame.shape[1]) # Get the x position of the wrist
                y0 = int(hand_landmarks.landmark[0].y * frame.shape[0]) # Get the y position of the wrist
                
                cv2.line(frame, (x1, y1), (x0, y0), (0, 0, 255), 10)  # Draw a black border line (thicker)
                cv2.line(frame, (x1, y1), (x0, y0), (255, 255, 255), 6) # Draw a white inner line (thinner)


# Function to detect landmarks
def landmarks(frame, results, show):
    landmarks_list_per_hand = [] # list of landmarks for each hand

    if results.multi_hand_landmarks: # Check if there are hands detected
        for hand_landmarks in results.multi_hand_landmarks: # Iterate through the hands
            landmarks_list = [] # list of landmarks for each hand
            for i, landmark in enumerate(hand_landmarks.landmark): # Iterate through the landmarks
                if i <= 20: # if the landmark is less than or equal to 20
                    x1 = int(landmark.x * frame.shape[1]) # Get the x position of the landmark
                    y1 = int(landmark.y * frame.shape[0]) # Get the y position of the landmark
                     
                    landmarks_list.append((x1, y1)) # append the x and y position of the landmark as a tuple to the landmarks list
                    
                    if i < 20:
                        landmark_next = hand_landmarks.landmark[i+1] # Get the next landmark
                    
                    x2 = int(landmark_next.x * frame.shape[1]) # Get the x position of the next landmark
                    y2 = int(landmark_next.y * frame.shape[0]) # Get the y position of the next landmark

                    draw_lines(i, x1, y1, x2, y2, hand_landmarks, frame, show) # Draw lines between landmarks to show the hands

            landmarks_list_per_hand.append(landmarks_list) # append the landmarks list to the landmarks list per hand
                
    return landmarks_list_per_hand # return the landmarks list for each hand