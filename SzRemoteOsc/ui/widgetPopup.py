from os import stat
import re 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout,
                                QApplication, QHBoxLayout, QDial, QLineEdit, 
                                QSizePolicy, QScrollArea, QMenu)
from PyQt5.QtGui import QPixmap, QImage


class widgetPopupSetting(QWidget):
    requestConnectOsc = pyqtSignal()
    requestDisconnectOsc = pyqtSignal()

    def __init__(self, userSetting):
        super(widgetPopupSetting, self).__init__()
        self.userSetting = userSetting
        self.load_ui()

    def load_ui(self):
        mainLayout = QVBoxLayout()
        ipLayout = QVBoxLayout()
        portLayout = QVBoxLayout()
        addressLayout = QHBoxLayout()
        btnLayout = QHBoxLayout()

        lineEditorIPAddress = QLineEdit(objectName='lineEditorIPAddress')
        lineEditorIPAddress.setText(self.userSetting.value('ip'))
        lineEditorIPAddress.setFixedSize(QSize(250,24))
        
        lineEditorSocketPort = QLineEdit(objectName='lineEditorSocketPort')
        lineEditorSocketPort.setText(self.userSetting.value('port'))
        lineEditorSocketPort.setFixedSize(QSize(80,24))

        btnConnectOsc = QPushButton('Connect Oscilloscope', objectName='ConnectOscilloscope')
        btnConnectOsc.setEnabled(True)
        btnConnectOsc.clicked.connect(self.connectOsc)
        btnDisconnectOsc = QPushButton('Disconnect Oscilloscope', objectName='DisconnectOscilloscope')
        btnDisconnectOsc.setEnabled(False)
        btnDisconnectOsc.clicked.connect(self.disconnectOsc)

        ipLayout.addWidget(QLabel('IP'))
        ipLayout.addWidget(lineEditorIPAddress)
        ipLayout.setAlignment(Qt.AlignLeft)
        portLayout.addWidget(QLabel('Port'))
        portLayout.addWidget(lineEditorSocketPort)
        portLayout.setAlignment(Qt.AlignLeft)
        addressLayout.addLayout(ipLayout)
        addressLayout.addLayout(portLayout)
        addressLayout.setAlignment(Qt.AlignCenter)
        btnLayout.addWidget(btnConnectOsc)
        btnLayout.addWidget(btnDisconnectOsc)
        btnLayout.setAlignment(Qt.AlignCenter)
        mainLayout.addLayout(addressLayout)
        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(Qt.AlignCenter)

        self.setLayout(mainLayout)

    def connectOsc(self):
        if self.findChild(QLineEdit, 'lineEditorIPAddress').text() != '':
            self.userSetting.setValue('ip',self.findChild(QLineEdit, 'lineEditorIPAddress').text())
        if self.findChild(QLineEdit, 'lineEditorSocketPort').text() != '':
            self.userSetting.setValue('port',self.findChild(QLineEdit, 'lineEditorSocketPort').text())
        
        self.requestConnectOsc.emit()

    def disconnectOsc(self):
        self.requestDisconnectOsc.emit()

    def connectStatusUpdate(self, status):
        btnConnect = self.findChild(QPushButton, 'ConnectOscilloscope')
        btnDisconnect = self.findChild(QPushButton, 'DisconnectOscilloscope')
        btnConnect.setEnabled(not status)
        btnDisconnect.setEnabled(status)
