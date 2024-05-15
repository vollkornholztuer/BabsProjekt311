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


def detect_wave(arr):
    # Initialize direction switch count
    direction_switch = 0
    
    # TODO: threshold for wave detection
    
    # no early wave detection
    if len(arr) >= 10:
        # Start scanning from the second last element
        for i in range(len(arr) -3, -1, -1):
            # print("i:", i, "len(arr):", len(arr))
            if arr[i] < arr[i + 1]:  # Increasing
                if arr[i + 1] > arr[i + 2]:  # Switching direction
                    direction_switch += 1
            elif arr[i] > arr[i + 1]:  # Decreasing
                if arr[i + 1] < arr[i + 2]:  # Switching direction
                    direction_switch += 1
    else:
        return False
                
    if direction_switch >= 3:
        print("WAVING GESTURE DETECTED")
        return True
    else:
        return False
    
    
def detect_open_palm(landmarks_list, hand_size):
    if not detect_is_finger_down(landmarks_list, hand_size)['index_down'] and not detect_is_finger_down(landmarks_list, hand_size)['middle_down'] and not detect_is_finger_down(landmarks_list, hand_size)['ring_down'] and not detect_is_finger_down(landmarks_list, hand_size)['pinky_down']:
        return landmarks_list[0][1]
    else:
        return 0
    
    
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
    
def detect_pinch(landmarks_list, hand_size):
    if normalized_distance(landmarks_list[4], landmarks_list[8], hand_size) < 0.25 and not detect_is_finger_down(landmarks_list, hand_size)['index_down']:
        return True
    else:
        return False


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

            palm_center = calculate_palm_points(landmarks_list)
            hand_size = calculate_hand_size(landmarks_list, palm_center)

            if (detect_pinch(landmarks_list, hand_size)):
                dragging_point = getDraggingPoint(landmarks_list)
                cv2.circle(frame, dragging_point, 10, (255, 255, 255), 2)  # Visual feedback for pinching
            
            # handPositionX = detect_open_palm(landmarks_list, hand_size)
            # if handPositionX != 0:
            #     x_hand_offset_arr = np.append(x_hand_offset_arr, handPositionX)
            #     print(x_hand_offset_arr)
            
    #         if (detect_wave(x_hand_offset_arr) or len(x_hand_offset_arr) > 20):
    #             x_hand_offset_arr = np.array([]) # reset array
                
    #         key = cv2.waitKey(1)
    #         if key == ord('p'):
    #             printHandCoords(landmarks_list, hand_size)
    # return x_hand_offset_arr