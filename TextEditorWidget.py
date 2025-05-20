import sys
import os
import struct
import threading

from PyQt6 import QtCore, QtGui, QtWidgets

class TextEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(TextEditorWidget, self).__init__(parent)

        mainLayout = QtWidgets.QGridLayout()

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

        messageEditLayout = QtWidgets.QVBoxLayout()




        messageOptionsLayout = QtWidgets.QGridLayout()

        boxTypeLabel = QtWidgets.QLabel("Box Type:", self)
        boxPositionLabel = QtWidgets.QLabel("Box Position:", self)

        boxTypeCombo = QtWidgets.QComboBox()
        boxPositionCombo = QtWidgets.QComboBox()

        messageOptionsLayout.addWidget(boxTypeLabel, 0, 0)
        messageOptionsLayout.addWidget(boxTypeCombo, 0, 1)
        messageOptionsLayout.addWidget(boxPositionLabel, 1, 0)
        messageOptionsLayout.addWidget(boxPositionCombo, 1, 1)

        messageEditLayout.addLayout(messageOptionsLayout)

        messageEditor = QtWidgets.QPlainTextEdit()
        messageEditLayout.addWidget(messageEditor)

        messagePreviewLayout = QtWidgets.QVBoxLayout()
        messagePreview = QtWidgets.QLabel()
        messagePreview.setFixedWidth(300)


        messagePreviewLayout.addWidget(messagePreview)












        mainLayout.addLayout(messageGridLayout, 0, 0)
        mainLayout.addLayout(messageEditLayout, 0, 1)
        mainLayout.addLayout(messagePreviewLayout, 0, 2)




    

        self.setLayout(mainLayout)



        self.changesMade = False

        return
    
    def LoadROM(self):
        return