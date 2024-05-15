import cv2
import math

cap = cv2.VideoCapture(0)  # Öffne die Webcam (0 steht für die erste verfügbare Kamera)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

phi = 0
sign = 1

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
            sign = -1
        else:
            sign = 1

    for y in range(height // 4, height - height // 4):
        if y < height // 2:
            A = 20 * (y - height / 4) / height * 4
        else:
            A = 20 * (3 * height / 4 - y) / height * 4
        source_y = round(y + A * math.cos(2 * math.pi * y / height + phi))
        for x in range(width):
            if 0 <= source_y < height:
                shifted_frame[y, x] = frame[source_y, x]

    cv2.imshow('Shifted Webcam', shifted_frame)
    cv2.imshow("Original", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 