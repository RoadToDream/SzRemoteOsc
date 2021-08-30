import ctypes
import numpy as np
import pyvisa as visa
from PyQt5.QtGui import QImage
import cv2 
import time

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

setting = {'ip': '192.168.0.127', 'port': '3080'}
resourceManager = visa.ResourceManager()
ipAddress = setting['ip']+"::"+setting['port']
dev = 'TCPIP0::'+ipAddress+'::SOCKET'
session = resourceManager.open_resource(dev)
session.read_termination = '\n'

start = time.time()
length = 800*480*3
data = bytes(bytearray(b'\x00'*length))
pdata = ctypes.create_string_buffer(data, length)
libc = ctypes.cdll.LoadLibrary('../SzRemoteOsc/lib/libparseOutput.dylib')

for i in range(20):
    dataRec = session.query_binary_values(':DISPlay:OUTPut?', datatype='c')
    dataToC = b''.join(dataRec)
    pToC = ctypes.create_string_buffer(dataToC, len(dataRec))
    libc.parseOutput(pToC, pdata, len(dataRec))
    im = np.frombuffer(
        pdata.raw, dtype=np.uint8).reshape((480, 800, 3))
    image = QImage(displayModify(im, 0.52, 10, 30), im.shape[1], im.shape[0], QImage.Format.Format_BGR888)
    end = time.time()
    print(1/(end-start))
    start = end
