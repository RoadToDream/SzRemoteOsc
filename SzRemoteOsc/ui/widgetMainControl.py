from os import name
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QGridLayout, QButtonGroup, QMainWindow, QSpinBox
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout, QFrame, 
                                QApplication, QHBoxLayout, QDial, QLineEdit, 
                                QSizePolicy, QScrollArea, QMenu, QTreeWidget, 
                                QTreeWidgetItem, QStyle, QAbstractItemView)
from PyQt5.QtGui import QPixmap, QImage
from .widgetCustom import *

class widgetMainControl(QWidget):
    def __init__(self,serverThreadConfig):
        super(widgetMainControl, self).__init__()
        self.load_ui()
        self.connectActions(serverThreadConfig)
        self.update()

    def load_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        tree = QTreeWidget()
        tree.setIndentation(0)
        tree.setColumnCount(1)
        tree.setHeaderHidden(True)
        tree.setSelectionMode(QAbstractItemView.NoSelection)
        tree.setFocusPolicy(Qt.NoFocus)
        items = []
        self.sections = [('Shortcut',widgetSectionShortcut()),
                    ('Vertical',widgetSectionChannelVerticalScale()),
                    ('Control',widgetSectionChannelControl()),
                    ('Timebase',widgetSectionTimebase())]
        for i in range(len(self.sections)):
            item = QTreeWidgetItem()
            child = QTreeWidgetItem()
            item.addChild(child)
            items.append([item,child])
            
        tree.insertTopLevelItems(0,[ x[0] for x in items])

        for i,item in enumerate(items):
            tree.setItemWidget(item[1],0,self.sections[i][1])
            item[0].setExpanded(True)
            tree.setItemWidget(item[0],0,sectionButton(item[0],self.sections[i][0]))

        mainLayout.addWidget(tree)
        self.setLayout(mainLayout)

    def connectActions(self,serverThreadConfig):
        for section in self.sections:
            section[1].request.connect(serverThreadConfig.request)

    def update(self,serverConfig={}):
        self.serverConfig = serverConfig
        if not serverConfig == {}:   
            for section in self.sections:
                section[1].update(serverConfig)

    
    def minimumSizeHint(self) -> QSize:
        return QSize(500, 30)

class widgetSectionShortcut(QWidget):
    request = pyqtSignal(str,object)

    def __init__(self):
        super(widgetSectionShortcut, self).__init__()
        self.load_ui()
        self.setFocusPolicy(Qt.NoFocus)
        self.connectActions()
        self.update()

    def load_ui(self):
        mainLayout = QHBoxLayout()
        self.btnAutoSet = QPushButton('AutoSet', objectName='AutoSet')
        self.btnRun = QPushButton('Run', objectName='Run')
        self.btnStop = QPushButton('Stop', objectName='Stop')
        self.btnSingle = QPushButton('Single', objectName='Single')

        mainLayout.addWidget(self.btnAutoSet)
        mainLayout.addWidget(self.btnRun)
        mainLayout.addWidget(self.btnStop)
        mainLayout.addWidget(self.btnSingle)
        self.setLayout(mainLayout)
    
    def connectActions(self):
        self.btnAutoSet.clicked.connect(self.autoset)
        self.btnRun.clicked.connect(self.run)
        self.btnStop.clicked.connect(self.stop)
        self.btnSingle.clicked.connect(self.single)

    def update(self,serverConfig={}):
        return

    def autoset(self):
        self.request.emit('AUTOSet',[' '])
    
    def run(self):
        self.request.emit('RUN',[' '])

    def stop(self):
        self.request.emit('STOP',[' '])
        
    def single(self):
        self.request.emit('SINGle',[' '])
    

class widgetSectionChannelVerticalScale(QWidget):
    request = pyqtSignal(str,object)
    holdUpdate = False
    enableUpdate = True

    def __init__(self):
        super(widgetSectionChannelVerticalScale, self).__init__()
        self.load_ui()
        self.setFocusPolicy(Qt.NoFocus)
        self.connectActions()
        self.update()

    def load_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5, 5, 0, 5)
        channelEnableLayout = QGridLayout()
        channelEnableLayout.setHorizontalSpacing(3)

        self.checkboxChannelDisplay = []
        self.spinboxChannelPosition = []
        self.spinboxChannelScale = []

        for i in range(1,8):
            if i%2 == 1:
                channelVerticalWidget = QWidget()
                channelVerticalWidgetLayout = QVBoxLayout()
                self.checkboxChannelDisplay.append(QCheckBox())
                self.spinboxChannelPosition.append(spinBoxDelayedSignal())
                self.spinboxChannelScale.append(spinBoxWithPresetDelayedSignal([1e-3,2e-3,5e-3,1e-2,2e-2,5e-2,1e-1,2e-1,5e-1,1e0,2e0,5e0,1e1],3,objectName='CHANnel'+str(int((i+1)/2))+'SCALe'))
                
                # self.spinboxChannelPosition[int((i-1)/2)].setDecimals(3)
                self.spinboxChannelPosition[int((i-1)/2)].setRange(-125,125)
                self.spinboxChannelPosition[int((i-1)/2)].lineEdit().setReadOnly(True)

                self.spinboxChannelScale[int((i-1)/2)].lineEdit().setReadOnly(True)

                channelVerticalWidgetLayout.addWidget(QLabel('Channel'+str(int((i+1)/2))),alignment=Qt.AlignHCenter)
                channelVerticalWidgetLayout.addWidget(self.checkboxChannelDisplay[int((i-1)/2)],alignment=Qt.AlignHCenter)
                channelVerticalWidgetLayout.addWidget(QLabel('Position'))
                channelVerticalWidgetLayout.addWidget(self.spinboxChannelPosition[int((i-1)/2)],alignment=Qt.AlignHCenter)

                channelVerticalWidgetLayout.addWidget(QLabel('Scale'))
                channelVerticalWidgetLayout.addWidget(self.spinboxChannelScale[int((i-1)/2)],alignment=Qt.AlignHCenter)
                channelVerticalWidget.setLayout(channelVerticalWidgetLayout)
                channelEnableLayout.addWidget(channelVerticalWidget,1,i)
                channelEnableLayout.setColumnStretch(i,50)
            else:
                separator = QWidget()
                separator.setStyleSheet('background-color: #CCCCCC;')
                channelEnableLayout.addWidget(separator,1,i,-1,1)
                channelEnableLayout.setColumnStretch(i,0)
                channelEnableLayout.setColumnMinimumWidth(i,2)

        mainLayout.addLayout(channelEnableLayout)
        self.setLayout(mainLayout)
        
    def connectActions(self):
        self.checkboxChannelDisplay[0].toggled.connect(self.channel1Display)
        self.checkboxChannelDisplay[1].toggled.connect(self.channel2Display)
        self.checkboxChannelDisplay[2].toggled.connect(self.channel3Display)
        self.checkboxChannelDisplay[3].toggled.connect(self.channel4Display)
        self.spinboxChannelPosition[0].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelPosition[1].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelPosition[2].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelPosition[3].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelPosition[0].valueChangedDelayed.connect(self.channel1Position)
        self.spinboxChannelPosition[1].valueChangedDelayed.connect(self.channel2Position)
        self.spinboxChannelPosition[2].valueChangedDelayed.connect(self.channel3Position)
        self.spinboxChannelPosition[3].valueChangedDelayed.connect(self.channel4Position)
        self.spinboxChannelScale[0].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelScale[1].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelScale[2].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelScale[3].valueChanged.connect(self.disableUpdate)
        self.spinboxChannelScale[0].valueChangedDelayed.connect(self.channel1Scale)
        self.spinboxChannelScale[1].valueChangedDelayed.connect(self.channel2Scale)
        self.spinboxChannelScale[2].valueChangedDelayed.connect(self.channel3Scale)
        self.spinboxChannelScale[3].valueChangedDelayed.connect(self.channel4Scale)
    
    def disableUpdate(self):
        self.holdUpdate = True
        self.enableUpdate = False

    def update(self, serverConfig={}):
        if self.holdUpdate:
            self.enableUpdate = True
            return
        if not self.enableUpdate:
            return 
        if not serverConfig == {}:
            for i in range(4):
                self.checkboxChannelDisplay[i].blockSignals(True)
                self.spinboxChannelPosition[i].blockSignals(True)
                self.spinboxChannelScale[i].blockSignals(True)
                self.checkboxChannelDisplay[i].setCheckState(Qt.Checked if serverConfig[':CHANnel CH'+str(int(i+1))+':DISPlay'] == 'ON' else Qt.Unchecked)
                self.spinboxChannelPosition[i].setSingleStep(float(serverConfig[':CHANnel CH'+str(int(i+1))+':SCALe'])/25)
                self.spinboxChannelPosition[i].setValue(float(serverConfig[':CHANnel CH'+str(int(i+1))+':POSition']))
                self.spinboxChannelScale[i].setValue(float(serverConfig[':CHANnel CH'+str(int(i+1))+':SCALe']))
                self.checkboxChannelDisplay[i].blockSignals(False)
                self.spinboxChannelPosition[i].blockSignals(False)
                self.spinboxChannelScale[i].blockSignals(False)

    def channel1Display(self,state):
        self.request.emit('CHANnelDISPlay',['1','ON' if state else 'OFF'])

    def channel2Display(self,state):
        self.request.emit('CHANnelDISPlay',['2','ON' if state else 'OFF'])

    def channel3Display(self,state):
        self.request.emit('CHANnelDISPlay',['3','ON' if state else 'OFF'])

    def channel4Display(self,state):
        self.request.emit('CHANnelDISPlay',['4','ON' if state else 'OFF'])

    def channel1Position(self,pos):
        self.request.emit('CHANnelPOSition',['1',str(pos)])
        self.holdUpdate = False

    def channel2Position(self,pos):
        self.request.emit('CHANnelPOSition',['2',str(pos)])
        self.holdUpdate = False

    def channel3Position(self,pos):
        self.request.emit('CHANnelPOSition',['3',str(pos)])
        self.holdUpdate = False

    def channel4Position(self,pos):
        self.request.emit('CHANnelPOSition',['4',str(pos)])
        self.holdUpdate = False

    def channel1Scale(self,scale):
        self.request.emit('CHANnelSCALe',['1',str(scale)])

    def channel2Scale(self,scale):
        self.request.emit('CHANnelSCALe',['2',str(scale)])

    def channel3Scale(self,scale):
        self.request.emit('CHANnelSCALe',['3',str(scale)])

    def channel4Scale(self,scale):
        self.request.emit('CHANnelSCALe',['4',str(scale)])

class widgetSectionChannelControl(QWidget):
    request = pyqtSignal(str,object)
    serverConfig = {}
    holdUpdate = False
    enableUpdate = True
    def __init__(self):
        super(widgetSectionChannelControl, self).__init__()
        self.load_ui()
        self.setFocusPolicy(Qt.NoFocus)
        self.connectActions()
        self.update()

    def load_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5, 5, 0, 5)

        self.channelSelectionGroup = QButtonGroup(self,objectName = 'channelSelectionGroup')
        channelSelectionLayout = QHBoxLayout()
        for i in range(1,5):
            btn = QPushButton('CH'+str(i),objectName='channelSelectionCH'+str(i))
            btn.setCheckable(True)
            channelSelectionLayout.addWidget(btn)
            self.channelSelectionGroup.addButton(btn)

        channelControlLayout = QGridLayout()

        couplingList = ['DC','AC','GND']
        self.comboboxChannelCoupling = QComboBox()
        self.comboboxChannelCoupling.addItems(couplingList)
        

        invertList = ['On','Off']
        self.comboboxChannelInvert = QComboBox()
        self.comboboxChannelInvert.addItems(invertList)

        bwList = ['Full','20MHz']
        self.comboboxChannelBW = QComboBox()
        self.comboboxChannelBW.addItems(bwList)

        expandList = ['Ground','Center']
        self.comboboxChannelExpand = QComboBox()
        self.comboboxChannelExpand.addItems(expandList)


        channelControlLayout.addWidget(QLabel('Coupling'),1,1)
        channelControlLayout.addWidget(self.comboboxChannelCoupling,2,1)
        channelControlLayout.addWidget(QLabel('Invert'),1,2)
        channelControlLayout.addWidget(self.comboboxChannelInvert,2,2)
        channelControlLayout.addWidget(QLabel('BW'),1,3)
        channelControlLayout.addWidget(self.comboboxChannelBW,2,3)
        channelControlLayout.addWidget(QLabel('Expand'),1,4)
        channelControlLayout.addWidget(self.comboboxChannelExpand,2,4)

        channelProbeControlLayout = QGridLayout()

        probetypeList = ['Voltage','Current']
        self.comboboxProbeType = QComboBox()
        self.comboboxProbeType.addItems(probetypeList)

        self.spinboxProbeAttenuation = spinBoxWithPresetDelayedSignal([0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000]
                                                    ,3,objectName='1')
        self.spinboxProbeAttenuation.lineEdit().setReadOnly(True)

        self.spinboxDeskew = QDoubleSpinBox()
        self.spinboxDeskew.setRange(-50,50)
        self.spinboxDeskew.setDecimals(2)
        self.spinboxDeskew.setSingleStep(0.01)
        self.spinboxDeskew.lineEdit().setReadOnly(True)

        channelProbeControlLayout.addWidget(QLabel('Probe Type'),1,1)
        channelProbeControlLayout.addWidget(self.comboboxProbeType,2,1)
        channelProbeControlLayout.addWidget(QLabel('Probe Attenuation'),1,2)
        channelProbeControlLayout.addWidget(self.spinboxProbeAttenuation,2,2)
        channelProbeControlLayout.addWidget(QLabel('*Probe Deskew/ns'),1,3)
        channelProbeControlLayout.addWidget(self.spinboxDeskew,2,3)
        channelProbeControlLayout.setColumnStretch(1,10)
        channelProbeControlLayout.setColumnStretch(2,15)
        channelProbeControlLayout.setColumnStretch(3,15)

        mainLayout.addLayout(channelSelectionLayout)
        mainLayout.addLayout(channelControlLayout)
        mainLayout.addLayout(channelProbeControlLayout)

        self.setLayout(mainLayout)
        self.findChild(QPushButton,name='channelSelectionCH1').setChecked(True)

    def connectActions(self):
        self.channelSelectionGroup.buttonClicked.connect(self.updateChannel)
        self.comboboxChannelCoupling.currentTextChanged.connect(self.channelCoupling)
        self.comboboxChannelInvert.currentTextChanged.connect(self.channelInvert)
        self.comboboxChannelBW.currentTextChanged.connect(self.channelBW)
        self.comboboxChannelExpand.currentTextChanged.connect(self.channelExpand)
        self.comboboxProbeType.currentTextChanged.connect(self.channelType)
        self.spinboxProbeAttenuation.valueChanged.connect(self.disableUpdate)
        self.spinboxProbeAttenuation.valueChangedDelayed.connect(self.channelAttenuation)
        self.spinboxDeskew.valueChanged.connect(self.channelDeskew)

    def updateChannel(self):
        self.channel = -(self.channelSelectionGroup.checkedId())-1
        self.update()

    def disableUpdate(self):
        self.holdUpdate = True
        self.enableUpdate = False

    def update(self,serverConfig={}):
        if self.holdUpdate:
            self.enableUpdate = True
            return
        if not self.enableUpdate:
            return 
        self.channel = -(self.channelSelectionGroup.checkedId())-1
        if not serverConfig == {}:
            self.serverConfig = serverConfig
        
        if not self.serverConfig == {}:
            indexCoupling = [ i for i, s in enumerate(["DC","AC","GND"]) if s == self.serverConfig[':CHANnel CH'+str(self.channel)+':COUPling'] ]
            indexInvert = [ i for i, s in enumerate(["ON","OFF"]) if s == self.serverConfig[':CHANnel CH'+str(self.channel)+':INVert'] ]
            indexBW = [ i for i, s in enumerate(["FULL","2E+7"]) if s == self.serverConfig[':CHANnel CH'+str(self.channel)+':BWLimit'] ]
            indexExpand = [ i for i, s in enumerate(["CENTER","GROUND"]) if s == self.serverConfig[':CHANnel CH'+str(self.channel)+':EXPand'] ]
            indexProbeType = [ i for i, s in enumerate(["VOLTAGE","CURRENT"]) if s == self.serverConfig[':CHANnel CH'+str(self.channel)+':PROBe:TYPe'] ]

            self.comboboxChannelCoupling.blockSignals(True)
            self.comboboxChannelInvert.blockSignals(True)
            self.comboboxChannelBW.blockSignals(True)
            self.comboboxChannelExpand.blockSignals(True)
            self.comboboxProbeType.blockSignals(True)
            self.spinboxProbeAttenuation.blockSignals(True)
            
            self.comboboxChannelCoupling.setCurrentIndex(indexCoupling[0])
            self.comboboxChannelInvert.setCurrentIndex(indexInvert[0])
            self.comboboxChannelBW.setCurrentIndex(indexBW[0])
            self.comboboxChannelExpand.setCurrentIndex(indexExpand[0])
            self.comboboxProbeType.setCurrentIndex(indexProbeType[0])
            self.spinboxProbeAttenuation.setValue(float(self.serverConfig[':CHANnel CH'+str(self.channel)+':PROBe:RATio']))

            self.comboboxChannelCoupling.blockSignals(False)
            self.comboboxChannelInvert.blockSignals(False)
            self.comboboxChannelBW.blockSignals(False)
            self.comboboxChannelExpand.blockSignals(False)
            self.comboboxProbeType.blockSignals(False)
            self.spinboxProbeAttenuation.blockSignals(False)
            
    def channelCoupling(self,coupling):
        self.request.emit('CHANnelCOUPling',[str(self.channel),coupling])
        
    def channelInvert(self,invert):
        self.request.emit('CHANnelINVert',[str(self.channel),invert])
        
    def channelBW(self,bw):
        self.request.emit('CHANnelBWLimit',[str(self.channel),'20E+6' if bw == '20MHz' else bw])
        
    def channelExpand(self,expand):
        self.request.emit('CHANnelEXPand',[str(self.channel),expand])
        
    def channelType(self,type):
        self.request.emit('CHANnelPROBeTYPe',[str(self.channel),type])
        
    def channelAttenuation(self,attenuation):
        self.request.emit('CHANnelPROBeRATio',[str(self.channel),str(attenuation)])
        
    def channelDeskew(self,deskew):
        self.request.emit('CHANnelDESKew',[str(self.channel),str(deskew*1e-9)])

class widgetSectionTimebase(QWidget):
    request = pyqtSignal(str,object)
    holdUpdate = False
    enableUpdate = True

    def __init__(self):
        super(widgetSectionTimebase, self).__init__()
        self.setupTimer()
        self.load_ui()
        self.setFocusPolicy(Qt.NoFocus)
        self.connectActions()
        self.update()

    def setupTimer(self):
        self.timerTimebasePosition = QTimer()
        self.timerTimebasePosition.setSingleShot(True)
        self.timerTimebasePosition.setInterval(200)

    def load_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5, 5, 0, 5)

        timebaseGeneralLayout = QGridLayout()

        timebasemodeList = ['Main','Zoom','XY'] 
        self.comboboxTimebaseMode = QComboBox()
        self.comboboxTimebaseMode.addItems(timebasemodeList)

        timebaseexpandList = ['Center','TRIGger']
        self.comboboxTimebaseExpand = QComboBox()
        self.comboboxTimebaseExpand.addItems(timebaseexpandList)


        timebaseGeneralLayout.addWidget(QLabel('Mode'),1,1)
        timebaseGeneralLayout.addWidget(self.comboboxTimebaseMode,2,1)
        timebaseGeneralLayout.addWidget(QLabel('*Expand'),1,2)
        timebaseGeneralLayout.addWidget(self.comboboxTimebaseExpand,2,2)

        timebaseControlLayout = QGridLayout()
        self.spinBoxTimebaseScale = spinBoxWithPresetDelayedSignal(
            [5e-9,1e-8,2e-8,5e-8,1e-7,2e-7,5e-7,1e-6,2e-6,5e-6,
            1e-5,2e-5,5e-5,1e-4,2e-4,5e-4,1e-3,2e-3,5e-3,1e-2,2e-2,5e-2,
            1e-1,2e-1,5e-1,1e0,2e0,5e0,1e1,2e1,5e1,1e2],9,objectName='2')
        self.spinBoxTimebaseScale.lineEdit().setReadOnly(True)
        
        self.spinBoxTimebasePosition = spinBoxDelayedSignal()
        self.spinBoxTimebasePosition.setRange(-1,1)
        self.spinBoxTimebasePosition.setSingleStep(0.01)
        self.spinBoxTimebasePosition.setDecimals(9)
        self.spinBoxTimebasePosition.lineEdit().setReadOnly(True)

        self.spinBoxTimebaseZoomScale = spinBoxWithPresetDelayedSignal(
            [5e-9,1e-8,2e-8,5e-8,1e-7,2e-7,5e-7,1e-6,2e-6,5e-6,
            1e-5,2e-5,5e-5,1e-4,2e-4,5e-4,1e-3,2e-3,5e-3,1e-2,2e-2,5e-2,
            1e-1,2e-1,5e-1,1e0,2e0,5e0,1e1,2e1,5e1,1e2],9,objectName='3')
        self.spinBoxTimebaseZoomScale.lineEdit().setReadOnly(True)

        self.spinBoxTimebaseZoomPosition = spinBoxDelayedSignal()
        self.spinBoxTimebaseZoomPosition.setRange(-1,1)
        self.spinBoxTimebaseZoomPosition.setSingleStep(0.01)
        self.spinBoxTimebaseZoomPosition.setDecimals(9)
        self.spinBoxTimebaseZoomPosition.lineEdit().setReadOnly(True)

        timebaseControlLayout.addWidget(QLabel('Main'),1,1,Qt.AlignHCenter)
        timebaseControlLayout.addWidget(QLabel('Zoom'),1,3,Qt.AlignHCenter)

        timebaseControlLayout.addWidget(QLabel('Scale'),2,1)
        timebaseControlLayout.addWidget(self.spinBoxTimebaseScale,3,1)
        timebaseControlLayout.addWidget(QLabel('Position'),4,1)
        timebaseControlLayout.addWidget(self.spinBoxTimebasePosition,5,1)
        timebaseControlLayout.addWidget(QLabel('Scale'),2,3)
        timebaseControlLayout.addWidget(self.spinBoxTimebaseZoomScale,3,3)
        timebaseControlLayout.addWidget(QLabel('*Position'),4,3)
        timebaseControlLayout.addWidget(self.spinBoxTimebaseZoomPosition,5,3)
        timebaseControlLayout.setColumnStretch(1,50)
        timebaseControlLayout.setColumnStretch(3,50)

        separator = QWidget()
        separator.setStyleSheet('background-color: #CCCCCC;')
        timebaseControlLayout.addWidget(separator,1,2,-1,1)
        timebaseControlLayout.setColumnStretch(2,0)
        timebaseControlLayout.setColumnMinimumWidth(2,2)
        
        mainLayout.addLayout(timebaseGeneralLayout)
        mainLayout.addLayout(timebaseControlLayout)

        self.setLayout(mainLayout)

    def connectActions(self):
        self.comboboxTimebaseMode.currentTextChanged.connect(self.timebaseMode)
        self.comboboxTimebaseExpand.currentTextChanged.connect(self.timebaseExpand)
        self.spinBoxTimebaseScale.valueChanged.connect(self.disableUpdate)
        self.spinBoxTimebaseScale.valueChangedDelayed.connect(self.timebaseMainScale)
        self.spinBoxTimebasePosition.valueChanged.connect(self.disableUpdate)
        self.spinBoxTimebasePosition.valueChangedDelayed.connect(self.timebaseMainPosition)
        self.spinBoxTimebaseZoomScale.valueChanged.connect(self.disableUpdate)
        self.spinBoxTimebaseZoomScale.valueChangedDelayed.connect(self.timebaseZoomScale)
        self.spinBoxTimebaseZoomPosition.valueChanged.connect(self.disableUpdate)
        self.spinBoxTimebaseZoomPosition.valueChangedDelayed.connect(self.timebaseZoomPosition)

    def disableUpdate(self):
        self.holdUpdate = True
        self.enableUpdate = False

    def update(self,serverConfig={}):
        if self.holdUpdate:
            self.enableUpdate = True
            return
        if not self.enableUpdate:
            return 
        if not serverConfig == {}:
            indexMode = [ i for i, s in enumerate(["MAIN","WINDOW","XY MODE"]) if s == serverConfig[':TIMebase:MODe'] ]
            self.spinBoxTimebasePosition.setMinimum(-float(serverConfig[':TIMebase:SCALe'])*5)
            self.spinBoxTimebasePosition.setSingleStep(float(serverConfig[':TIMebase:SCALe'])/100)
            self.spinBoxTimebaseZoomPosition.setRange(-float(serverConfig[':TIMebase:SCALe'])*5+float(serverConfig[':TIMebase:POSition']),float(serverConfig[':TIMebase:SCALe'])*5+float(serverConfig[':TIMebase:POSition']))
            self.spinBoxTimebaseZoomPosition.setSingleStep(float(serverConfig[':TIMebase:WINDow:SCALe'])/100)
            
            self.comboboxTimebaseMode.blockSignals(True)
            self.spinBoxTimebaseScale.blockSignals(True)
            self.spinBoxTimebasePosition.blockSignals(True)
            self.spinBoxTimebaseZoomScale.blockSignals(True)

            self.comboboxTimebaseMode.setCurrentIndex(indexMode[0])
            self.spinBoxTimebaseScale.setValue(float(serverConfig[':TIMebase:SCALe']))
            self.spinBoxTimebasePosition.setValue(float(serverConfig[':TIMebase:POSition']))
            self.spinBoxTimebaseZoomScale.setValue(float(serverConfig[':TIMebase:WINDow:SCALe']))

            self.comboboxTimebaseMode.blockSignals(False)
            self.spinBoxTimebaseScale.blockSignals(False)
            self.spinBoxTimebasePosition.blockSignals(False)
            self.spinBoxTimebaseZoomScale.blockSignals(False)

    def timebaseMode(self,mode):
        self.request.emit('TIMebaseMODe',['Window' if mode == 'Zoom' else mode])

    def timebaseExpand(self,expand):
        self.request.emit('TIMebaseEXPand',[expand])

    def timebaseMainScale(self,scale):
        self.request.emit('TIMebaseSCALe',[str(scale)])

    def timebaseMainPosition(self,position):
        self.request.emit('TIMebasePOSition',[str(position)])
        self.holdUpdate = False

    def timebaseZoomScale(self,scale):
        self.request.emit('TIMebaseWINDowSCALe',[str(scale)])

    def timebaseZoomPosition(self,position):
        self.request.emit('TIMebaseWINDowPOSition',[str(position)])
        self.holdUpdate = False
