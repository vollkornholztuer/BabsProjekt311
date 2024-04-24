import cv2
import mediapipe as mp
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

gestureRecognizerModelPath = "mpModels/gesture_recognizer.task"
print(gestureRecognizerModelPath)

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print(result.gestures)
    
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=gestureRecognizerModelPath),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
    # Recognizer is initialized. Use it here
    
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Ignoring empty camera frame.")
            break
    
        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()