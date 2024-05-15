# Maigo was here
import sys
import cv2
import random
import threading

grid_size = 4

def split_frame(frame, height, width):
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
    

# cap = cv2.VideoCapture(0)

# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# width = int(width)
# height = int(height)
# print(width, height)

videoblocks_are_shuffled = False
frame_blocks_shuffeled = []

set_videoblocks_to_index = False
index_videoblock = []

changes_to_videoblock_order = []

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
print("Seed was:", seed)

# def async_video_feed():
#     while True:
#         ret, frame = cap.read()
#         cv2.imshow('testFrame', frame)

#         # index_videoblock = frame_blocks_original
#         frame_blocks_original = split_frame(frame)
        
#         frame_blocks_shuffeled = frame_blocks_original
#         random.Random(seed).shuffle(frame_blocks_shuffeled) # TODO: 
        
#         for change in changes_to_videoblock_order:
#             temp = frame_blocks_shuffeled[change[0]]
#             frame_blocks_shuffeled[change[0]] = frame_blocks_shuffeled[change[1]]
#             frame_blocks_shuffeled[change[1]] = temp
        
#         index_videoblock[0:16] = frame_blocks_shuffeled[0:16]
        
#         row1 = cv2.vconcat(index_videoblock[0:4])
#         row2 = cv2.vconcat(index_videoblock[4:8])
#         row3 = cv2.vconcat(index_videoblock[8:12])
#         row4 = cv2.vconcat(index_videoblock[12:16])
        
#         final = cv2.hconcat([row1, row2, row3, row4])
        
#         cv2.imshow('final', final)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break  # if the 'q' key is pressed, break from the loop

def async_input_videoblock_changes():
    while True:
    
        index_to_swap1 = input("Enter index to swap 1: ")
        index_to_swap2 = input("Enter index to swap 2: ")
        swap = (int(index_to_swap1), int(index_to_swap2))
        
        changes_to_videoblock_order.append(swap)

# Creating threads
# thread1 = threading.Thread(target=async_video_feed)
# thread2 = threading.Thread(target=async_input_videoblock_changes)

# Starting threads
# thread1.start()
# thread2.start()

def stitchBlocks(frame):
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