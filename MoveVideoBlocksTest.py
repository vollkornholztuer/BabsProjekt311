import sys
import cv2
import random
import numpy as np
from enum import Enum
import State
from PIL import Image # ONLY FOR DEBUGGING, REMOVE LATER


frame_blocks_shuffeled = []
index_videoblock = []

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
# print("Seed was:", seed)

def split_frame(frame, height, width, puzzle_state):    
    
    match puzzle_state:
        case State.PuzzleDifficulty.EASY:
            grid_size = 3
            
            frame_block_0_0 = frame[0:height//grid_size, 0:width//grid_size]
            frame_block_0_1 = frame[0:height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_0_2 = frame[0:height//grid_size, 2*width//grid_size:3*width//grid_size]
            
            img1 = Image.fromarray(frame_block_0_0)
            img2 = Image.fromarray(frame_block_0_1)
            img3 = Image.fromarray(frame_block_0_2)
            print("frame_block_0_0 - width:", img1.width, "height:", img1.height)
            print("frame_block_0_1 - width:", img2.width, "height:", img2.height)
            print("frame_block_0_2 - width:", img3.width, "height:", img3.height)
            print("combined width:", img1.width + img2.width + img3.width)
            
            
            frame_block_1_0 = frame[height//grid_size:2*height//grid_size, 0:width//grid_size]
            frame_block_1_1 = frame[height//grid_size:2*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_1_2 = frame[height//grid_size:2*height//grid_size, 2*width//grid_size:3*width//grid_size]
            
            img4 = Image.fromarray(frame_block_1_0)
            img5 = Image.fromarray(frame_block_1_1)
            img6 = Image.fromarray(frame_block_1_2)
            print("frame_block_1_0 - width:", img4.width, "height:", img4.height)
            print("frame_block_1_1 - width:", img5.width, "height:", img5.height)
            print("frame_block_1_2 - width:", img6.width, "height:", img6.height)
            print("combined width:", img4.width + img5.width + img6.width)
            
            
            frame_block_2_0 = frame[2*height//grid_size:3*height//grid_size, 0:width//grid_size]
            frame_block_2_1 = frame[2*height//grid_size:3*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_2_2 = frame[2*height//grid_size:3*height//grid_size, 2*width//grid_size:3*width//grid_size]
            img7 = Image.fromarray(frame_block_2_0)
            img8 = Image.fromarray(frame_block_2_1)
            img9 = Image.fromarray(frame_block_2_2)
            print("frame_block_2_0 - width:", img7.width, "height:", img7.height)
            print("frame_block_2_1 - width:", img8.width, "height:", img8.height)
            print("frame_block_2_2 - width:", img9.width, "height:", img9.height)
            print("combined width:", img7.width + img8.width + img9.width)
            
            return [frame_block_0_0, frame_block_0_1, frame_block_0_2,
                    frame_block_1_0, frame_block_1_1, frame_block_1_2,
                    frame_block_2_0, frame_block_2_1, frame_block_2_2]
            
            
        case State.PuzzleDifficulty.NORMAL:  
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
            
            
        case State.PuzzleDifficulty.HARD:
            grid_size = 5

            frame_block_0_0 = frame[0:height//grid_size, 0:width//grid_size]
            frame_block_0_1 = frame[0:height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_0_2 = frame[0:height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_0_3 = frame[0:height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_0_4 = frame[0:height//grid_size, 4*width//grid_size:5*width//grid_size]
            
            frame_block_1_0 = frame[height//grid_size:2*height//grid_size, 0:width//grid_size]
            frame_block_1_1 = frame[height//grid_size:2*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_1_2 = frame[height//grid_size:2*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_1_3 = frame[height//grid_size:2*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_1_4 = frame[height//grid_size:2*height//grid_size, 4*width//grid_size:5*width//grid_size]
            
            frame_block_2_0 = frame[2*height//grid_size:3*height//grid_size, 0:width//grid_size]
            frame_block_2_1 = frame[2*height//grid_size:3*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_2_2 = frame[2*height//grid_size:3*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_2_3 = frame[2*height//grid_size:3*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_2_4 = frame[2*height//grid_size:3*height//grid_size, 4*width//grid_size:5*width//grid_size]
            
            frame_block_3_0 = frame[3*height//grid_size:4*height//grid_size, 0:width//grid_size]
            frame_block_3_1 = frame[3*height//grid_size:4*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_3_2 = frame[3*height//grid_size:4*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_3_3 = frame[3*height//grid_size:4*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_3_4 = frame[3*height//grid_size:4*height//grid_size, 4*width//grid_size:5*width//grid_size]
            
            frame_block_4_0 = frame[4*height//grid_size:5*height//grid_size, 0:width//grid_size]
            frame_block_4_1 = frame[4*height//grid_size:5*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_4_2 = frame[4*height//grid_size:5*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_4_3 = frame[4*height//grid_size:5*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_4_4 = frame[4*height//grid_size:5*height//grid_size, 4*width//grid_size:5*width//grid_size]
            
            return [frame_block_0_0, frame_block_0_1, frame_block_0_2, frame_block_0_3, frame_block_0_4,
                    frame_block_1_0, frame_block_1_1, frame_block_1_2, frame_block_1_3, frame_block_1_4,
                    frame_block_2_0, frame_block_2_1, frame_block_2_2, frame_block_2_3, frame_block_2_4,
                    frame_block_3_0, frame_block_3_1, frame_block_3_2, frame_block_3_3, frame_block_3_4,
                    frame_block_4_0, frame_block_4_1, frame_block_4_2, frame_block_4_3, frame_block_4_4]
    
    
    

def stitchBlocks(frame, changes_to_videoblock_order, puzzle_state):
    frame_blocks_shuffeled = frame
    random.Random(seed).shuffle(frame_blocks_shuffeled) # TODO: 
    
    for change in changes_to_videoblock_order:
        temp = frame_blocks_shuffeled[change[0]]
        frame_blocks_shuffeled[change[0]] = frame_blocks_shuffeled[change[1]]
        frame_blocks_shuffeled[change[1]] = temp
    
    match puzzle_state:
        case State.PuzzleDifficulty.EASY:
            index_videoblock[0:9] = frame_blocks_shuffeled[0:9]
            # row1 = cv2.vconcat(index_videoblock[0:3])
            # row2 = cv2.vconcat(index_videoblock[3:6])
            # row3 = cv2.vconcat(index_videoblock[6:9])
            
            img1 = Image.fromarray(index_videoblock[0])
            img2 = Image.fromarray(index_videoblock[1])
            img3 = Image.fromarray(index_videoblock[2])
            img4 = Image.fromarray(index_videoblock[3])
            img5 = Image.fromarray(index_videoblock[4])
            img6 = Image.fromarray(index_videoblock[5])
            img7 = Image.fromarray(index_videoblock[6])
            img8 = Image.fromarray(index_videoblock[7])
            img9 = Image.fromarray(index_videoblock[8])
            print("index_videoblock[0] - width:", img1.width, "height:", img1.height)
            print("index_videoblock[1] - width:", img2.width, "height:", img2.height)
            print("index_videoblock[2] - width:", img3.width, "height:", img3.height)
            print("index_videoblock[3] - width:", img4.width, "height:", img4.height)
            print("index_videoblock[4] - width:", img5.width, "height:", img5.height)
            print("index_videoblock[5] - width:", img6.width, "height:", img6.height)
            print("index_videoblock[6] - width:", img7.width, "height:", img7.height)
            print("index_videoblock[7] - width:", img8.width, "height:", img8.height)
            print("index_videoblock[8] - width:", img9.width, "height:", img9.height)
            print("combined width:", img1.width + img2.width + img3.width)
            
            
            line1 = cv2.hconcat([index_videoblock[0], index_videoblock[3], index_videoblock[6]])
            line2 = cv2.hconcat([index_videoblock[1], index_videoblock[4], index_videoblock[7]])
            line3 = cv2.hconcat([index_videoblock[2], index_videoblock[5], index_videoblock[8]])
            
            #final = cv2.hconcat([row1, row2, row3])
            final = cv2.vconcat([line1, line2, line3])
            
            return final
        
        
        case State.PuzzleDifficulty.NORMAL:
            index_videoblock[0:16] = frame_blocks_shuffeled[0:16]
    
            row1 = cv2.vconcat(index_videoblock[0:4])
            row2 = cv2.vconcat(index_videoblock[4:8])
            row3 = cv2.vconcat(index_videoblock[8:12])
            row4 = cv2.vconcat(index_videoblock[12:16])
            
            final = cv2.hconcat([row1, row2, row3, row4])

            return final
        
        
        case State.PuzzleDifficulty.HARD:
            index_videoblock[0:25] = frame_blocks_shuffeled[0:25]
    
            row1 = cv2.vconcat(index_videoblock[0:5])
            row2 = cv2.vconcat(index_videoblock[5:10])
            row3 = cv2.vconcat(index_videoblock[10:15])
            row4 = cv2.vconcat(index_videoblock[15:20])
            row5 = cv2.vconcat(index_videoblock[20:25])
            
            final = cv2.hconcat([row1, row2, row3, row4, row5])

            return final
    
    

def compareImages(image1, image2):
    difference = cv2.subtract(image1, image2)
    # print(difference)
    if np.count_nonzero(difference) == 0:
        return True
    else:
        return False