import pyzed.sl as sl
import numpy as np
import mediapipe as mp
import cv2

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
        image_ocv, frame = image_zed.get_data()
        depth_image_ocv = depth_image_zed.get_data()
        
        cv2.imshow("Image", image_ocv)
        cv2.imshow("Depth", depth_image_ocv)
        
        key = cv2.waitKey(10)
    
cv2.destroyAllWindows()
zed.close()