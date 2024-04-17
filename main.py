import pyzed.sl as sl
import numpy as np
import cv2

# Create a ZED camera
zed = sl.Camera()
init_params = sl.InitParameters()
init_params.sdk_verbose = True # Enable verbose logging
init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE # Set the depth mode to performance (fastest)
init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use millimeter units

# Open the camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Error {}, exit program".format(err)) # Display the error
    exit()
    
    
# Capture 50 images and depth, then stop
i = 0
image = sl.Mat()
depth = sl.Mat()
# point_cloud = sl.Mat()
runtime_parameters = sl.RuntimeParameters()
while True:
    # Grab an image
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        # A new image is available if grab() returns sl.ERROR_CODE.SUCCESS
        zed.retrieve_image(image, sl.VIEW.LEFT) # Get the left image
        zed.retrieve_measure(depth, sl.MEASURE.DEPTH) # Retrieve depth matrix. Depth is aligned on the left RGB image
        # zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA) # Retrieve colored point cloud
        # i = i + 1
        image_ocv = depth.get_data()
        # Display the left image from the numpy array
        cv2.imshow("Image", image_ocv)
        cv2.waitKey(1)