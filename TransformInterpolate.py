import cv2
import numpy as np

# Bild laden
image = cv2.imread('testImage.png')

if image is not None:
    # Bereich des Bildes definieren, auf den die Verschiebung angewendet werden soll
    x, y, w, h = 100, 100, 50, 50  # Beispielwerte für x, y, Breite und Höhe

    # Ausschnitt des Bildes extrahieren
    roi = image[y:y+h, x:x+w]

    # Neue Koordinaten für den Ausschnitt nach der Verschiebung
    new_x, new_y = 120, 120

    # Verschiebungsvektor berechnen
    dx, dy = new_x - x, new_y - y

    # Matrix für die Verschiebung erstellen
    M = np.float32([[1, 0, dx], [0, 1, dy]])

    # Ausschnitt des Bildes transformieren
    shifted_roi = cv2.warpAffine(roi, M, (w, h))

    # Den verschobenen Ausschnitt zurück in das ursprüngliche Bild einfügen
    image[y:y+h, x:x+w] = shifted_roi

    # Leere Bereiche im ursprünglichen Bild mit Durchschnitt der umliegenden Pixel füllen
    mask = np.zeros_like(image)
    mask[y:y+h, x:x+w] = 1
    blurred = cv2.blur(image, (5, 5))  # Anpassen der Größe des Filterkernels nach Bedarf
    image = image * (1 - mask) + blurred * mask

    # Anzeige des veränderten Bildes
    cv2.imshow('Shifted Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Fehler beim Laden des Bildes.")
