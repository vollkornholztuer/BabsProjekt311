import cv2
import numpy as np

# Funktion zur Anwendung des Filters auf ein Bild
def apply_filter(frame):
    kernel = np.ones((3,3), np.float32) * (-1)
    kernel[1,1] = 8
    return cv2.filter2D(frame, -1, kernel)

# Hauptfunktion
def main():
    # Öffnen der Webcam
    cap = cv2.VideoCapture(0)

    # Überprüfen, ob die Webcam geöffnet wurde
    if not cap.isOpened():
        print("Error: Unable to open webcam")
        return

    # Schleife zum Lesen von Frames von der Webcam
    while True:
        # Lesen eines Frames von der Webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from webcam")
            break

        # Anwenden des Filters auf den Frame
        filtered_frame = apply_filter(frame)

        # Anzeigen des Originalrahmens und des gefilterten Rahmens
        cv2.imshow('Original', frame)
        cv2.imshow('Filtered', filtered_frame)

        # Warten auf das Drücken der Taste 'q', um die Schleife zu beenden
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Freigeben der Ressourcen
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()