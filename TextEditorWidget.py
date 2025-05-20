from ZeldaEnums import *
from PyQt6 import  QtGui, QtWidgets

class TextEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(TextEditorWidget, self).__init__(parent)

        mainLayout = QtWidgets.QGridLayout()

        # --------------- Message Grid

        messageGridLayout = QtWidgets.QVBoxLayout()

        searchField = QtWidgets.QLineEdit()
        searchField.setPlaceholderText("Type to search...")

        self.messageTable = QtWidgets.QTableWidget()
        self.messageTable.setColumnCount(2)
        self.messageTable.setHorizontalHeaderLabels(["ID", "Message"])
        self.messageTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.messageTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        
        headerView = self.messageTable.horizontalHeader()
        headerView.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        headerView.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.messageTable.verticalHeader().setVisible(False)
        self.messageTable.setHorizontalHeader(headerView)

        buttonsGrid = QtWidgets.QHBoxLayout() 

        buttonAdd = QtWidgets.QPushButton("Add", self)
        changeID = QtWidgets.QPushButton("Change ID", self)
        buttonRemove = QtWidgets.QPushButton("Remove", self)

        buttonsGrid.addWidget(buttonAdd)
        buttonsGrid.addWidget(changeID)
        buttonsGrid.addWidget(buttonRemove)

        messageGridLayout.addWidget(searchField)
        messageGridLayout.addWidget(self.messageTable)
        messageGridLayout.addLayout(buttonsGrid)

        # --------------- Message Edit

        messageEditLayout = QtWidgets.QVBoxLayout()

        messageOptionsFrame = QtWidgets.QGroupBox("Message Options")

        messageOptionsFrame.setStyleSheet(f"""
        QGroupBox {{
            border: 1px solid {messageOptionsFrame.palette().color(QtGui.QPalette.ColorRole.Mid).name()};
            margin-top: 1ex;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            margin: 0ex 0.5ex;
            background-color: {messageOptionsFrame.palette().color(QtGui.QPalette.ColorRole.Window).name()};
        }}
        """)

        messageOptionsLayout = QtWidgets.QGridLayout()
        
        boxTypeLabel = QtWidgets.QLabel("Box Type:", self)
        boxPositionLabel = QtWidgets.QLabel("Box Position:", self)

        self.boxTypeCombo = QtWidgets.QComboBox()

        for type in OcarinaTextboxType:
            self.boxTypeCombo.addItem(type.name)

        self.boxPositionCombo = QtWidgets.QComboBox()

        for tpos in TextboxPosition:
            self.boxPositionCombo.addItem(tpos.name)

        messageOptionsLayout.addWidget(boxTypeLabel, 0, 0)
        messageOptionsLayout.addWidget(self.boxTypeCombo, 0, 1)
        messageOptionsLayout.addWidget(boxPositionLabel, 1, 0)
        messageOptionsLayout.addWidget(self.boxPositionCombo, 1, 1)

        messageOptionsFrame.setLayout(messageOptionsLayout)
        messageEditLayout.addWidget(messageOptionsFrame)

        self.messageEditor = QtWidgets.QPlainTextEdit()
        messageEditLayout.addWidget(self.messageEditor)

        # --------------- Message Preview

        messagePreviewLayout = QtWidgets.QVBoxLayout()
        messagePreview = QtWidgets.QLabel()
        messagePreview.setFixedWidth(320)
        messagePreviewLayout.addWidget(messagePreview)

        # ------------------------------

        mainLayout.addLayout(messageGridLayout, 0, 0)
        mainLayout.addLayout(messageEditLayout, 0, 1)
        mainLayout.addLayout(messagePreviewLayout, 0, 2)

        self.setLayout(mainLayout)
        self.changesMade = False

        return
    
    def PopulateEditor(self, messageList):

        self.messageTable.itemSelectionChanged.disconnect
        self.messageList = messageList

        for message in messageList:
            self.messageTable.insertRow(self.messageTable.rowCount()) 
            self.UpdateRow(self.messageTable.rowCount()-1, message.messageId, message.textData)

        self.messageTable.itemSelectionChanged.connect(self.messageTableItemChanged)
        self.messageTable.selectRow(0)

    def UpdateRow(self, index, messageId, messageText):
        id = QtWidgets.QTableWidgetItem('0x' + format(messageId & 0xffff, '04X'))
        text = QtWidgets.QTableWidgetItem(messageText)

        self.messageTable.setItem(index, 0, id)
        self.messageTable.setItem(index, 1, text)

    def UpdateCurrentRow(self):
        self.UpdateRow(self.messageTable.selectedIndexes()[0].row(), self.curMessage.messageId, self.curMessage.textData)

    def GetCurrentMessage(self):
        msgId = int(self.messageTable.selectedItems()[0].text(), 16) & 0xFFFF

        for index, item in enumerate(self.messageList): 
            if item.messageId == msgId:
                return item
            
        return None

    def messageTableItemChanged(self):

        self.messageEditor.textChanged.disconnect
        self.boxPositionCombo.currentTextChanged.disconnect
        self.boxTypeCombo.currentTextChanged.disconnect

        self.curMessage = self.GetCurrentMessage()
        self.messageEditor.setPlainText(self.curMessage.textData)
        self.boxPositionCombo.setCurrentText(TextboxPosition(self.curMessage.boxPosition).name)
        self.boxTypeCombo.setCurrentText(OcarinaTextboxType(self.curMessage.boxType).name)

        self.messageEditor.textChanged.connect(self.MessageTextChanged)
        self.boxTypeCombo.currentTextChanged.connect(self.BoxTypeChanged)
        self.boxPositionCombo.currentTextChanged.connect(self.BoxPositionChanged)

    def MessageTextChanged(self):
        self.curMessage.textData = self.messageEditor.toPlainText()
        self.UpdateCurrentRow()

    def BoxTypeChanged(self):
        self.curMessage.boxType = OcarinaTextboxType[self.boxTypeCombo.currentText()]

    def BoxPositionChanged(self):
        self.curMessage.boxPosition = TextboxPosition[self.boxPositionCombo.currentText()]




