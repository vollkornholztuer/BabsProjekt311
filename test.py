import cv2
from show import showImage


def draw_grid(img, block_size):
    """Draw a grid on the image with each cell of size block_size x block_size."""
    h, w = img.shape[:2]
    for x in range(0, w, block_size):
        cv2.line(img, (x, 0), (x, h), (200, 200, 200), 1, lineType=cv2.LINE_AA)
    for y in range(0, h, block_size):
        cv2.line(img, (0, y), (w, y), (200, 200, 200), 1, lineType=cv2.LINE_AA)
    return img

cap = cv2.VideoCapture(0)

# Global variables
dragging = False
start_x, start_y = -1, -1
selected_pixels = None
shifted_image = None
original_image = None
block_size = 50  # Change this variable to set the block size
underlay_memory = {}  # Dictionary to store the original state of blocks before moving

def webcam():
    while True:
        ret, frame = cap.read()
        
        frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        
        # show images 
        #cv2.imshow('testFrame', frame)
        #cv2.imshow("second Input", frame)
        
        cv2.imread('testFrame', frame)
        c = cv2.waitKey(1)
        if c == 27:
            break



# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global dragging, start_x, start_y, selected_pixels, shifted_image, block_size

    x, y = (x // block_size) * block_size, (y // block_size) * block_size  # Snap to grid
    if event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        start_x, start_y = x, y
        selected_pixels = shifted_image[y:y+block_size, x:x+block_size].copy()

    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        move_image(x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
        end_x, end_y = x, y
        move_block(start_x, start_y, end_x, end_y)

def move_block(start_x, start_y, end_x, end_y):
    global shifted_image, selected_pixels, block_size, underlay_memory
    if (end_x, end_y) != (start_x, start_y):
        if (end_x, end_y) not in underlay_memory:
            underlay_memory[(end_x, end_y)] = shifted_image[end_y:end_y+block_size, end_x:end_x+block_size].copy()
        shifted_image[end_y:end_y+block_size, end_x:end_x+block_size] = selected_pixels
        if (start_x, start_y) in underlay_memory:
            shifted_image[start_y:start_y+block_size, start_x:start_x+block_size] = underlay_memory.pop((start_x, start_y))
        else:
            shifted_image[start_y:start_y+block_size, start_x:start_x+block_size] = 0  # Black out the original spot

    draw_grid(shifted_image, block_size)
    cv2.imshow('Shifted Image', shifted_image)

def move_image(x, y):
    display_image = shifted_image.copy()
    display_image[y:y+block_size, x:x+block_size] = selected_pixels
    cv2.imshow('Shifted Image', display_image)


#showImage(cap)

# Load image and create a backup
while True:
    ret, frame = cap.read()
        
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)

    image_path = 'testImage.png'
    original_image =  cv2.imread('testFrame', frame)      #cv2.imread(image_path)
    shifted_image = original_image.copy()
    draw_grid(shifted_image, block_size)

if original_image is not None:
    cv2.imshow('Shifted Image', shifted_image)
    cv2.setMouseCallback('Shifted Image', mouse_callback)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
else:
    print("Error loading the image.")
