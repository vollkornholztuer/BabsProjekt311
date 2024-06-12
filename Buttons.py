import cv2

def draw_difficulty_buttons(frame):
    # Draw buttons
    cv2.rectangle(frame, (50, 50), (200, 150), (240, 240, 240), -1)
    cv2.putText(frame, 'Normal', (80, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    cv2.rectangle(frame, (250, 50), (400, 150), (240, 240, 240), -1)
    cv2.putText(frame, 'Hard', (300, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    cv2.rectangle(frame, (450, 50), (600, 150), (240, 240, 240), -1)
    cv2.putText(frame, 'Impossible', (470, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    return frame

def check_difficulty_select_coords(dragging_point):
    if 50 < dragging_point[0] < 200 and 50 < dragging_point[1] < 150:
        return 1
    elif 250 < dragging_point[0] < 400 and 50 < dragging_point[1] < 150:
        return 2
    elif 450 < dragging_point[0] < 600 and 50 < dragging_point[1] < 150:
        return 3
    else:
        return 0