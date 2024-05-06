import cv2
import numpy as np

# Bild laden
image = cv2.imread('TestImage.png')

if image is not None:
    # Ursprüngliche Koordinaten des Pixels
    x, y = 100, 100

    # Neue Koordinaten nach der Verschiebung
    new_x, new_y = 120, 120

    # Verschiebungsvektor berechnen
    dx, dy = new_x - x, new_y - y

    # Matrix für die Verschiebung erstellen
    M = np.float32([[1, 0, dx], [0, 1, dy]])

    # Bild transformieren
    shifted_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    # Anzeige des verschobenen Bildes
    cv2.imshow('Shifted Image', shifted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Fehler beim Laden des Bildes.")