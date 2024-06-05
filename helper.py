from PIL import Image, ImageSequence
import cv2
import numpy as np
import State

def get_square_index(dragging_point, height, width, puzzle_state):
    
    grid_size = 0
    match puzzle_state:
        case State.PuzzleDifficulty.NORMAL:
            grid_size = 4
        case State.PuzzleDifficulty.HARD:
            grid_size = 5
        case State.PuzzleDifficulty.IMPOSSIBLE:
            grid_size = 8
    
    square_height = height // grid_size
    square_width = width // grid_size

    col = dragging_point[1] // square_height
    row = dragging_point[0] // square_width
    
    return row * grid_size + col

def highlight_square(frame, square_index, height, width, puzzle_state):
    
    grid_size = 0
    match puzzle_state:
        case State.PuzzleDifficulty.NORMAL:
            grid_size = 4
        case State.PuzzleDifficulty.HARD:
            grid_size = 5
        case State.PuzzleDifficulty.IMPOSSIBLE:
            grid_size = 8
    
    square_height = height // grid_size
    square_width = width // grid_size

    col = square_index // grid_size
    row = square_index % grid_size

    top_left = (col * square_width, row * square_height)
    bottom_right = ((col + 1) * square_width, (row + 1) * square_height)

    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)

def indicator_image(frame, image, width):
    size = width // 8
    image = cv2.resize(image, (size, size))
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Create a binary mask where the black regions are opaque
    ret, mask = cv2.threshold(img2gray, 150, 255, cv2.THRESH_BINARY_INV)

    roi = frame[10:size+10, width-size-10:width-10]
    
    # Set an index of where the mask is
    roi[np.where(mask)] = 0
    roi += image 

    return frame

def load_gif(gif_path):
    gif = Image.open(gif_path)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert('RGBA')  # Ensure it's in RGBA mode
        frames.append(frame)
    return frames

def resize_and_load_gif(gif_path):
    gif = Image.open(gif_path)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert('RGBA')  # Ensure it's in RGBA mode
        width, height = frame.size
        frame = frame.resize((width // 2, height // 2))
        frames.append(frame)
    return frames

def overlay_gif_on_frame(video_frame, gif_frame, position=(0, 0), resize_factor=0.3):
    gif_np = np.array(gif_frame)  # Convert PIL Image to numpy array
    
    # Separate the color and alpha channels
    gif_bgra = cv2.cvtColor(gif_np, cv2.COLOR_RGBA2BGRA)  # Convert RGBA to BGRA
    gif_rgb = gif_bgra[..., :3]
    gif_alpha = gif_bgra[..., 3] / 255.0
    
    x, y = position
    
    # Resize the GIF frame
    gif_rgb = cv2.resize(gif_rgb, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_AREA)
    gif_alpha = cv2.resize(gif_alpha, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_AREA)
    
    # Update position based on the resized GIF dimensions
    h, w, _ = gif_rgb.shape
    x = max(0, min(x, video_frame.shape[1] - w))
    y = max(0, min(y, video_frame.shape[0] - h))
    
    overlay = np.zeros_like(video_frame)
    overlay[y:y+h, x:x+w] = gif_rgb
    
    alpha = np.zeros_like(video_frame[:, :, 0], dtype=float)
    alpha[y:y+h, x:x+w] = gif_alpha
    
    # Composite the gif onto the video frame using the alpha mask
    result_frame = video_frame * (1 - alpha[..., None]) + overlay * alpha[..., None]
    result_frame = result_frame.astype(np.uint8)
    return result_frame