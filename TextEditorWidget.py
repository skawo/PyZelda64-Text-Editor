import zeldaMessage

from zeldaEnums import *
from PyQt6 import  QtGui, QtWidgets
from PyQt6.QtCore import Qt

class textEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()

        self.messageList = None

        mainLayout = QtWidgets.QGridLayout()

        # --------------- Message Grid

        messageGridLayout = QtWidgets.QVBoxLayout()

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
        self.messageEditor.textChanged.connect(self.messageTextChanged)
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
    
    def createModeWidgets(self):
        for i in reversed(range(self.messageOptionsLayout.count())): 
            self.messageOptionsLayout.itemAt(i).widget().setParent(None)

        boxPositionLabel = QtWidgets.QLabel("Box Position:", self) 
        self.boxPositionCombo = QtWidgets.QComboBox() 

        boxTypeLabel = QtWidgets.QLabel("Box Type:", self)         

        if self.messageMode == messageMode.Majora:

            for tpos in textboxPosition:
                self.boxPositionCombo.addItem(tpos.name)  

            iconLabel = QtWidgets.QLabel("Icon:", self)  
            jumpToLabel = QtWidgets.QLabel("Jump to:", self)  
            firstPriceLabel = QtWidgets.QLabel("1st Price:", self)  
            secondPriceLabel = QtWidgets.QLabel("2nd Price:", self)  

            self.boxTypeCombo = QtWidgets.QComboBox()

            for type in majoraTextboxType:
                self.boxTypeCombo.addItem(type.name)

            self.iconComboMajora = QtWidgets.QComboBox() 

            for icon in majoraIcon:
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

            for tpos in textboxPosition:
                self.boxPositionCombo.addItem(tpos.name)  

                if self.boxPositionCombo.count() == 4:
                    break

            self.boxTypeCombo = QtWidgets.QComboBox()

            for type in ocarinaTextboxType:
                self.boxTypeCombo.addItem(type.name)

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

        for i in range(self.messageTable.rowCount()):
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
        for index, item in enumerate(self.messageList): 
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

        if self.curMessage is not None:
            self.messageEditor.setPlainText(self.curMessage.textData)
            self.boxPositionCombo.setCurrentText(textboxPosition(self.curMessage.boxPosition).name)

            if self.messageMode == messageMode.Majora:
                self.boxTypeCombo.setCurrentText(majoraTextboxType(self.curMessage.boxType).name)
                self.iconComboMajora.setCurrentText(majoraIcon(self.curMessage.majoraIcon).name)
                self.jumpToField.setText(zeldaMessage.formatMessageID(self.curMessage.majoraJumpTo))
                self.firstPriceField.setText(str(self.curMessage.majoraFirstPrice))
                self.secondPriceField.setText(str(self.curMessage.majoraSecondPrice))
            else:
                self.boxTypeCombo.setCurrentText(ocarinaTextboxType(self.curMessage.boxType).name)

        self.messageEditor.blockSignals(False)
        self.boxPositionCombo.blockSignals(False)
        self.boxTypeCombo.blockSignals(False)

    def messageTextChanged(self):
        self.curMessage.textData = self.messageEditor.toPlainText()
        self.updateCurrentMsgRow()

    def boxTypeChanged(self):
        if self.messageMode == messageMode.Majora:
           self.curMessage.boxType = majoraTextboxType[self.boxTypeCombo.currentText()] 
        else:
            self.curMessage.boxType = ocarinaTextboxType[self.boxTypeCombo.currentText()]

    def boxPositionChanged(self):
        self.curMessage.boxPosition = textboxPosition[self.boxPositionCombo.currentText()]

    def addMessageClicked(self):
        if self.messageList is not None:
            input, done = QtWidgets.QInputDialog.getText(self, ' ', 'New Message ID (hex):')

            if done is False:
                return

            try:
                id = int(input, 16)
                msg = self.getMessageById(id)
                if msg is not None:
                    QtWidgets.QMessageBox.information(self, 'Error', 'Message ID already exists.')
                else:
                    self.addMsgRow(self.messageTable.rowCount() - 1, id, "")     
                    message = zeldaMessage.message(None, None, self.messageMode)
                    message.messageId = id
                    self.messageList.append(message)  
                    self.messageTable.selectRow(self.messageTable.rowCount() - 1)    

            except:
                QtWidgets.QMessageBox.information(self, 'Error', 'Invalid message ID.')

    def changeIDClicked(self):
        if self.messageList is not None:
            input, done = QtWidgets.QInputDialog.getText(self, ' ', 'New Message ID (hex):')

            if done is False:
                return
            
            try:
                id = int(input, 16)
                msg = self.getMessageById(id)
                if msg is not None:
                    QtWidgets.QMessageBox.information(self, 'Error', 'Message ID already exists.')  
                else:
                    self.curMessage.messageId = id 
                    self.updateCurrentMsgRow()             
            except:
                QtWidgets.QMessageBox.information(self, 'Error', 'Invalid message ID.')        

    def removeClicked(self):
        if self.messageList is not None:
            index = self.messageTable.selectedIndexes()[0].row()
            self.messageList.remove(self.curMessage)
            self.messageTable.removeRow(index)

    def searchFieldChanged(self):

        for index, item in enumerate(self.messageList): 
            self.messageTable.hideRow(index)

        text = self.searchField.text()

        matching = self.messageTable.findItems(self.searchField.text(), Qt.MatchFlag.MatchContains)

        for item in matching:
            index = self.messageTable.indexFromItem(item)
            self.messageTable.showRow(index.row())
