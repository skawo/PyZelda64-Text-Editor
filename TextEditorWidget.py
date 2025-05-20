import ZeldaMessage

from ZeldaEnums import *
from PyQt6 import  QtGui, QtWidgets

class TextEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(TextEditorWidget, self).__init__(parent)

        self.messageList = None

        mainLayout = QtWidgets.QGridLayout()

        # --------------- Message Grid

        messageGridLayout = QtWidgets.QVBoxLayout()

        self.searchField = QtWidgets.QLineEdit()
        self.searchField.setPlaceholderText("Type to search...")

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
        buttonAdd.clicked.connect(self.AddMessageClicked)

        changeID = QtWidgets.QPushButton("Change ID", self)
        changeID.clicked.connect(self.ChangeIDClicked)

        buttonRemove = QtWidgets.QPushButton("Remove", self)
        buttonRemove.clicked.connect(self.RemoveClicked)

        buttonsGrid.addWidget(buttonAdd)
        buttonsGrid.addWidget(changeID)
        buttonsGrid.addWidget(buttonRemove)

        messageGridLayout.addWidget(self.searchField)
        messageGridLayout.addWidget(self.messageTable)
        messageGridLayout.addLayout(buttonsGrid)

        # --------------- Message Edit

        self.messageEditLayout = QtWidgets.QVBoxLayout()

        self.messageOptionsFrame = QtWidgets.QGroupBox("Message Options")

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

        self.messageEditor = QtWidgets.QPlainTextEdit()
        self.messageEditor.textChanged.connect(self.MessageTextChanged)
        self.messageEditLayout.addWidget(self.messageEditor)

        # --------------- Message Preview

        messagePreviewLayout = QtWidgets.QVBoxLayout()
        messagePreview = QtWidgets.QLabel()
        messagePreview.setFixedWidth(320)
        messagePreviewLayout.addWidget(messagePreview)

        # ------------------------------

        mainLayout.addLayout(messageGridLayout, 0, 0)
        mainLayout.addLayout(self.messageEditLayout, 0, 1)
        mainLayout.addLayout(messagePreviewLayout, 0, 2)

        self.setLayout(mainLayout)
        self.changesMade = False

        return
    
    def CreateModeWidgets(self):
        for i in reversed(range(self.messageOptionsLayout.count())): 
            self.messageOptionsLayout.itemAt(i).widget().setParent(None)

        boxPositionLabel = QtWidgets.QLabel("Box Position:", self) 
        self.boxPositionCombo = QtWidgets.QComboBox() 

        boxTypeLabel = QtWidgets.QLabel("Box Type:", self)         

        if self.messageMode == MessageMode.Majora:

            for tpos in TextboxPosition:
                self.boxPositionCombo.addItem(tpos.name)  

            iconLabel = QtWidgets.QLabel("Icon:", self)  
            jumpToLabel = QtWidgets.QLabel("Jump to:", self)  
            firstPriceLabel = QtWidgets.QLabel("1st Price:", self)  
            secondPriceLabel = QtWidgets.QLabel("2nd Price:", self)  

            self.boxTypeCombo = QtWidgets.QComboBox()

            for type in MajoraTextboxType:
                self.boxTypeCombo.addItem(type.name)

            self.iconComboMajora = QtWidgets.QComboBox() 

            for icon in MajoraIcon:
                self.iconComboMajora.addItem(icon.name)

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

            for tpos in TextboxPosition:
                self.boxPositionCombo.addItem(tpos.name)  

                if self.boxPositionCombo.count() == 4:
                    break

            self.boxTypeCombo = QtWidgets.QComboBox()

            for type in OcarinaTextboxType:
                self.boxTypeCombo.addItem(type.name)

            self.messageOptionsLayout.addWidget(boxTypeLabel, 0, 0)
            self.messageOptionsLayout.addWidget(self.boxTypeCombo, 0, 1)
            self.messageOptionsLayout.addWidget(boxPositionLabel, 1, 0)
            self.messageOptionsLayout.addWidget(self.boxPositionCombo, 1, 1)

        self.boxTypeCombo.currentTextChanged.connect(self.BoxTypeChanged)
        self.boxPositionCombo.currentTextChanged.connect(self.BoxPositionChanged)


    def PopulateEditor(self, messageList, mode):
        self.messageTable.blockSignals(True)
        
        self.messageList = messageList
        self.messageMode = mode

        self.CreateModeWidgets()

        for i in range(self.messageTable.rowCount()):
            self.messageTable.removeRow(0)

        for message in messageList:
            self.AddMsgRow(self.messageTable.rowCount(), message.messageId, message.textData)

        self.messageTable.blockSignals(False)
        self.messageTable.selectRow(0)

    def AddMsgRow(self, index, messageId, messageText):
        self.messageTable.insertRow(index) 
        self.UpdateMsgRow(index, messageId, messageText)    

    def UpdateMsgRow(self, index, messageId, messageText):
        id = QtWidgets.QTableWidgetItem(ZeldaMessage.FormatMessageID(messageId))
        text = QtWidgets.QTableWidgetItem(messageText)

        self.messageTable.setItem(index, 0, id)
        self.messageTable.setItem(index, 1, text)

    def UpdateCurrentMsgRow(self):
        self.UpdateMsgRow(self.messageTable.selectedIndexes()[0].row(), self.curMessage.messageId, self.curMessage.textData)

    def GetMessageById(self, id):
        for index, item in enumerate(self.messageList): 
            if item.messageId == id:
                return item
            
        return None
    
    def GetCurrentMessage(self):
        msgId = int(self.messageTable.selectedItems()[0].text(), 16) & 0xFFFF
        return self.GetMessageById(msgId)

    def messageTableItemChanged(self):
        self.messageEditor.blockSignals(True)
        self.boxPositionCombo.blockSignals(True)
        self.boxTypeCombo.blockSignals(True)
    
        self.curMessage = self.GetCurrentMessage()

        if self.curMessage is not None:
            self.messageEditor.setPlainText(self.curMessage.textData)
            self.boxPositionCombo.setCurrentText(TextboxPosition(self.curMessage.boxPosition).name)

            if self.messageMode == MessageMode.Majora:
                self.boxTypeCombo.setCurrentText(MajoraTextboxType(self.curMessage.boxType).name)
                self.iconComboMajora.setCurrentText(MajoraIcon(self.curMessage.majoraIcon).name)
                self.jumpToField.setText(ZeldaMessage.FormatMessageID(self.curMessage.majoraJumpTo))
                self.firstPriceField.setText(str(self.curMessage.majoraFirstPrice))
                self.secondPriceField.setText(str(self.curMessage.majoraSecondPrice))
            else:
                self.boxTypeCombo.setCurrentText(OcarinaTextboxType(self.curMessage.boxType).name)

        self.messageEditor.blockSignals(False)
        self.boxPositionCombo.blockSignals(False)
        self.boxTypeCombo.blockSignals(False)

    def MessageTextChanged(self):
        self.curMessage.textData = self.messageEditor.toPlainText()
        self.UpdateCurrentMsgRow()

    def BoxTypeChanged(self):
        if self.messageMode == MessageMode.Majora:
           self.curMessage.boxType = MajoraTextboxType[self.boxTypeCombo.currentText()] 
        else:
            self.curMessage.boxType = OcarinaTextboxType[self.boxTypeCombo.currentText()]

    def BoxPositionChanged(self):
        self.curMessage.boxPosition = TextboxPosition[self.boxPositionCombo.currentText()]

    def AddMessageClicked(self):
        if self.messageList is not None:
            input, done = QtWidgets.QInputDialog.getText(self, ' ', 'New Message ID (hex):')

            if done is False:
                return

            try:
                id = int(input, 16)
                msg = self.GetMessageById(id)
                if msg is not None:
                    QtWidgets.QMessageBox.information(self, 'Error', 'Message ID already exists.')
                else:
                    self.AddMsgRow(self.messageTable.rowCount() - 1, id, "")     
                    message = ZeldaMessage.Message(None, None, self.messageMode)
                    message.messageId = id
                    self.messageList.append(message)  
                    self.messageTable.selectRow(self.messageTable.rowCount() - 1)    

            except:
                QtWidgets.QMessageBox.information(self, 'Error', 'Invalid message ID.')


    def ChangeIDClicked(self):
        if self.messageList is not None:
            input, done = QtWidgets.QInputDialog.getText(self, ' ', 'New Message ID (hex):')

            if done is False:
                return
            
            try:
                id = int(input, 16)
                msg = self.GetMessageById(id)
                if msg is not None:
                    QtWidgets.QMessageBox.information(self, 'Error', 'Message ID already exists.')  
                else:
                    self.curMessage.messageId = id 
                    self.UpdateCurrentMsgRow()             
            except:
                QtWidgets.QMessageBox.information(self, 'Error', 'Invalid message ID.')        

    def RemoveClicked(self):
        if self.messageList is not None:
            index = self.messageTable.selectedIndexes()[0].row()
            self.messageList.remove(self.curMessage)
            self.messageTable.removeRow(index)

    def SaveCurTextboxDebug(self):

        with open('out', 'wb') as f:
            for i in range(len(self.messageList)):
                data = self.messageList[i].ConvertToBytes()
                f.write(bytes(data))