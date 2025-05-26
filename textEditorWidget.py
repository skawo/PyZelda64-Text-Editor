import zeldaMessage
import zeldaMessagePreview

from zeldaEnums import *
from messageTextEditor import CustomPlainTextEdit
from hSpinBox import *
from qLabelPreviewer import QLabelPreviewer

from PyQt6 import  QtGui, QtWidgets
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

class TextEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()

        self.messageList = None
        self.boxDataLast = None
        self.changesMade = False

        splitter = QtWidgets.QSplitter()
        splitter.setHandleWidth(3)

        # --------------- Message Grid

        messageTableLayout = QtWidgets.QVBoxLayout()

        self.searchField = QtWidgets.QLineEdit()
        self.searchField.setPlaceholderText("Type to search...")
        self.searchField.textChanged.connect(self.searchFieldChanged)

        self.messageTable = QtWidgets.QTableWidget()
        self.messageTable.setColumnCount(2)
        self.messageTable.setHorizontalHeaderLabels(["ID", "Message"])
        self.messageTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.messageTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.messageTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.messageTable.itemSelectionChanged.connect(self.messageTableItemChanged)
        
        headerView = self.messageTable.horizontalHeader()
        headerView.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        headerView.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.messageTable.verticalHeader().setVisible(False)
        self.messageTable.setHorizontalHeader(headerView)

        buttonsGrid = QtWidgets.QHBoxLayout() 

        buttonAdd = QtWidgets.QPushButton("Add", self)
        buttonAdd.clicked.connect(self.addMessageClicked)

        changeID = QtWidgets.QPushButton("Change ID", self)
        changeID.clicked.connect(self.changeIDClicked)

        buttonRemove = QtWidgets.QPushButton("Remove", self)
        buttonRemove.clicked.connect(self.removeClicked)

        buttonsGrid.addWidget(buttonAdd)
        buttonsGrid.addWidget(changeID)
        buttonsGrid.addWidget(buttonRemove)

        messageTableLayout.addWidget(self.searchField)
        messageTableLayout.addWidget(self.messageTable)
        messageTableLayout.addLayout(buttonsGrid)

        # --------------- Message Edit

        self.messageEditLayout = QtWidgets.QVBoxLayout()

        self.messageOptionsFrame = QtWidgets.QGroupBox("Message Options")
        self.messageOptionsFrame.setMaximumWidth(700)

        self.messageOptionsFrame.setStyleSheet(f"""
        QGroupBox {{
            border: 1px solid {self.messageOptionsFrame.palette().color(QtGui.QPalette.ColorRole.Mid).name()};
            margin-top: 1ex;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            margin: 0ex 0.5ex;
            background-color: {self.messageOptionsFrame.palette().color(QtGui.QPalette.ColorRole.Window).name()};
        }}
        """)

        self.messageOptionsLayout = QtWidgets.QGridLayout()
        self.messageOptionsFrame.setLayout(self.messageOptionsLayout)
        self.messageEditLayout.addWidget(self.messageOptionsFrame)

        self.messageEditor = CustomPlainTextEdit()
        self.messageEditor.textChanged.connect(self.messageTextChanged)
        self.messageEditLayout.addWidget(self.messageEditor)

        # --------------- Message Preview

        messagePreviewLayout = QtWidgets.QVBoxLayout()

        messagePreviewScrollArea = QtWidgets.QScrollArea()
        messagePreviewScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        messagePreviewScrollArea.setSizeAdjustPolicy(QtWidgets.QScrollArea.SizeAdjustPolicy.AdjustIgnored)
        
        self.messagePreview = QLabelPreviewer()
        self.messagePreview.setMinimumWidth(256)
        messagePreviewScrollArea.setWidgetResizable(True)
        messagePreviewScrollArea.setWidget(self.messagePreview)
        messagePreviewLayout.addWidget(messagePreviewScrollArea)
        messagePreviewLayout.maximumSize()

        # ------------------------------

        messageTableLayout.setContentsMargins(0, 0, 0, 0)
        self.messageEditLayout.setContentsMargins(0, 0, 0, 0)
        messagePreviewLayout.setContentsMargins(0, 0, 0, 0)

        widgetsA = QtWidgets.QWidget(self)
        widgetsB = QtWidgets.QWidget(self)
        widgetsC = QtWidgets.QWidget(self)

        widgetsA.setLayout(messageTableLayout)
        widgetsB.setLayout(self.messageEditLayout)
        widgetsC.setLayout(messagePreviewLayout)

        splitter.addWidget(widgetsA)
        splitter.addWidget(widgetsB)
        splitter.addWidget(widgetsC)

        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(splitter)

        self.setLayout(topLayout)
        return
    
    def createModeWidgets(self):
        for i in reversed(range(self.messageOptionsLayout.count())): 
            self.messageOptionsLayout.itemAt(i).widget().setParent(None)

        boxPositionLabel = QtWidgets.QLabel("Box Position:", self) 
        self.boxPositionCombo = QtWidgets.QComboBox() 

        boxTypeLabel = QtWidgets.QLabel("Box Type:", self)         

        if self.messageMode == MessageMode.Majora:
            
            self.boxPositionCombo.addItems([type.name for type in TextboxPosition])

            iconLabel = QtWidgets.QLabel("Icon:", self)  
            jumpToLabel = QtWidgets.QLabel("Jump to:", self)  
            firstPriceLabel = QtWidgets.QLabel("1st Price:", self)  
            secondPriceLabel = QtWidgets.QLabel("2nd Price:", self)  

            self.boxTypeCombo = QtWidgets.QComboBox()
            self.boxTypeCombo.addItems([type.name for type in MajoraTextboxType])

            self.iconComboMajora = QtWidgets.QComboBox() 
            self.iconComboMajora.addItems([type.name for type in MajoraIcon])

            self.jumpToField = HexSpinBox()
            self.jumpToField.setRange(0, 0xFFFF)
            self.firstPriceField = QtWidgets.QSpinBox()
            self.firstPriceField.setRange(-1, 999)
            self.secondPriceField = QtWidgets.QSpinBox()
            self.secondPriceField.setRange(-1, 999)

            self.messageOptionsLayout.addWidget(boxTypeLabel, 0, 0)
            self.messageOptionsLayout.addWidget(self.boxTypeCombo, 0, 1)
            self.messageOptionsLayout.addWidget(boxPositionLabel, 1, 0)
            self.messageOptionsLayout.addWidget(self.boxPositionCombo, 1, 1)
            self.messageOptionsLayout.addWidget(iconLabel, 2, 0)
            self.messageOptionsLayout.addWidget(self.iconComboMajora, 2, 1)
            self.messageOptionsLayout.addWidget(jumpToLabel, 3, 0)
            self.messageOptionsLayout.addWidget(self.jumpToField, 3, 1)
            self.messageOptionsLayout.addWidget(firstPriceLabel, 4, 0)
            self.messageOptionsLayout.addWidget(self.firstPriceField, 4, 1)
            self.messageOptionsLayout.addWidget(secondPriceLabel, 5, 0)
            self.messageOptionsLayout.addWidget(self.secondPriceField, 5, 1) 

            self.iconComboMajora.currentTextChanged.connect(self.majoraIconChanged)
            self.jumpToField.textChanged.connect(self.jumpToFieldChanged)
            self.firstPriceField.textChanged.connect(self.firstPriceFieldChanged)
            self.secondPriceField.textChanged.connect(self.secondPriceFieldChanged)
        else:

            for tpos in list(TextboxPosition)[:5]:
                self.boxPositionCombo.addItem(tpos.name)

            self.boxTypeCombo = QtWidgets.QComboBox()
            self.boxTypeCombo.addItems([type.name for type in OcarinaTextboxType])

            self.messageOptionsLayout.addWidget(boxTypeLabel, 0, 0)
            self.messageOptionsLayout.addWidget(self.boxTypeCombo, 0, 1)
            self.messageOptionsLayout.addWidget(boxPositionLabel, 1, 0)
            self.messageOptionsLayout.addWidget(self.boxPositionCombo, 1, 1)

        self.boxTypeCombo.currentTextChanged.connect(self.boxTypeChanged)
        self.boxPositionCombo.currentTextChanged.connect(self.boxPositionChanged)

    def populateEditor(self, messageList, mode):
        self.messageTable.blockSignals(True)
        
        self.messageList = messageList
        self.messageMode = mode

        self.createModeWidgets()
        self.messageEditor.setMode(self.messageMode)

        for _ in range(self.messageTable.rowCount()):
            self.messageTable.removeRow(0)

        for message in messageList:
            self.addMsgRow(self.messageTable.rowCount(), message.messageId, message.textData)

        self.messageTable.blockSignals(False)
        self.messageTable.selectRow(0)

    def addMsgRow(self, index, messageId, messageText):
        self.messageTable.insertRow(index) 
        self.updateMsgRow(index, messageId, messageText)    

    def updateMsgRow(self, index, messageId, messageText):
        id = QtWidgets.QTableWidgetItem(zeldaMessage.formatMessageID(messageId))
        text = QtWidgets.QTableWidgetItem(messageText)

        self.messageTable.setItem(index, 0, id)
        self.messageTable.setItem(index, 1, text)

    def updateCurrentMsgRow(self):
        self.updateMsgRow(self.messageTable.selectedIndexes()[0].row(), self.curMessage.messageId, self.curMessage.textData)

    def getMessageById(self, id):
        for item in self.messageList: 
            if item.messageId == id:
                return item
            
        return None
    
    def getCurrentMessage(self):
        msgId = int(self.messageTable.selectedItems()[0].text(), 16) & 0xFFFF
        return self.getMessageById(msgId)

    def messageTableItemChanged(self):
        self.messageEditor.blockSignals(True)
        self.boxPositionCombo.blockSignals(True)
        self.boxTypeCombo.blockSignals(True)

        if self.messageMode == MessageMode.Majora:
            self.iconComboMajora.blockSignals(True)
            self.jumpToField.blockSignals(True)
            self.firstPriceField.blockSignals(True)
            self.secondPriceField.blockSignals(True)
    
        self.curMessage = self.getCurrentMessage()
        self.messagePreview.clear

        if self.curMessage is not None:
            self.messageEditor.setPlainText(self.curMessage.textData)
            self.boxPositionCombo.setCurrentText(TextboxPosition(self.curMessage.boxPosition).name)

            if self.messageMode == MessageMode.Majora:
                self.boxTypeCombo.setCurrentText(MajoraTextboxType(self.curMessage.boxType).name)
                self.iconComboMajora.setCurrentText(MajoraIcon(self.curMessage.majoraIcon).name)
                self.jumpToField.setValue(self.curMessage.majoraJumpTo)
                self.firstPriceField.setValue(self.curMessage.majoraFirstPrice)
                self.secondPriceField.setValue(self.curMessage.majoraSecondPrice)
            else:
                self.boxTypeCombo.setCurrentText(OcarinaTextboxType(self.curMessage.boxType).name)

        self.updateMsgPreview(True)
        self.messageEditor.blockSignals(False)
        self.boxPositionCombo.blockSignals(False)
        self.boxTypeCombo.blockSignals(False)

        if self.messageMode == MessageMode.Majora:
            self.iconComboMajora.blockSignals(False)
            self.jumpToField.blockSignals(False)
            self.firstPriceField.blockSignals(False)
            self.secondPriceField.blockSignals(False)

    def updateMsgPreview(self, force = False):

        boxData = self.curMessage.preparePreviewData()
        img = None

        if boxData is not None:

            if self.messageMode == MessageMode.Majora:
                previewer = zeldaMessagePreview.MessagePreviewMajora(self.curMessage.boxType, False, boxData) 
            else:
                previewer = zeldaMessagePreview.MessagePreviewOcarina(self.curMessage.boxType, boxData)

            _, OUTPUT_IMAGE_Y = previewer.getImageSizes()

            if self.boxDataLast is not None and len(boxData) == len(self.boxDataLast) and not force:
                img = self.messagePreview.pixmapOg.copy()
                painter = QPainter(img)

                for i, box in enumerate(boxData):
                    if box != self.boxDataLast[i]:
                        newPreview = previewer.getPreview(i)

                        if newPreview is not None:
                            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
                            painter.drawImage(0, OUTPUT_IMAGE_Y * i + zeldaMessagePreview.SPACER_HEIGHT * i, newPreview)
                        else:
                            img = None
                            break

                painter.end()
            else:
                img = QtGui.QPixmap.fromImage(self.curMessage.getFullPreview(boxData))

        self.boxDataLast = boxData

        if img is not None:
            self.messagePreview.setPixmap(img)
            self.messagePreview.setGraphicsEffect(None)
        else:
            effect = QtWidgets.QGraphicsOpacityEffect()
            effect.setOpacity(0.7)
            self.messagePreview.setGraphicsEffect(effect)

    def _changesMade(self):
        self.changesMade = True

    def messageTextChanged(self):
        self.curMessage.textData = self.messageEditor.toPlainText()
        self.updateMsgPreview()
        self.updateCurrentMsgRow()
        self._changesMade()        

    def boxTypeChanged(self):
        if self.messageMode == MessageMode.Majora:
           self.curMessage.boxType = MajoraTextboxType[self.boxTypeCombo.currentText()] 
        else:
            self.curMessage.boxType = OcarinaTextboxType[self.boxTypeCombo.currentText()]

        self.updateMsgPreview(True)
        self._changesMade()

    def majoraIconChanged(self):
        self.curMessage.majoraIcon = MajoraIcon[self.iconComboMajora.currentText()]
        self.updateMsgPreview(True)
        self._changesMade()

    def boxPositionChanged(self):
        self.curMessage.boxPosition = TextboxPosition[self.boxPositionCombo.currentText()]
        self._changesMade()

    def jumpToFieldChanged(self):
        self.curMessage.majoraJumpTo = self.jumpToField.value()
        self._changesMade()

    def firstPriceFieldChanged(self):
        self.curMessage.majoraFirstPrice = self.firstPriceField.value()
        self._changesMade()

    def secondPriceFieldChanged(self):
        self.curMessage.majoraFirstPrice = self.secondPriceField.value()
        self._changesMade()

    def addMessageClicked(self):
        if self.messageList is not None:
            dbox = InputBox(self.parent, InputBox.Type_HexSpinBox)
            result = dbox.show(' ', 'New Message ID?', 0, 0, 0xFFFF)

            if result != QtWidgets.QDialog.DialogCode.Accepted:
                return

            try:
                id = dbox.spinbox.value()
                msg = self.getMessageById(id)
                if msg is not None:
                    QtWidgets.QMessageBox.information(self, 'Error', 'Message ID already exists.')
                else:
                    self.addMsgRow(self.messageTable.rowCount() - 1, id, "")     

                    if self.messageMode == MessageMode.Majora:
                        message = zeldaMessage.MessageMajora(None, None, self.messageMode) 
                    else:
                        message = zeldaMessage.MessageOcarina(None, None, self.messageMode)

                    message.messageId = id
                    self.messageList.append(message)  
                    self.messageTable.selectRow(self.messageTable.rowCount() - 1)    
                    self._changesMade()

            except ValueError:
                QtWidgets.QMessageBox.information(self, 'Error', 'Invalid message ID.')

    def changeIDClicked(self):
        if self.messageList is not None and self.curMessage is not None:
            dbox = InputBox(self, InputBox.Type_HexSpinBox)
            result = dbox.show(' ', 'New Message ID?', self.curMessage.messageId, 0, 0xFFFF)

            if result != QtWidgets.QDialog.DialogCode.Accepted:
                return
            
            try:
                id = dbox.spinbox.value()
                msg = self.getMessageById(id)
                if msg is not None:
                    QtWidgets.QMessageBox.information(self, 'Error', 'Message ID already exists.')  
                else:
                    self.curMessage.messageId = id 
                    self.updateCurrentMsgRow()             
                    self._changesMade()
            except ValueError:
                QtWidgets.QMessageBox.information(self, 'Error', 'Invalid message ID.')        

    def removeClicked(self):
        if self.messageList is not None:
            index = self.messageTable.selectedIndexes()[0].row()
            self.messageList.remove(self.curMessage)
            self.messageTable.removeRow(index)
            self._changesMade()

    def searchFieldChanged(self):
        for index, _ in enumerate(self.messageList): 
            self.messageTable.hideRow(index)

        matching = self.messageTable.findItems(self.searchField.text(), Qt.MatchFlag.MatchContains)

        for item in matching:
            index = self.messageTable.indexFromItem(item)
            self.messageTable.showRow(index.row())
