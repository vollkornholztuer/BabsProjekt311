import cv2
import numpy as np
import math

# Variablen zur Speicherung der Koordinaten des Mausklicks
mouse_x, mouse_y = -1, -1

# Funktion zur Berechnung der radialen Verschiebung
def radial_shift(image, mouse_position, amplitude, wavelength):
    height, width = image.shape[:2]

    # Leeres Bild erstellen
    shifted_image = np.zeros_like(image)

    # Mittelpunkt des Bildes
    center_x = width // 2
    center_y = height // 2

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

            # Sicherstellen, dass die neue Position innerhalb der Bildgrenzen liegt
            if 0 <= new_x < width and 0 <= new_y < height:
                shifted_image[new_y, new_x] = image[y, x]

    return shifted_image

# Mausklickereignis-Callback-Funktion
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y

    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y

        # Radiale Verschiebung durchführen und Ergebnis anzeigen
        shifted_image = radial_shift(image, (mouse_x, mouse_y), amplitude=30, wavelength=50)
        cv2.imshow("Radially Shifted Image", shifted_image)

# Bild laden
image = cv2.imread("TestImage.png")
cv2.imshow("Original Image", image)
cv2.setMouseCallback("Original Image", mouse_callback)

# Auf Mausklick warten
cv2.waitKey(0)
cv2.destroyAllWindows()