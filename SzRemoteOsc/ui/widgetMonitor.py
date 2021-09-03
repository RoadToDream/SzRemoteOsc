from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout,
                                QApplication, QHBoxLayout, QDial, QLineEdit, 
                                QSizePolicy, QScrollArea, QMenu)
from PyQt5.QtGui import QPixmap, QImage

class widgetMonitor(QWidget):
    requestRemoteFrame = pyqtSignal()

    def __init__(self, serverThreadConfig):
        super(widgetMonitor, self).__init__()
        self.setupTimer()
        self.connectActions(serverThreadConfig)
        self.load_ui()

    def setupTimer(self):
        self.timer = QTimer()

    def load_ui(self):
        layout = QHBoxLayout()
        self.labelMonitor = QLabel(objectName='labelMonitor')
        layout.addWidget(self.labelMonitor)
        self.setLayout(layout)

    def connectActions(self,serverThreadConfig):
        serverThreadConfig.resultFrame.connect(self.updateFrame)
        self.requestRemoteFrame.connect(serverThreadConfig.DISPlayOUTPut)
        self.timer.timeout.connect(self.remoteFrameRequested)

    
    def minimumSizeHint(self) -> QSize:
        return QSize(800, 480)

    def startUpdate(self):
        self.timer.start(1000. / 8)
        self.inRequest = False

    def stopUpdate(self):
        self.timer.stop()
        self.inRequest = False


    def remoteFrameRequested(self):
        if self.inRequest == False:
            self.inRequest=True
            self.requestRemoteFrame.emit()

    @pyqtSlot(QImage)
    def updateFrame(self,image):
        self.inRequest = False
        pixmap = QPixmap.fromImage(image)
        self.labelMonitor.setPixmap(pixmap.scaled(self.labelMonitor.width(),self.labelMonitor.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation))

    