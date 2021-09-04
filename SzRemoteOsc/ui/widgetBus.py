from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout,
                                QApplication, QHBoxLayout, QDial, QLineEdit, 
                                QSizePolicy, QScrollArea, QMenu, QTreeWidget,
                             QTreeWidgetItem, QAbstractItemView)
from PyQt5.QtGui import QPixmap, QImage


class widgetBus(QWidget):
    def __init__(self):
        super(widgetBus, self).__init__()
        self.load_ui()

    def load_ui(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        
    def minimumSizeHint(self) -> QSize:
        return QSize(500, 30)