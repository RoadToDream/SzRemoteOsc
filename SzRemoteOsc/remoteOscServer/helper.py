import cv2 
import numpy as np

def displayModify(inputImg, gamma = 1, brightness = 0, contrast = 0):
    LUT = np.empty((1,256), np.uint8)
    for i in range(256):
        LUT[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    inputImg=cv2.LUT(inputImg,LUT)
    if brightness > 0:
        shadow = brightness
        highlight = 255
    else:
        shadow = 0
        highlight = 255 + brightness
    alpha_b = (highlight - shadow)/255
    gamma_b = shadow
    inputImg = cv2.addWeighted(inputImg, alpha_b, inputImg, 0, gamma_b)
    f = 131*(contrast + 127)/(127*(131-contrast))
    alpha_c = f
    gamma_c = 127*(1-f)
    inputImg = cv2.addWeighted(inputImg, alpha_c, inputImg, 0, gamma_c)
    return inputImg
