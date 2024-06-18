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

        
        case State.PuzzleDifficulty.IMPOSSIBLE:
            grid_size = 8
            
            frame_block_0_0 = frame[0:height//grid_size, 0:width//grid_size]
            frame_block_0_1 = frame[0:height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_0_2 = frame[0:height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_0_3 = frame[0:height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_0_4 = frame[0:height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_0_5 = frame[0:height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_0_6 = frame[0:height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_0_7 = frame[0:height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            frame_block_1_0 = frame[height//grid_size:2*height//grid_size, 0:width//grid_size]
            frame_block_1_1 = frame[height//grid_size:2*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_1_2 = frame[height//grid_size:2*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_1_3 = frame[height//grid_size:2*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_1_4 = frame[height//grid_size:2*height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_1_5 = frame[height//grid_size:2*height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_1_6 = frame[height//grid_size:2*height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_1_7 = frame[height//grid_size:2*height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            frame_block_2_0 = frame[2*height//grid_size:3*height//grid_size, 0:width//grid_size]
            frame_block_2_1 = frame[2*height//grid_size:3*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_2_2 = frame[2*height//grid_size:3*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_2_3 = frame[2*height//grid_size:3*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_2_4 = frame[2*height//grid_size:3*height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_2_5 = frame[2*height//grid_size:3*height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_2_6 = frame[2*height//grid_size:3*height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_2_7 = frame[2*height//grid_size:3*height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            frame_block_3_0 = frame[3*height//grid_size:4*height//grid_size, 0:width//grid_size]
            frame_block_3_1 = frame[3*height//grid_size:4*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_3_2 = frame[3*height//grid_size:4*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_3_3 = frame[3*height//grid_size:4*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_3_4 = frame[3*height//grid_size:4*height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_3_5 = frame[3*height//grid_size:4*height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_3_6 = frame[3*height//grid_size:4*height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_3_7 = frame[3*height//grid_size:4*height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            frame_block_4_0 = frame[4*height//grid_size:5*height//grid_size, 0:width//grid_size]
            frame_block_4_1 = frame[4*height//grid_size:5*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_4_2 = frame[4*height//grid_size:5*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_4_3 = frame[4*height//grid_size:5*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_4_4 = frame[4*height//grid_size:5*height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_4_5 = frame[4*height//grid_size:5*height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_4_6 = frame[4*height//grid_size:5*height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_4_7 = frame[4*height//grid_size:5*height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            frame_block_5_0 = frame[5*height//grid_size:6*height//grid_size, 0:width//grid_size]
            frame_block_5_1 = frame[5*height//grid_size:6*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_5_2 = frame[5*height//grid_size:6*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_5_3 = frame[5*height//grid_size:6*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_5_4 = frame[5*height//grid_size:6*height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_5_5 = frame[5*height//grid_size:6*height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_5_6 = frame[5*height//grid_size:6*height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_5_7 = frame[5*height//grid_size:6*height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            frame_block_6_0 = frame[6*height//grid_size:7*height//grid_size, 0:width//grid_size]
            frame_block_6_1 = frame[6*height//grid_size:7*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_6_2 = frame[6*height//grid_size:7*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_6_3 = frame[6*height//grid_size:7*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_6_4 = frame[6*height//grid_size:7*height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_6_5 = frame[6*height//grid_size:7*height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_6_6 = frame[6*height//grid_size:7*height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_6_7 = frame[6*height//grid_size:7*height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            frame_block_7_0 = frame[7*height//grid_size:8*height//grid_size, 0:width//grid_size]
            frame_block_7_1 = frame[7*height//grid_size:8*height//grid_size, width//grid_size:2*width//grid_size]
            frame_block_7_2 = frame[7*height//grid_size:8*height//grid_size, 2*width//grid_size:3*width//grid_size]
            frame_block_7_3 = frame[7*height//grid_size:8*height//grid_size, 3*width//grid_size:4*width//grid_size]
            frame_block_7_4 = frame[7*height//grid_size:8*height//grid_size, 4*width//grid_size:5*width//grid_size]
            frame_block_7_5 = frame[7*height//grid_size:8*height//grid_size, 5*width//grid_size:6*width//grid_size]
            frame_block_7_6 = frame[7*height//grid_size:8*height//grid_size, 6*width//grid_size:7*width//grid_size]
            frame_block_7_7 = frame[7*height//grid_size:8*height//grid_size, 7*width//grid_size:8*width//grid_size]
            
            return [frame_block_0_0, frame_block_0_1, frame_block_0_2, frame_block_0_3, frame_block_0_4, frame_block_0_5, frame_block_0_6, frame_block_0_7,
                    frame_block_1_0, frame_block_1_1, frame_block_1_2, frame_block_1_3, frame_block_1_4, frame_block_1_5, frame_block_1_6, frame_block_1_7,
                    frame_block_2_0, frame_block_2_1, frame_block_2_2, frame_block_2_3, frame_block_2_4, frame_block_2_5, frame_block_2_6, frame_block_2_7,
                    frame_block_3_0, frame_block_3_1, frame_block_3_2, frame_block_3_3, frame_block_3_4, frame_block_3_5, frame_block_3_6, frame_block_3_7,
                    frame_block_4_0, frame_block_4_1, frame_block_4_2, frame_block_4_3, frame_block_4_4, frame_block_4_5, frame_block_4_6, frame_block_4_7,
                    frame_block_5_0, frame_block_5_1, frame_block_5_2, frame_block_5_3, frame_block_5_4, frame_block_5_5, frame_block_5_6, frame_block_5_7,
                    frame_block_6_0, frame_block_6_1, frame_block_6_2, frame_block_6_3, frame_block_6_4, frame_block_6_5, frame_block_6_6, frame_block_6_7,
                    frame_block_7_0, frame_block_7_1, frame_block_7_2, frame_block_7_3, frame_block_7_4, frame_block_7_5, frame_block_7_6, frame_block_7_7]
            

                
    
    

def stitchBlocks(frame, changes_to_videoblock_order, puzzle_state):
    frame_blocks_shuffeled = frame
    random.Random(seed).shuffle(frame_blocks_shuffeled) # TODO: 
    
    for change in changes_to_videoblock_order:
        temp = frame_blocks_shuffeled[change[0]]
        frame_blocks_shuffeled[change[0]] = frame_blocks_shuffeled[change[1]]
        frame_blocks_shuffeled[change[1]] = temp
    
    match puzzle_state:
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
        
        case State.PuzzleDifficulty.IMPOSSIBLE:
            index_videoblock[0:64] = frame_blocks_shuffeled[0:64]
            
            row1 = cv2.vconcat(index_videoblock[0:8])
            row2 = cv2.vconcat(index_videoblock[8:16])
            row3 = cv2.vconcat(index_videoblock[16:24])
            row4 = cv2.vconcat(index_videoblock[24:32])
            row5 = cv2.vconcat(index_videoblock[32:40])
            row6 = cv2.vconcat(index_videoblock[40:48])
            row7 = cv2.vconcat(index_videoblock[48:56])
            row8 = cv2.vconcat(index_videoblock[56:64])
            
            final = cv2.hconcat([row1, row2, row3, row4, row5, row6, row7, row8])
            
            return final
 

def compareImages(image1, image2, threshold):
    '''
    threshold in percentage
    \n bla bla maggion
    '''
    difference = cv2.subtract(image1, image2)
    # print(difference)

    height, width, _ = difference.shape
    total_pixels = height * width
    non_zero_pixels = np.count_nonzero(difference)
    percentage_difference = (non_zero_pixels / total_pixels) * 100

    # threshold in percentage
    # alles kleiner als treshold is true
    # aka threshold is 50% -> 49% is true, 51% is false
    if percentage_difference <= threshold:
        return True
    else:
        return False