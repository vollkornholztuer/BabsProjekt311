import cv2
import numpy as np
import random

# Funktion zur Berechnung der radialen Verschiebung
def radial_shift(frame, mouse_position, amplitude, wavelength):
    height, width = frame.shape[:2]

    x, y = np.meshgrid(np.arange(width), np.arange(height))  # Koordinatenraster erstellen

    # Entfernungen und Winkel zur Mausposition berechnen
    distance = np.sqrt((x - mouse_position[0])**2 + (y - mouse_position[1])**2)  # Entfernung zur Mausposition
    angle = np.arctan2(y - mouse_position[1], x - mouse_position[0])  # Winkel in Bogenmaß

    displacement = amplitude * np.sin(distance / wavelength)  # Verschiebung basierend auf Welle berechnen

    # Neue Positionen nach Verschiebung berechnen
    new_x = (x + displacement * np.cos(angle)).clip(0, width - 1).astype(int)
    new_y = (y + displacement * np.sin(angle)).clip(0, height - 1).astype(int)
    
    shifted_frame = frame[new_y, new_x]  # Pixelwerte aus dem ursprünglichen Bild zuweisen

    return shifted_frame

# Funktion zum Auswählen und Testen der Kamera
def select_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Camera with index {camera_index} could not be opened.")
        return

    # Fenster für das Originalbild erstellen
    cv2.namedWindow("Original Frame")

    # Initialisieren Sie das Verzerrungsgebiet
    distortion_map = np.ones((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))), dtype=np.uint8)

    while True:
        # Frame aus der Webcam erfassen
        ret, frame = cap.read()

        if not ret:
            break

        # Aktuelle Mausposition abrufen
        mouse_x, mouse_y = cv2.getWindowImageRect('Original Frame')[:2]
        mouse_x, mouse_y = mouse_x + int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2), mouse_y + int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
        
        mouse_position = (mouse_x, mouse_y)

        # Verzerrtes Bild erstellen
        shifted_frame = radial_shift(frame, mouse_position, amplitude=10, wavelength=50)

        # Bereiche ohne Verzerrung (wo die Maus sich bewegt hat) auf das verzerrte Bild anwenden
        mask = distortion_map
        restored_area = cv2.bitwise_and(frame, frame, mask=1 - mask)
        distorted_area = cv2.bitwise_and(shifted_frame, shifted_frame, mask=mask)
        result_frame = cv2.add(restored_area, distorted_area)

        # Ergebnis anzeigen
        cv2.imshow("Original Frame", result_frame)

        # ESC zum Beenden drücken
        if cv2.waitKey(1) == 27:
            break

    # Webcam-Feed freigeben und Fenster schließen
    cap.release()
    cv2.destroyAllWindows()

select_camera(0)  # Auswahl der Kamera mit Index 0
