import numpy as np
import cv2
# ingertips for clarity
# wrist = landmarks_list[0]
# thumb_tip = landmarks_list[4]
# index_tip = landmarks_list[8]
# middle_tip = landmarks_list[12]
# ring_tip = landmarks_list[16]
# pinky_tip = landmarks_list[20]

# Pinch state
is_pinching = False
x_hand_positions = []

# Hand middle point
def calculate_palm_points(landmarks_list):
    wrist = np.array(landmarks_list[0])
    thumb_base = np.array(landmarks_list[2])
    index_base = np.array(landmarks_list[5])
    middle_base = np.array(landmarks_list[9])
    ring_base = np.array(landmarks_list[13])
    pinky_base = np.array(landmarks_list[17])

    return np.mean([wrist, thumb_base, index_base, middle_base, ring_base, pinky_base], axis=0)


def calculate_hand_size(landmarks_list, palm_center):
    return calculate_distance(landmarks_list[0], palm_center)


# Function to calculate distance
def calculate_distance(p1, p2):
#     # p = x, y of landmark
#     # sqrt((x2 - x1)^2 + (y2 - y1)^2) distance between 2 points
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def normalized_distance(p1, p2, hand_size):
    raw_distance = calculate_distance(p1, p2)
    return raw_distance / hand_size


def detect_is_finger_down(landmarks_list, hand_size):
    finger_status = {
        # 'thumb_down': normalized_distance(landmarks_list[4], landmarks_list[0], hand_size) < 0.25,
        'index_down': normalized_distance(landmarks_list[8], landmarks_list[0], hand_size) < 1.5,
        'middle_down': normalized_distance(landmarks_list[12], landmarks_list[0], hand_size) < 1.5,
        'ring_down': normalized_distance(landmarks_list[16], landmarks_list[0], hand_size) < 1.5,
        'pinky_down': normalized_distance(landmarks_list[20], landmarks_list[0], hand_size) < 1.5
    }
    return finger_status


def detect_wave(landmarks_list):
    global x_hand_positions
    threshold = 3
    min_distance = 5
    
    palm_center = calculate_palm_points(landmarks_list)
    x_hand_positions.append(palm_center[0])
    
    # Keep only the last 20 positions
    if len(x_hand_positions) > 20:
        x_hand_positions.pop(0)
    
    direction_changes = 0
    
    # Check the number of direction changes
    for i in range(1, len(x_hand_positions) - 1):
        if abs(x_hand_positions[i] - x_hand_positions[i - 1]) > min_distance and abs(x_hand_positions[i] - x_hand_positions[i + 1]) > min_distance:
            if (x_hand_positions[i] > x_hand_positions[i - 1] and x_hand_positions[i] > x_hand_positions[i + 1]) or \
               (x_hand_positions[i] < x_hand_positions[i - 1] and x_hand_positions[i] < x_hand_positions[i + 1]):
                direction_changes += 1
    
    if direction_changes >= threshold:
        print("WAVING GESTURE DETECTED")
        return True
    return False
    

def detect_open_palm(landmarks_list, hand_size):
    if not detect_is_finger_down(landmarks_list, hand_size)['index_down'] and not detect_is_finger_down(landmarks_list, hand_size)['middle_down'] and not detect_is_finger_down(landmarks_list, hand_size)['ring_down'] and not detect_is_finger_down(landmarks_list, hand_size)['pinky_down']:
        return landmarks_list[0][1]
    
    
def getDraggingPoint(landmarks_list): # calc middle point between both tips
    return ((landmarks_list[4][0] + landmarks_list[8][0]) // 2, (landmarks_list[4][1] + landmarks_list[8][1]) // 2)


def printHandCoords(landmarks_list, hand_size):
    print("\n")
    print("thumb: ", normalized_distance(landmarks_list[4], landmarks_list[0], hand_size))
    print("index: ", normalized_distance(landmarks_list[8], landmarks_list[0], hand_size))
    print("middle: ", normalized_distance(landmarks_list[12], landmarks_list[0], hand_size))
    print("ring: ", normalized_distance(landmarks_list[16], landmarks_list[0], hand_size))
    print("pinky: ", normalized_distance(landmarks_list[20], landmarks_list[0], hand_size))
    print("\n")
    
    
def detect_pinch(landmarks_list):
    palm_center = calculate_palm_points(landmarks_list)
    hand_size = calculate_hand_size(landmarks_list, palm_center)
    threshold = 0.15

    if normalized_distance(landmarks_list[4], landmarks_list[8], hand_size) < threshold and not detect_is_finger_down(landmarks_list, hand_size)['index_down']:
        dragging_point = getDraggingPoint(landmarks_list)
        return True, dragging_point
    return False, (0,0)


def draw_lines(i, x1, y1, x2, y2, hand_landmarks, frame, show):
    if show:
        cv2.circle(frame, (x1, y1), 5, (0, 0, 255), -1) # Draw a circle for each landmark
        cv2.putText(frame, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) # Write the index of the landmark

        if i%4 != 0:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # Draw a line between the landmarks
            
            if i == 1 or i == 5 or i == 17:
                x0 = int(hand_landmarks.landmark[0].x * frame.shape[1])
                y0 = int(hand_landmarks.landmark[0].y * frame.shape[0])
                cv2.line(frame, (x1, y1), (x0, y0), (0, 255, 0), 2)


def landmarks(frame, results, show):
    landmarks_list_per_hand = []

    if results.multi_hand_landmarks: # Check if there are hands detected
        for hand_landmarks in results.multi_hand_landmarks: # Iterate through the hands
            landmarks_list = []
            for i, landmark in enumerate(hand_landmarks.landmark): # Iterate through the landmarks
                if i <= 20: 
                    x1 = int(landmark.x * frame.shape[1]) 
                    y1 = int(landmark.y * frame.shape[0])
                    
                    landmarks_list.append((x1, y1))
                    
                    if i < 20:
                        landmark_next = hand_landmarks.landmark[i+1] # Get the next landmark
                    
                    x2 = int(landmark_next.x * frame.shape[1])
                    y2 = int(landmark_next.y * frame.shape[0])

                    draw_lines(i, x1, y1, x2, y2, hand_landmarks, frame, show)

            landmarks_list_per_hand.append(landmarks_list)
                
    return landmarks_list_per_hand