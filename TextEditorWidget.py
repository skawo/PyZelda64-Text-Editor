import sys
import os
import struct
import threading

from PyQt6 import QtCore, QtGui, QtWidgets

class TextEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(TextEditorWidget, self).__init__(parent)

        mainLayout = QtWidgets.QGridLayout()

        # --------------- Message Grid

        messageGridLayout = QtWidgets.QVBoxLayout()

        searchField = QtWidgets.QLineEdit()
        searchField.setPlaceholderText("Type to search...")
        messageTable = QtWidgets.QTableView()
        buttonsGrid = QtWidgets.QHBoxLayout() 

        buttonAdd = QtWidgets.QPushButton("Add", self)
        changeID = QtWidgets.QPushButton("Change ID", self)
        buttonRemove = QtWidgets.QPushButton("Remove", self)

        buttonsGrid.addWidget(buttonAdd)
        buttonsGrid.addWidget(changeID)
        buttonsGrid.addWidget(buttonRemove)

        messageGridLayout.addWidget(searchField)
        messageGridLayout.addWidget(messageTable)
        messageGridLayout.addLayout(buttonsGrid)

        # --------------- Message Edit

        messageEditLayout = QtWidgets.QVBoxLayout()

        messageOptionsFrame = QtWidgets.QFrame()
        messageOptionsFrame.setLineWidth(1)
        messageOptionsFrame.setFrameStyle(QtWidgets.QFrame.Shape.StyledPanel)

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

        messageEditor = QtWidgets.QPlainTextEdit()
        messageEditLayout.addWidget(messageEditor)

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
    
    def LoadROM(self):
        return