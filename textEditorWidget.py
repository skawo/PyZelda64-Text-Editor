import zeldaMessage

from zeldaEnums import *
from messageTextEditor import CustomPlainTextEdit
from hSpinBox import InputBox
from qLabelPreviewer import QLabelPreviewer

from PyQt6 import  QtGui, QtWidgets
from PyQt6.QtCore import Qt

class TextEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()

        self.messageList = None

        mainLayout = QtWidgets.QHBoxLayout()

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
        self.messageEditor.setMaximumWidth(700)
        self.messageEditor.textChanged.connect(self.messageTextChanged)
        self.messageEditLayout.addWidget(self.messageEditor)

        # --------------- Message Preview

        messagePreviewLayout = QtWidgets.QVBoxLayout()
        self.messagePreview = QLabelPreviewer()
        messagePreviewLayout.addWidget(self.messagePreview)

        # ------------------------------

        mainLayout.addLayout(messageTableLayout,True)
        mainLayout.addLayout(self.messageEditLayout)
        mainLayout.addLayout(messagePreviewLayout,True)

        self.setLayout(mainLayout)
        self.changesMade = False

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

            self.jumpToField = QtWidgets.QLineEdit()
            self.firstPriceField = QtWidgets.QLineEdit()
            self.secondPriceField = QtWidgets.QLineEdit()

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
    
        self.curMessage = self.getCurrentMessage()
        self.messagePreview.clear

        if self.curMessage is not None:
            self.messageEditor.setPlainText(self.curMessage.textData)
            self.boxPositionCombo.setCurrentText(TextboxPosition(self.curMessage.boxPosition).name)

            if self.messageMode == MessageMode.Majora:
                self.boxTypeCombo.setCurrentText(MajoraTextboxType(self.curMessage.boxType).name)
                self.iconComboMajora.setCurrentText(MajoraIcon(self.curMessage.majoraIcon).name)
                self.jumpToField.setText(zeldaMessage.formatMessageID(self.curMessage.majoraJumpTo))
                self.firstPriceField.setText(str(self.curMessage.majoraFirstPrice))
                self.secondPriceField.setText(str(self.curMessage.majoraSecondPrice))
            else:
                self.boxTypeCombo.setCurrentText(OcarinaTextboxType(self.curMessage.boxType).name)

        self.updateMsgPreview()
        self.messageEditor.blockSignals(False)
        self.boxPositionCombo.blockSignals(False)
        self.boxTypeCombo.blockSignals(False)

    def messageTextChanged(self):
        self.curMessage.textData = self.messageEditor.toPlainText()
        self.updateMsgPreview()
        self.updateCurrentMsgRow()

    def updateMsgPreview(self):
        img = self.curMessage.getFullPreview()

        if img is not None:
            pxm = QtGui.QPixmap.fromImage(img)
            self.messagePreview.setPixmap(pxm.scaledToWidth(self.messagePreview.width(), Qt.TransformationMode.SmoothTransformation))
            self.messagePreview.setGraphicsEffect(None)
        else:
            effect = QtWidgets.QGraphicsOpacityEffect()
            effect.setOpacity(0.7)
            self.messagePreview.setGraphicsEffect(effect)


    def boxTypeChanged(self):
        if self.messageMode == MessageMode.Majora:
           self.curMessage.boxType = MajoraTextboxType[self.boxTypeCombo.currentText()] 
        else:
            self.curMessage.boxType = OcarinaTextboxType[self.boxTypeCombo.currentText()]

        self.updateMsgPreview()

    def boxPositionChanged(self):
        self.curMessage.boxPosition = TextboxPosition[self.boxPositionCombo.currentText()]

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
            except ValueError:
                QtWidgets.QMessageBox.information(self, 'Error', 'Invalid message ID.')        

    def removeClicked(self):
        if self.messageList is not None:
            index = self.messageTable.selectedIndexes()[0].row()
            self.messageList.remove(self.curMessage)
            self.messageTable.removeRow(index)

    def searchFieldChanged(self):

        for index, _ in enumerate(self.messageList): 
            self.messageTable.hideRow(index)

        matching = self.messageTable.findItems(self.searchField.text(), Qt.MatchFlag.MatchContains)

        for item in matching:
            index = self.messageTable.indexFromItem(item)
            self.messageTable.showRow(index.row())
