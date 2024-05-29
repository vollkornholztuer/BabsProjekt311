import sys
import cv2
import random
import numpy as np

frame_blocks_shuffeled = []
index_videoblock = []

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
# print("Seed was:", seed)

def split_frame(frame, height, width):
    grid_size = 4

    frame_block_0_0 = frame[0:height//grid_size, 0:width//grid_size]
    frame_block_0_1 = frame[0:height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_0_2 = frame[0:height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_0_3 = frame[0:height//grid_size, 3*width//grid_size:4*width//grid_size]
    
    frame_block_1_0 = frame[height//grid_size:2*height//grid_size, 0:width//grid_size]
    frame_block_1_1 = frame[height//grid_size:2*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_1_2 = frame[height//grid_size:2*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_1_3 = frame[height//grid_size:2*height//grid_size, 3*width//grid_size:4*width//grid_size]
    
    frame_block_2_0 = frame[2*height//grid_size:3*height//grid_size, 0:width//grid_size]
    frame_block_2_1 = frame[2*height//grid_size:3*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_2_2 = frame[2*height//grid_size:3*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_2_3 = frame[2*height//grid_size:3*height//grid_size, 3*width//grid_size:4*width//grid_size]
    
    frame_block_3_0 = frame[3*height//grid_size:4*height//grid_size, 0:width//grid_size]
    frame_block_3_1 = frame[3*height//grid_size:4*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_3_2 = frame[3*height//grid_size:4*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_3_3 = frame[3*height//grid_size:4*height//grid_size, 3*width//grid_size:4*width//grid_size]
    
    return [frame_block_0_0, frame_block_0_1, frame_block_0_2, frame_block_0_3,
            frame_block_1_0, frame_block_1_1, frame_block_1_2, frame_block_1_3,
            frame_block_2_0, frame_block_2_1, frame_block_2_2, frame_block_2_3,
            frame_block_3_0, frame_block_3_1, frame_block_3_2, frame_block_3_3]

def stitchBlocks(frame, changes_to_videoblock_order):
    frame_blocks_shuffeled = frame
    random.Random(seed).shuffle(frame_blocks_shuffeled) # TODO: 
    
    for change in changes_to_videoblock_order:
        temp = frame_blocks_shuffeled[change[0]]
        frame_blocks_shuffeled[change[0]] = frame_blocks_shuffeled[change[1]]
        frame_blocks_shuffeled[change[1]] = temp
    
    index_videoblock[0:16] = frame_blocks_shuffeled[0:16]
    
    row1 = cv2.vconcat(index_videoblock[0:4])
    row2 = cv2.vconcat(index_videoblock[4:8])
    row3 = cv2.vconcat(index_videoblock[8:12])
    row4 = cv2.vconcat(index_videoblock[12:16])
    
    final = cv2.hconcat([row1, row2, row3, row4])

    return final

def compareImages(image1, image2):
    difference = cv2.subtract(image1, image2)
    # print(difference)
    if np.count_nonzero(difference) == 0:
        return True
    else:
        return False