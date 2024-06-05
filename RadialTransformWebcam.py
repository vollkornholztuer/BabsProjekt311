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

    # Koordinatenraster erstellen
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Entfernungen und Winkel zur Mausposition berechnen
    distance = np.sqrt((x - mouse_position[0])**2 + (y - mouse_position[1])**2)
    angle = np.arctan2(y - mouse_position[1], x - mouse_position[0])

    # Verschiebung basierend auf Welle berechnen
    displacement = amplitude * np.sin(distance / wavelength)

    # Neue Positionen nach Verschiebung berechnen
    new_x = (x + displacement * np.cos(angle)).clip(0, width - 1).astype(int)
    new_y = (y + displacement * np.sin(angle)).clip(0, height - 1).astype(int)

    # Pixelwerte aus dem ursprünglichen Bild zuweisen
    shifted_frame = frame[new_y, new_x]

    return shifted_frame

# Mausklickereignis-Callback-Funktion
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y, start_time
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y
        start_time = time.time()

# Funktion zum Auswählen und Testen der Kamera
def select_camera(camera_index=0):
    global mouse_x, mouse_y, start_time
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Camera with index {camera_index} could not be opened.")
        return

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


select_camera(1)  # Auswahl der Kamera mit Index 1

