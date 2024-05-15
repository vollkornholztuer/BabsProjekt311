import cv2
import numpy as np

# Globale Variablen zur Verwendung im Callback
dragging = False
start_x, start_y = -1, -1
selected_pixels = None

# Mouse Callback Funktion
def mouse_callback(event, x, y, flags, param):
    global dragging, start_x, start_y, selected_pixels

    if event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        start_x, start_y = x, y
        selected_pixels = image[y-5:y+5, x-5:x+5].copy()  # Auswahl von 10x10 Pixel um den Mauszeiger
    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging:
            move_image(x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False

# Funktion zum Verschieben des ausgewählten 10x10 Pixelbereichs
def move_image(x, y):
    global image, shifted_image, selected_pixels
    if selected_pixels is not None:  
        # Berechne Verschiebung
        dx = x - start_x
        dy = y - start_y
        # Verschiebe ausgewählte Pixel
        shifted_image = image.copy()
        shifted_image[start_y-5:start_y+5, start_x-5:start_x+5] = 0  # Setze ursprüngliche Pixel auf Schwarz
        shifted_image[y-5:y+5, x-5:x+5] = selected_pixels  # Setze ausgewählte Pixel an die neue Position
        cv2.imshow('Shifted Image', shifted_image)
    else:
        print("Bitte wählen Sie zuerst einen Bereich aus.")

# Bild laden
image = cv2.imread('testImage.png')
shifted_image = image.copy()

if image is not None:
    cv2.imshow('Shifted Image', shifted_image)
    cv2.setMouseCallback('Shifted Image', mouse_callback)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
else:
    print("Fehler beim Laden des Bildes.")