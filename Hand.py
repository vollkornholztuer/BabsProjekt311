import numpy as np

# ingertips for clarity
# wrist = landmarks_list[0]
# thumb_tip = landmarks_list[4]
# index_tip = landmarks_list[8]
# middle_tip = landmarks_list[12]
# ring_tip = landmarks_list[16]
# pinky_tip = landmarks_list[20]

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
    if len(arr) < 10   :
        return False
    
    # Initialize direction switch count
    direction_switch = 0
    
    # Start scanning from the second last element
    for i in range(len(arr) -3, -1, -1):
        print("i:", i, "len(arr):", len(arr))
        if arr[i] < arr[i + 1]:  # Increasing
            if arr[i + 1] > arr[i + 2]:  # Switching direction
                direction_switch += 1
        elif arr[i] > arr[i + 1]:  # Decreasing
            if arr[i + 1] < arr[i + 2]:  # Switching direction
                direction_switch += 1
                
    if direction_switch >= 3:
        return True
    else:
        return False
    
    
def detect_open_palm(landmarks_list, hand_size):
    thumb_distance = normalized_distance(landmarks_list[4], landmarks_list[0], hand_size)
    index_distance = normalized_distance(landmarks_list[8], landmarks_list[0], hand_size)
    middle_distance = normalized_distance(landmarks_list[12], landmarks_list[0], hand_size)
    ring_distance = normalized_distance(landmarks_list[16], landmarks_list[0], hand_size)
    pinky_distance = normalized_distance(landmarks_list[20], landmarks_list[0], hand_size)
    
    # detect open palm
    if thumb_distance > 1.6 and index_distance > 2 and middle_distance > 2 and ring_distance > 2 and pinky_distance > 2:
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