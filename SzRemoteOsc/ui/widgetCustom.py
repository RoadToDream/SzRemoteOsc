from os import name
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QGridLayout, QButtonGroup, QMainWindow, QSpinBox
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout, QFrame, 
                                QApplication, QHBoxLayout, QDial, QLineEdit, 
                                QSizePolicy, QScrollArea, QMenu, QTreeWidget, 
                                QTreeWidgetItem, QStyle, QAbstractItemView)
from PyQt5.QtGui import QPixmap, QImage


class spinBoxWithPresetDelayedSignal(QDoubleSpinBox):
    valueChangedDelayed = pyqtSignal(float)
    def __init__(self,acceptedValues,decimals, objectName):
        super().__init__(objectName=objectName)
        self.acceptedValues = acceptedValues
        self.setDecimals(decimals)
        self.setRange(self.acceptedValues[0],self.acceptedValues[-1])
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.valueChanged.connect(self.startTimer)
        self.timer.timeout.connect(self.emitValueChanged)
    
    def startTimer(self):
        self.timer.start()

    def stepBy(self, steps: int):
        index = max(0,self.acceptedValues.index(self.value()) + steps)% len(self.acceptedValues)
        self.setValue(self.acceptedValues[index])

    def textFromValue(self, value):
        return "{:.3E}".format(value)

    def valueFromTex(self, text):
        return float(text)

    def emitValueChanged(self):
        self.valueChangedDelayed.emit(self.value())

class spinBoxDelayedSignal(QDoubleSpinBox):
    valueChangedDelayed = pyqtSignal(float)
    mouseStartPos = 0
    startValue = 0

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.valueChanged.connect(self.startTimer)
        self.timer.timeout.connect(self.emitValueChanged)

    def startTimer(self):
        self.timer.start()

    def textFromValue(self, value):
        return "{:.3E}".format(value)

    def valueFromTex(self, text):
        return float(text)

    def mousePressEvent(self, e):
        super(spinBoxDelayedSignal, self).mousePressEvent(e)
        if e.button() == Qt.MiddleButton:
            self.setValue(0)
        self.mouseStartPos = e.pos().y()
        self.startValue = self.value()
    
    def mouseMoveEvent(self, e):
        self.setCursor(Qt.SizeVerCursor)
        valueOffset = int((self.mouseStartPos-e.pos().y()))*self.singleStep()
        self.setValue(self.startValue+valueOffset)
        return super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        super(spinBoxDelayedSignal,self).mouseReleaseEvent(e)
        self.unsetCursor()

    def emitValueChanged(self):
        self.valueChangedDelayed.emit(self.value())

class sectionButton(QPushButton):
    def __init__(self, item, text = "", parent = None):
        super().__init__(text, parent)
        self.notExpandedIcon = self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay'))
        self.ExpandedIcon = self.style().standardIcon(getattr(QStyle, 'SP_TitleBarUnshadeButton'))
        self.setStyleSheet("text-align:left;background-color: #AAAAAA;")
        self.section = item
        self.clicked.connect(self.on_clicked)
        self.setFocusPolicy(Qt.NoFocus)
        self.setIcon(self.ExpandedIcon if self.section.isExpanded() else self.notExpandedIcon)

    def on_clicked(self):
        self.section.setExpanded(not self.section.isExpanded())
        self.setIcon((self.ExpandedIcon if self.section.isExpanded() else self.notExpandedIcon))

    

