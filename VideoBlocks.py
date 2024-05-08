# Maigo was here
import sys
import cv2
import random

cap = cv2.VideoCapture(0)


width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = int(width)
height = int(height)
print(width, height)

grid_size = 10

videoblocks_are_shuffled = False
frame_blocks_shuffeled = []

set_videoblocks_to_index = False
index_videoblock = []

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
print("Seed was:", seed)

while True:
    ret, frame = cap.read()
    cv2.imshow('testFrame', frame)
    
    # frame[y1:y2, x1:x2]
    frame_block_0_0 = frame[0:height//grid_size, 0:width//grid_size]
    frame_block_0_1 = frame[0:height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_0_2 = frame[0:height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_0_3 = frame[0:height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_0_4 = frame[0:height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_0_5 = frame[0:height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_0_6 = frame[0:height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_0_7 = frame[0:height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_0_8 = frame[0:height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_0_9 = frame[0:height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_1_0 = frame[height//grid_size:2*height//grid_size, 0:width//grid_size]
    frame_block_1_1 = frame[height//grid_size:2*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_1_2 = frame[height//grid_size:2*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_1_3 = frame[height//grid_size:2*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_1_4 = frame[height//grid_size:2*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_1_5 = frame[height//grid_size:2*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_1_6 = frame[height//grid_size:2*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_1_7 = frame[height//grid_size:2*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_1_8 = frame[height//grid_size:2*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_1_9 = frame[height//grid_size:2*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_2_0 = frame[2*height//grid_size:3*height//grid_size, 0:width//grid_size]
    frame_block_2_1 = frame[2*height//grid_size:3*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_2_2 = frame[2*height//grid_size:3*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_2_3 = frame[2*height//grid_size:3*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_2_4 = frame[2*height//grid_size:3*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_2_5 = frame[2*height//grid_size:3*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_2_6 = frame[2*height//grid_size:3*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_2_7 = frame[2*height//grid_size:3*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_2_8 = frame[2*height//grid_size:3*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_2_9 = frame[2*height//grid_size:3*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_3_0 = frame[3*height//grid_size:4*height//grid_size, 0:width//grid_size]
    frame_block_3_1 = frame[3*height//grid_size:4*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_3_2 = frame[3*height//grid_size:4*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_3_3 = frame[3*height//grid_size:4*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_3_4 = frame[3*height//grid_size:4*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_3_5 = frame[3*height//grid_size:4*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_3_6 = frame[3*height//grid_size:4*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_3_7 = frame[3*height//grid_size:4*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_3_8 = frame[3*height//grid_size:4*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_3_9 = frame[3*height//grid_size:4*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_4_0 = frame[4*height//grid_size:5*height//grid_size, 0:width//grid_size]
    frame_block_4_1 = frame[4*height//grid_size:5*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_4_2 = frame[4*height//grid_size:5*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_4_3 = frame[4*height//grid_size:5*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_4_4 = frame[4*height//grid_size:5*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_4_5 = frame[4*height//grid_size:5*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_4_6 = frame[4*height//grid_size:5*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_4_7 = frame[4*height//grid_size:5*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_4_8 = frame[4*height//grid_size:5*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_4_9 = frame[4*height//grid_size:5*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_5_0 = frame[5*height//grid_size:6*height//grid_size, 0:width//grid_size]
    frame_block_5_1 = frame[5*height//grid_size:6*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_5_2 = frame[5*height//grid_size:6*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_5_3 = frame[5*height//grid_size:6*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_5_4 = frame[5*height//grid_size:6*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_5_5 = frame[5*height//grid_size:6*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_5_6 = frame[5*height//grid_size:6*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_5_7 = frame[5*height//grid_size:6*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_5_8 = frame[5*height//grid_size:6*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_5_9 = frame[5*height//grid_size:6*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_6_0 = frame[6*height//grid_size:7*height//grid_size, 0:width//grid_size]
    frame_block_6_1 = frame[6*height//grid_size:7*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_6_2 = frame[6*height//grid_size:7*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_6_3 = frame[6*height//grid_size:7*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_6_4 = frame[6*height//grid_size:7*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_6_5 = frame[6*height//grid_size:7*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_6_6 = frame[6*height//grid_size:7*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_6_7 = frame[6*height//grid_size:7*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_6_8 = frame[6*height//grid_size:7*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_6_9 = frame[6*height//grid_size:7*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_7_0 = frame[7*height//grid_size:8*height//grid_size, 0:width//grid_size]
    frame_block_7_1 = frame[7*height//grid_size:8*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_7_2 = frame[7*height//grid_size:8*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_7_3 = frame[7*height//grid_size:8*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_7_4 = frame[7*height//grid_size:8*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_7_5 = frame[7*height//grid_size:8*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_7_6 = frame[7*height//grid_size:8*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_7_7 = frame[7*height//grid_size:8*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_7_8 = frame[7*height//grid_size:8*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_7_9 = frame[7*height//grid_size:8*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_8_0 = frame[8*height//grid_size:9*height//grid_size, 0:width//grid_size]
    frame_block_8_1 = frame[8*height//grid_size:9*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_8_2 = frame[8*height//grid_size:9*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_8_3 = frame[8*height//grid_size:9*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_8_4 = frame[8*height//grid_size:9*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_8_5 = frame[8*height//grid_size:9*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_8_6 = frame[8*height//grid_size:9*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_8_7 = frame[8*height//grid_size:9*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_8_8 = frame[8*height//grid_size:9*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_8_9 = frame[8*height//grid_size:9*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_block_9_0 = frame[9*height//grid_size:10*height//grid_size, 0:width//grid_size]
    frame_block_9_1 = frame[9*height//grid_size:10*height//grid_size, width//grid_size:2*width//grid_size]
    frame_block_9_2 = frame[9*height//grid_size:10*height//grid_size, 2*width//grid_size:3*width//grid_size]
    frame_block_9_3 = frame[9*height//grid_size:10*height//grid_size, 3*width//grid_size:4*width//grid_size]
    frame_block_9_4 = frame[9*height//grid_size:10*height//grid_size, 4*width//grid_size:5*width//grid_size]
    frame_block_9_5 = frame[9*height//grid_size:10*height//grid_size, 5*width//grid_size:6*width//grid_size]
    frame_block_9_6 = frame[9*height//grid_size:10*height//grid_size, 6*width//grid_size:7*width//grid_size]
    frame_block_9_7 = frame[9*height//grid_size:10*height//grid_size, 7*width//grid_size:8*width//grid_size]
    frame_block_9_8 = frame[9*height//grid_size:10*height//grid_size, 8*width//grid_size:9*width//grid_size]
    frame_block_9_9 = frame[9*height//grid_size:10*height//grid_size, 9*width//grid_size:10*width//grid_size]
    
    frame_blocks_original = [
        frame_block_0_0, frame_block_0_1, frame_block_0_2, frame_block_0_3, frame_block_0_4, frame_block_0_5, frame_block_0_6, frame_block_0_7, frame_block_0_8, frame_block_0_9,
        frame_block_1_0, frame_block_1_1, frame_block_1_2, frame_block_1_3, frame_block_1_4, frame_block_1_5, frame_block_1_6, frame_block_1_7, frame_block_1_8, frame_block_1_9,
        frame_block_2_0, frame_block_2_1, frame_block_2_2, frame_block_2_3, frame_block_2_4, frame_block_2_5, frame_block_2_6, frame_block_2_7, frame_block_2_8, frame_block_2_9,
        frame_block_3_0, frame_block_3_1, frame_block_3_2, frame_block_3_3, frame_block_3_4, frame_block_3_5, frame_block_3_6, frame_block_3_7, frame_block_3_8, frame_block_3_9,
        frame_block_4_0, frame_block_4_1, frame_block_4_2, frame_block_4_3, frame_block_4_4, frame_block_4_5, frame_block_4_6, frame_block_4_7, frame_block_4_8, frame_block_4_9,
        frame_block_5_0, frame_block_5_1, frame_block_5_2, frame_block_5_3, frame_block_5_4, frame_block_5_5, frame_block_5_6, frame_block_5_7, frame_block_5_8, frame_block_5_9,
        frame_block_6_0, frame_block_6_1, frame_block_6_2, frame_block_6_3, frame_block_6_4, frame_block_6_5, frame_block_6_6, frame_block_6_7, frame_block_6_8, frame_block_6_9,
        frame_block_7_0, frame_block_7_1, frame_block_7_2, frame_block_7_3, frame_block_7_4, frame_block_7_5, frame_block_7_6, frame_block_7_7, frame_block_7_8, frame_block_7_9,
        frame_block_8_0, frame_block_8_1, frame_block_8_2, frame_block_8_3, frame_block_8_4, frame_block_8_5, frame_block_8_6, frame_block_8_7, frame_block_8_8, frame_block_8_9,
        frame_block_9_0, frame_block_9_1, frame_block_9_2, frame_block_9_3, frame_block_9_4, frame_block_9_5, frame_block_9_6, frame_block_9_7, frame_block_9_8, frame_block_9_9
    ]

    # index_videoblock = frame_blocks_original
    frame_blocks_shuffeled = frame_blocks_original
    random.Random(seed).shuffle(frame_blocks_shuffeled)
    
    index_videoblock[0:10] = frame_blocks_shuffeled[0:10]
    index_videoblock[10:20] = frame_blocks_shuffeled[10:20]
    index_videoblock[20:30] = frame_blocks_shuffeled[20:30]
    index_videoblock[30:40] = frame_blocks_shuffeled[30:40]
    index_videoblock[40:50] = frame_blocks_shuffeled[40:50]
    index_videoblock[50:60] = frame_blocks_shuffeled[50:60]
    index_videoblock[60:70] = frame_blocks_shuffeled[60:70]
    index_videoblock[70:80] = frame_blocks_shuffeled[70:80]
    index_videoblock[80:90] = frame_blocks_shuffeled[80:90]
    index_videoblock[90:100] = frame_blocks_shuffeled[90:100]
    
    cv2.imshow('test1', index_videoblock[0])
    
    final1 = cv2.vconcat(index_videoblock[0:10])
    final2 = cv2.vconcat(index_videoblock[10:20])
    final3 = cv2.vconcat(index_videoblock[20:30])
    final4 = cv2.vconcat(index_videoblock[30:40])
    final5 = cv2.vconcat(index_videoblock[40:50])
    final6 = cv2.vconcat(index_videoblock[50:60])
    final7 = cv2.vconcat(index_videoblock[60:70])
    final8 = cv2.vconcat(index_videoblock[70:80])
    final9 = cv2.vconcat(index_videoblock[80:90])
    final10 = cv2.vconcat(index_videoblock[90:100])
    

    final = cv2.hconcat([final1, final2, final3, final4, final5, final6, final7, final8, final9, final10])
    
    cv2.imshow('finalFrame', final)
                        
    

    
    
    
      
    # frame_block_tl = frame[0:height//2,      0:width//2]
    # frame_block_tr = frame[0:height//2,      width//2:width]
    # frame_block_bl = frame[height//2:height, 0:width//2]
    # frame_block_br = frame[height//2:height, width//2:width]
    
    # final1 = cv2.hconcat([frame_block_tr, frame_block_tl])
    # final2 = cv2.hconcat([frame_block_bl, frame_block_br])
    
    # final = cv2.vconcat([final1, final2])
    
    # cv2.imshow('testFrame', final)
    
    # cv2.imshow('test1', frame_block_tl)
    # cv2.imshow('test2', frame_block_tr)
    # cv2.imshow('test3', frame_block_bl)
    # cv2.imshow('test4', frame_block_br)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
