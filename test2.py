import cv2
import math
import time

# Funktion zur Erfassung des Mausklicks
def mouse_click(event, x, y, flags, param):
    global selected_x, click_time
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_x = x
        click_time = time.time()

cap = cv2.VideoCapture(0)  # Öffne die Webcam (0 steht für die erste verfügbare Kamera)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

phi = 0
sign = 2
selected_x = -1
click_time = 0

cv2.namedWindow('Shifted Webcam')
cv2.setMouseCallback('Shifted Webcam', mouse_click)

while True:
    ret, frame = cap.read()  # Erfassen eines Frames von der Webcam
    if not ret:
        print("Error: Failed to capture frame")
        break

    height, width, channels = frame.shape

    shifted_frame = frame.copy()
    phi = phi + 0.1 * sign
    if phi > math.pi:
        if sign > 0:
            sign = -2
        else:
            sign = 2

    if time.time() - click_time < 1:  # Überprüfen, ob die Zeit seit dem Mausklick kleiner als 5 Sekunden ist
        for y in range(height // 4, height - height // 4):
            if y < height // 2:
                A = 20 * (y - height / 4) / height * 4
            else:
                A = 20 * (3 * height / 4 - y) / height * 4
            source_y = round(y + A * math.cos(2 * math.pi * y / height + phi))
            for x in range(width):
                if selected_x - 50 <= x <= selected_x + 50:  # Überprüfen, ob der x-Wert im Bereich von ±20 Pixeln um den ausgewählten Wert liegt
                    if 0 <= source_y < height:
                        shifted_frame[y, x] = frame[source_y, x]
    else:
        selected_x = -1  # Zurücksetzen des ausgewählten x-Werts, wenn die 5 Sekunden abgelaufen sind

    cv2.imshow('Shifted Webcam', shifted_frame)
    cv2.imshow("Original", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()