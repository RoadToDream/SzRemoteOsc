import os
from pathlib import Path
import re
import sys
from time import sleep
import threading

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal, pyqtSlot, QSettings, QSize, QMetaObject
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout,
                                QApplication, QHBoxLayout, QDial, QLineEdit, 
                                QSizePolicy, QScrollArea, QMenu, QMessageBox, 
                                QFileDialog)

from PyQt5.QtGui import QPixmap, QImage

from PyQtAds import QtAds

if sys.platform == 'darwin':
    os.environ['QT_MAC_WANTS_LAYER'] = '1'

from remoteOscServer import remoteOscServer
import ui

class SzRemoteOscMain(QMainWindow):
    requestConnectionStatus = pyqtSignal(object,threading.Event)
    requestDisconnectOsc = pyqtSignal(threading.Event)
    requestCompleteConfig = pyqtSignal()
    connectStatus = False

    def __init__(self):
        super(SzRemoteOscMain, self).__init__()

        self.setupTimer()
        self.setupServer()
        self.createMenuBar()
        self.load_ui()
        self.connectActions()
        self.show()
        
    def setupTimer(self):
        self.timerConfigUpdate = QTimer()

    def setupServer(self):
        self.serverThread=QThread()
        self.serverThreadConfig=remoteOscServer(self.getUserSetting())
    
    def createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        self.fileMenu = menuBar.addMenu("&File")
        self.connectionMenu = menuBar.addMenu("&Connection")
        self.windowMenu = menuBar.addMenu("&Window")

    def load_ui(self):
        self.m_DockManager = QtAds.CDockManager()
        
        dockWidgetMonitor = self.createDockWidgetMonitor()
        dockWidgetMainControl = self.createDockWidgetMainControl()
        dockWidgetTrigger = self.createDockWidgetTrigger()
        dockWidgetMath = self.createDockWidgetMath()
        dockWidgetRef = self.createDockWidgetRef()
        dockWidgetBus = self.createDockWidgetBus()
        dockWidgetMeasure = self.createDockWidgetMeasure()

        monitorArea = self.m_DockManager.addDockWidget(QtAds.TopDockWidgetArea, dockWidgetMonitor)
        configArea = self.m_DockManager.addDockWidget(QtAds.RightDockWidgetArea, dockWidgetMainControl)
        self.m_DockManager.addDockWidget(QtAds.CenterDockWidgetArea, dockWidgetTrigger, configArea)
        self.m_DockManager.addDockWidget(QtAds.CenterDockWidgetArea, dockWidgetMath, configArea)
        self.m_DockManager.addDockWidget(QtAds.CenterDockWidgetArea, dockWidgetRef, configArea)
        self.m_DockManager.addDockWidget(QtAds.CenterDockWidgetArea, dockWidgetBus, configArea)
        self.m_DockManager.addDockWidget(QtAds.CenterDockWidgetArea, dockWidgetMeasure, configArea)
        configArea.setCurrentIndex(0)

        self.setCentralWidget(self.m_DockManager)

        self.widgetPopupSetting = ui.widgetPopupSetting(self.getUserSetting())

        self.setWindowTitle('SzRemoteOsc')

        self.widgetMonitor.setDisabled(True)
        self.widgetMainControl.setDisabled(True)
        self.widgetTrigger.setDisabled(True)
        self.widgetMath.setDisabled(True)
        self.widgetRef.setDisabled(True)
        self.widgetBus.setDisabled(True)
        self.widgetMeasure.setDisabled(True)

    
    def connectActions(self):

        fileSaveImageAction = QAction("&Save Image", self)
        connectionAction = QAction("&Connect", self)

        fileSaveImageAction.triggered.connect(self.showSaveImagePanel)
        connectionAction.triggered.connect(self.showConnectionPanel)

        self.fileMenu.addAction(fileSaveImageAction)
        self.connectionMenu.addAction(connectionAction) 

        self.widgetPopupSetting.requestConnectOsc.connect(self.connectOsc)
        self.widgetPopupSetting.requestDisconnectOsc.connect(self.disconnectOsc)

        self.requestConnectionStatus.connect(self.serverThreadConfig.status)
        self.requestDisconnectOsc.connect(self.serverThreadConfig.stop)
        self.requestCompleteConfig.connect(self.serverThreadConfig.requestCompleteConfig)

        self.serverThreadConfig.resultCompleteConfig.connect(self.update)
        self.serverThreadConfig.connectionError.connect(self.notifyConnectError)

        self.timerConfigUpdate.timeout.connect(self.requestCompleteConfig)

    def closeEvent(self, event):
        self.disconnectOsc()
        self.widgetPopupSetting.close()
        event.accept()

    def showSaveImagePanel(self):
        self.getUserSetting()
        if self.userSetting.value('pathSaveImage') is None:
            if sys.platform == 'darwin':
                desktopPath = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/untitled.png') 
            elif sys.platform == 'win32':
                desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/untitled.png')
            self.userSetting.setValue('pathSaveImage',desktopPath)


        imagePath = QFileDialog().getSaveFileName(self,'Save Image',self.userSetting.value('pathSaveImage'), filter="Images (*.png *.jpg)")
        if imagePath[0] != '':
            pixmapRemoteDisplay = self.findChild(QLabel,name='labelMonitor').pixmap()
            self.userSetting.setValue('pathSaveImage',imagePath[0])
            if pixmapRemoteDisplay:
                pixmapRemoteDisplay.save(imagePath[0])

            
    def showConnectionPanel(self):
        self.widgetPopupSetting.show()
        
    def createDockWidgetMonitor(self) -> QtAds.CDockWidget:
        dockWidgetMonitor = QtAds.CDockWidget('Monitor')
        self.widgetMonitor = ui.widgetMonitor(self.serverThreadConfig)
        dockWidgetMonitor.setWidget(self.widgetMonitor, QtAds.CDockWidget.ForceNoScrollArea)
        dockWidgetMonitor.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromContent)
        self.windowMenu.addAction(dockWidgetMonitor.toggleViewAction())
        return dockWidgetMonitor
        
    def createDockWidgetMainControl(self) -> QtAds.CDockWidget:
        dockWidgetMainControl = QtAds.CDockWidget('Main')
        self.widgetMainControl = ui.widgetMainControl(self.serverThreadConfig)
        dockWidgetMainControl.setWidget(self.widgetMainControl, QtAds.CDockWidget.ForceNoScrollArea)
        dockWidgetMainControl.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromContent)
        self.windowMenu.addAction(dockWidgetMainControl.toggleViewAction())
        return dockWidgetMainControl
        
    def createDockWidgetTrigger(self) -> QtAds.CDockWidget:
        dockWidgetTrigger = QtAds.CDockWidget('Trigger')
        self.widgetTrigger = ui.widgetTrigger()
        dockWidgetTrigger.setWidget(self.widgetTrigger, QtAds.CDockWidget.ForceNoScrollArea)
        dockWidgetTrigger.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromContent)
        self.windowMenu.addAction(dockWidgetTrigger.toggleViewAction())
        return dockWidgetTrigger
        
    def createDockWidgetMath(self) -> QtAds.CDockWidget:
        dockWidgetMath = QtAds.CDockWidget('Math')
        self.widgetMath = ui.widgetMath()
        dockWidgetMath.setWidget(self.widgetMath, QtAds.CDockWidget.ForceNoScrollArea)
        dockWidgetMath.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromContent)
        self.windowMenu.addAction(dockWidgetMath.toggleViewAction())
        return dockWidgetMath
        
    def createDockWidgetRef(self) -> QtAds.CDockWidget:
        dockWidgetRef = QtAds.CDockWidget('Ref')
        self.widgetRef = ui.widgetRef()
        dockWidgetRef.setWidget(self.widgetRef, QtAds.CDockWidget.ForceNoScrollArea)
        dockWidgetRef.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromContent)
        self.windowMenu.addAction(dockWidgetRef.toggleViewAction())
        return dockWidgetRef
        
    def createDockWidgetBus(self) -> QtAds.CDockWidget:
        dockWidgetBus = QtAds.CDockWidget('Bus')
        self.widgetBus = ui.widgetBus()
        dockWidgetBus.setWidget(self.widgetBus, QtAds.CDockWidget.ForceNoScrollArea)
        dockWidgetBus.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromContent)
        self.windowMenu.addAction(dockWidgetBus.toggleViewAction())
        return dockWidgetBus
        
    def createDockWidgetMeasure(self) -> QtAds.CDockWidget:
        dockWidgetMeasure = QtAds.CDockWidget('Measure')
        self.widgetMeasure = ui.widgetMeasure()
        dockWidgetMeasure.setWidget(self.widgetMeasure, QtAds.CDockWidget.ForceNoScrollArea)
        dockWidgetMeasure.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromContent)
        self.windowMenu.addAction(dockWidgetMeasure.toggleViewAction())
        return dockWidgetMeasure

    def getUserSetting(self) -> object:
        self.userSetting= QSettings('RoadToDreamTech','SzRemoteOsc')
        userIP = self.userSetting.value('ip')
        userPort = self.userSetting.value('port')
        if userIP is None:
            self.userSetting.setValue('ip','192.168.0.128')
        if userPort is None:
            self.userSetting.setValue('port','3000')
        return self.userSetting

    @pyqtSlot()
    def connectOsc(self):
        if not self.connectStatus:
            status = [False]
            self.event = threading.Event()
            self.serverThreadConfig.setting = self.getUserSetting()
            self.serverThread.started.connect(self.serverThreadConfig.start)
            self.serverThreadConfig.moveToThread(self.serverThread)
            self.serverThread.start()
            self.requestConnectionStatus.emit(status,self.event)
            self.event.wait()
            
            if status[0]:
                self.widgetMonitor.setEnabled(True)
                self.widgetMainControl.setEnabled(True)
                self.widgetTrigger.setEnabled(True)
                self.widgetMath.setEnabled(True)
                self.widgetRef.setEnabled(True)
                self.widgetBus.setEnabled(True)
                self.widgetMeasure.setEnabled(True)
                self.startUpdate()
                self.connectStatus = status[0]
                self.getCompleteConfig()
            else:
                self.serverThread.quit()
                self.serverThread.wait()
            self.widgetPopupSetting.connectStatusUpdate(status[0])

    
    def disconnectOsc(self):
        if self.connectStatus:
            self.widgetMonitor.stopUpdate()
            self.event = threading.Event()
            self.requestDisconnectOsc.emit(self.event)
            self.event.wait()
            self.widgetPopupSetting.connectStatusUpdate(False)
            self.serverThread.quit()
            self.serverThread.wait()
            self.connectStatus = False

    @pyqtSlot()
    def notifyConnectError(self):
        msgError = QMessageBox()
        msgError.setIcon(QMessageBox.Warning)
        msgError.setText('Connection Error')
        msgError.setInformativeText('Unable to connect to oscilloscope, please check \n 1. Your oscilloscope\'s ethernet cable connection. \n2. IP address and port on your oscilloscope.')
        msgError.exec()

    def getCompleteConfig(self):
        self.requestCompleteConfig.emit()

    def startUpdate(self):
        self.widgetMonitor.startUpdate()
        self.timerConfigUpdate.start(1000)
        
    def stopUpdate(self):
        self.widgetMonitor.stopUpdate()
        self.timerConfigUpdate.stop()

    @pyqtSlot(object)
    def update(self,serverConfig):
        self.widgetMainControl.update(serverConfig)

if __name__ == '__main__':
    app = QApplication([])
    widget=SzRemoteOscMain()
    widget.show()
    sys.exit(app.exec())