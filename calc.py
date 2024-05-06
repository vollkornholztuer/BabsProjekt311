import numpy as np
from PIL import Image
import cv2
from show import showImage

def render(res):
    w,h = res
    x,y = np.arange(-w//2, w//2)*4*2*np.pi/w, np.arange(-h//2, h//2)*4*2*np.pi/h  # chosen to have some repeats
    r = np.sin(np.outer(x,y)*y)  # np.outer generates the complete matrix for the red channel
    g = np.cos(y)*np.cos(np.outer(x,y)) # green
    b = np.cos(np.outer(x,y)+np.pi) # blue
    img = (np.array((r, g, b))*128+127).transpose(1,2,0).astype(np.uint8) # no alpha this time
    
    pilimg = Image.fromarray(img, 'RGB')
    #pilimg.save('result.jpg')
    #if __name__ == '__main__':    
        #render(res=(500, 500))
    
    cap = Image.fromarray(img, 'RGB')
    showImage(cap)
