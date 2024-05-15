import cv2
import numpy as np
import math

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
        selected_pixels = image[y-10:y+10, x-10:x+10].copy()  # Auswahl von 10x10 Pixel um den Mauszeiger
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
        shifted_image[start_y-10:start_y+10, start_x-10:start_x+10] = 0  # Setze ursprüngliche Pixel auf Schwarz
        shifted_image[y-10:y+10, x-10:x+10] = selected_pixels  # Setze ausgewählte Pixel an die neue Position
        cv2.imshow('Shifted Image', shifted_image)
    else:
        print("Bitte wählen Sie zuerst einen Bereich aus.")

# Bild laden
image = cv2.imread('testImage.png')

if image is not None:
    
    height, width, channels = image.shape
    
    phi = 0 #wird durch mausdrag ersetzt
    sign = 1 # erlaubt wellen
    while True:
        
        shifted_image = image.copy()
        phi = phi + 0.1 * sign
        if phi > math.pi :
            if sign > 0 :
                sign = -1
            else:
                sign = 1
        for y in range( height //4,height-height //4 ):
            if y < height//2:
                A = 20 * (y - height/4)/height*4
            else: 
                A = 20 * (3 * height/4 - y)/height*4
            source_y = round( y +  A* math.cos(2* math.pi * y / height + phi))
            for x in range(width): 
                
                shifted_image[y, x] = image[source_y, x]
        
            print(source_y, y)
        cv2.imshow('Shifted Image', shifted_image)
        cv2.imshow("original", image)
    
    # cv2.setMouseCallback('Shifted Image', mouse_callback)

    
        key = cv2.waitKey(1) 
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
else:
    print("Fehler beim Laden des Bildes.")