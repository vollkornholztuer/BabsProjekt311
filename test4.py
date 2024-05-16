import cv2
import numpy as np
import math
import time

# Variablen zur Speicherung der Koordinaten des Mausklicks und der Zeit
mouse_x, mouse_y = -1, -1
start_time = None

# Funktion zur Berechnung der radialen Verschiebung
def radial_shift(frame, mouse_position, amplitude, wavelength):
    height, width = frame.shape[:2]

    # Leeres Bild erstellen
    shifted_frame = np.zeros_like(frame)

    # Radiale Verschiebung durchführen
    for y in range(height):
        for x in range(width):
            # Entfernung vom Mittelpunkt berechnen
            distance = np.sqrt((x - mouse_position[0])**2 + (y - mouse_position[1])**2)

            # Winkel zur Mausposition berechnen
            angle = math.atan2(y - mouse_position[1], x - mouse_position[0])

            # Verschiebung basierend auf Welle berechnen
            displacement = amplitude * math.sin(distance / wavelength)

            # Neue Position nach Verschiebung berechnen
            new_x = int(x + displacement * math.cos(angle))
            new_y = int(y + displacement * math.sin(angle))

            # Werte der neuen Position begrenzen
            new_x = max(0, min(new_x, width - 1))
            new_y = max(0, min(new_y, height - 1))

            # Pixelwert aus dem ursprünglichen Bild zuweisen
            shifted_frame[y, x] = frame[new_y, new_x]

    return shifted_frame

# Mausklickereignis-Callback-Funktion
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y, start_time
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y
        start_time = time.time()

# Webcam initialisieren
cap = cv2.VideoCapture(0)

# Fenster für das Originalbild erstellen
cv2.namedWindow("Original Frame")

# Mausklickereignisse festlegen
cv2.setMouseCallback("Original Frame", mouse_callback)

while True:
    # Frame aus der Webcam erfassen
    ret, frame = cap.read()

    if not ret:
        break

    # Radiale Verschiebung durchführen und Ergebnis anzeigen, wenn Mausklick stattgefunden hat
    if mouse_x != -1 and mouse_y != -1:
        elapsed_time = time.time() - start_time
        if elapsed_time < 3:
            shifted_frame = radial_shift(frame, (mouse_x, mouse_y), amplitude=10, wavelength=50)
            cv2.imshow("Original Frame", shifted_frame)
        else:
            cv2.imshow("Original Frame", frame)
            mouse_x, mouse_y = -1, -1  # Zurücksetzen der Mausklickkoordinaten
            start_time = None
    else:
        cv2.imshow("Original Frame", frame)

    # ESC zum Beenden drücken
    if cv2.waitKey(1) == 27:
        break

# Webcam-Feed freigeben und Fenster schließen
cap.release()
cv2.destroyAllWindows()