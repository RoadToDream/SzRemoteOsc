import ctypes
from time import sleep
import numpy as np
import pyvisa as visa
import sys
import os
import json
import threading

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, qRgb

from .helper import displayModify
from common import lrnParser


class remoteOscServer(QObject):
    resultFrame = pyqtSignal(QImage)
    resultACQuireMEMory = pyqtSignal(object)
    resultConfig = pyqtSignal(object)
    resultCompleteConfig = pyqtSignal(object)
    connectionError = pyqtSignal()

    def __init__(self, setting):
        super().__init__()
        self.setting = setting
        self.image = QImage(800,480,QImage.Format.Format_RGB888)
        self.image.fill(qRgb(255,255,255))

    def resourcePath(self,relativePath):
        try:
            root = sys._MEIPASS
        except Exception:
            root = os.path.abspath(".")
        return os.path.join(root, relativePath)

    @pyqtSlot()
    def start(self):
        try:
            self.resourceManager = visa.ResourceManager()
            ipAddress = self.setting.value('ip')+"::"+self.setting.value('port')
            dev = 'TCPIP0::'+ipAddress+'::SOCKET'
            self.session = self.resourceManager.open_resource(dev)
            self.session.read_termination = '\n'
            self.session.clear()


            length = 800*480*3
            self.data = bytes(bytearray(b'\x00'*length))
            self.pdata = ctypes.create_string_buffer(self.data, length)
            if sys.platform == 'darwin':
                self.libc = ctypes.cdll.LoadLibrary(self.resourcePath('lib/libparseOutput.dylib'))
            elif sys.platform == 'win32':
                self.libc = ctypes.cdll.LoadLibrary(self.resourcePath('lib/libparseOutput.dll'))

        except Exception as e:
            print(e.args)
        with open(self.resourcePath('oscProtocol/GWInstekGDS1000B.json')) as fp:
            self.protocolConfig = json.load(fp)

    @pyqtSlot(threading.Event)
    def stop(self, event):
        try:
            self.session.clear()
            self.resourceManager.close()
            event.set()
        except:
            event.set()

    @pyqtSlot(object,threading.Event)
    def status(self,status,events):
        try:
            self.session.query('*IDN?')
            status[0] = True
            events.set()
        except:
            status[0] = False
            events.set()
            self.connectionError.emit()


    @pyqtSlot()
    def requestCompleteConfig(self):
        self.session.clear()
        result = self.session.query('*LRN?')
        config = lrnParser.lrnParser(result)
        self.resultCompleteConfig.emit(config)

    @pyqtSlot(str, object)
    def request(self, protocolName, parameter):
        protocol=self.protocolConfig[protocolName]
        parameterNumber = len(protocol["Protocol"])
        if len(parameter) != parameterNumber:
            return

        command = ''
        for i in range(parameterNumber-1):
            command += protocol["Protocol"][i]["Prefix"]+parameter[i]
        
        command += protocol["Protocol"][-1]["Prefix"]
        command += parameter[-1] if parameter[-1] == '?' else ' '+parameter[-1]

        if parameter[-1] == '?':
            result = self.session.query(command)
            self.resultConfig.emit([protocol["Name"],result])
        else:
            self.session.write(command)

    @pyqtSlot()
    def DISPlayOUTPut(self):
        self.session.clear()
        try:
            dataRec = self.session.query_binary_values(
            ':DISPlay:OUTPut?', datatype='c')
            dataToC = b''.join(dataRec)
            pToC = ctypes.create_string_buffer(dataToC, len(dataRec))
            self.libc.parseOutput(pToC, self.pdata, len(dataRec))
            im = np.frombuffer(
                self.pdata.raw, dtype=np.uint8).reshape((480, 800, 3))
            self.image = QImage(displayModify(im, 0.52, 10, 30),
                        im.shape[1], im.shape[0], QImage.Format.Format_RGB888).convertToFormat(QImage.Format_ARGB32)
            self.resultFrame.emit(self.image)
        except:
            self.resultFrame.emit(self.image)

    @pyqtSlot(str)
    def ACQuireMEMory(self, channel):
        self.session.clear()
        self.session.write(':HEADer ON')
        resultAscii = self.session.query(':ACQuire'+channel+':MEMory?')
        resultBin = self.session.read_binary_values(
            datatype='h', is_big_endian=True, container=np.ndarray)

        headerList = dict(item.split(',') for item in resultAscii.split(';')[0:23])
        self.resultACQuireMEMory.emit((headerList, resultBin))
