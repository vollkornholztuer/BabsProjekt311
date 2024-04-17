import pyzed.sl as sl
import numpy as np
import mediapipe as mp
import cv2

# initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Create a ZED camera
zed = sl.Camera()

# Set configuration parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD1080 # Set the camera resolution to HD1080
init_params.camera_fps = 30 # Set the camera FPS to 30
init_params.sdk_verbose = True # Enable verbose logging
init_params.depth_mode = sl.DEPTH_MODE.NEURAL_PLUS # Set the depth mode to performance (fastest)
init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use millimeter units

# Open the camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Error {}, exit program".format(err)) # Display the error
    zed.close()
    exit(1)
    
# Set runtime paramters after opening the camera
runtime_parameters = sl.RuntimeParameters()
runtime_parameters.enable_fill_mode = True # Enable the fill mode

# set image size
image_size = zed.get_camera_information().camera_configuration.resolution
    
# declare sl.Mat matrices
image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
depth_image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    
while True:
    err = zed.grab(runtime_parameters)
    if err == sl.ERROR_CODE.SUCCESS :
        # retrieve left image
        zed.retrieve_image(image_zed, sl.VIEW.LEFT, sl.MEM.CPU, image_size)
        zed.retrieve_image(depth_image_zed, sl.VIEW.DEPTH, sl.MEM.CPU, image_size)
        
        # To recover data from sl.Mat to use it with opencv, use the get_data() method
        # It returns a numpy array that can be used as a matrix with opencv
        image_ocv = image_zed.get_data() # 'frame' is for mediapipe
        depth_image_ocv = depth_image_zed.get_data()
        
        # MEDIAPIPE HAND RECOGNITION HAPPENING
        # frame to RGB
        results = hands.process(cv2.cvtColor(image_ocv, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks: # Check if there are hands detected
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_list = []
                for i, landmark in enumerate(hand_landmarks.landmark):
                    
                    
                    if i <= 20:
                        x1 = int(landmark.x * image_ocv.shape[1])
                        y1 = int(landmark.y * image_ocv.shape[0])
                        
                        landmarks_list.append((x1, y1))
                        
                        if i == 0: # Check if the landmark is the wrist
                            cv2.circle(image_ocv, (x1, y1), 5, (255, 0, 0), -1)
                        else:
                            cv2.circle(image_ocv, (x1, y1), 5, (0, 0, 255), -1)
                            
                        cv2.putText(image_ocv, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        
                    if i < 20:
                        landmark_next = hand_landmarks.landmark[i+1]
                        
                    x2 = int(landmark_next.x * image_ocv.shape[1])
                    y2 = int(landmark_next.y * image_ocv.shape[0])
                    
                    if i%4 != 0:
                        cv2.line(image_ocv, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                    if i == 1 or i == 5 or i == 17:
                        x0 = int(hand_landmarks.landmark[0].x * image_ocv.shape[1])
                        y0 = int(hand_landmarks.landmark[0].y * image_ocv.shape[0])
                        cv2.line(image_ocv, (x1, y1), (x0, y0), (0, 255, 0), 2)
                        
                # 13 and 17
                cv2.line(image_ocv, (landmarks_list[13][0], landmarks_list[13][1]), (landmarks_list[17][0], landmarks_list[17][1]), (0, 255, 0), 2)
                # 5 und 9
                cv2.line(image_ocv, (landmarks_list[5][0], landmarks_list[5][1]), (landmarks_list[9][0], landmarks_list[9][1]), (0, 255, 0), 2)
                # 9 und 13
                cv2.line(image_ocv, (landmarks_list[9][0], landmarks_list[9][1]), (landmarks_list[13][0], landmarks_list[13][1]), (0, 255, 0), 2)
        
        cv2.imshow("Image", image_ocv)
        cv2.imshow("Depth", depth_image_ocv)
        
        key = cv2.waitKey(10)
    
cv2.destroyAllWindows()
zed.close()