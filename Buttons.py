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