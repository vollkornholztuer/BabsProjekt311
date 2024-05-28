from PIL import Image
import cv2
import numpy as np

def get_square_index(dragging_point, height, width):
    grid_size = 4
    square_height = height // grid_size
    square_width = width // grid_size

    col = dragging_point[1] // square_height
    row = dragging_point[0] // square_width
    
    return row * grid_size + col

def highlight_square(frame, square_index, height, width):
    grid_size = 4
    square_height = height // grid_size
    square_width = width // grid_size

    col = square_index // grid_size
    row = square_index % grid_size

    top_left = (col * square_width, row * square_height)
    bottom_right = ((col + 1) * square_width, (row + 1) * square_height)

    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)