from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout,
                                QApplication, QHBoxLayout, QDial, QLineEdit, 
                                QSizePolicy, QScrollArea, QMenu)
from PyQt5.QtGui import QPixmap, QImage

class widgetTrigger(QWidget):
    def __init__(self):
        super(widgetTrigger, self).__init__()

    def minimumSizeHint(self) -> QSize:
        return QSize(500, 30)