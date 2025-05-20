import sys
import os
import struct
import threading
import ZeldaMessage

from PyQt6 import QtCore, QtGui, QtWidgets
from typing import List

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

        boxTypeCombo = QtWidgets.QComboBox()
        boxPositionCombo = QtWidgets.QComboBox()

        messageOptionsLayout.addWidget(boxTypeLabel, 0, 0)
        messageOptionsLayout.addWidget(boxTypeCombo, 0, 1)
        messageOptionsLayout.addWidget(boxPositionLabel, 1, 0)
        messageOptionsLayout.addWidget(boxPositionCombo, 1, 1)

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
        self.zm = ZeldaMessage.ZeldaMessage()

        return
    
    def LoadROM(self):
        return

    def LoadFiles(self, tableFileName, stringFileName):
        tableFile = open(tableFileName, "rb")
        stringFile = open(stringFileName, "rb")

        self.tableData = tableFile.read()
        self.stringData = stringFile.read()

        self.messageList = self.zm.GetMessageList(self.tableData, self.stringData)

        if (self.messageList is None):
            pass
        else:
            self.InsertMessages(self.messageList)


        return

    def InsertMessages(self, messageList):

        self.messageTable.itemSelectionChanged.disconnect

        for message in messageList:
            self.messageTable.insertRow(self.messageTable.rowCount()) 
            id = QtWidgets.QTableWidgetItem('0x' + format(message.messageId & 0xffff, '04X'))
            text = QtWidgets.QTableWidgetItem(message.textData)
            self.messageTable.setItem(self.messageTable.rowCount()-1, 0, id)
            self.messageTable.setItem(self.messageTable.rowCount()-1, 1, text)

        self.messageTable.itemSelectionChanged.connect(self.messageTableItemChanged)

    def messageTableItemChanged(self):

        self.messageEditor.setPlainText(self.messageTable.selectedItems()[1].text())



