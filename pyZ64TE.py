import sys
import os
import textEditorWidget
import zeldaMessage

from zeldaEnums import *
from PyQt6 import QtGui, QtWidgets

class mainEditorWindow(QtWidgets.QMainWindow):

    def createMenuBar(self):

        self.setWindowIcon(QtGui.QIcon('res/z64text.ico'))

        self.statusBar()
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')
      
        openAction = QtGui.QAction('&Open...', self)
        openAction.triggered.connect(self.handleOpenROM)

        openSeparateAction = QtGui.QAction('&Open separate files...', self)
        openSeparateAction.triggered.connect(self.handleOpenFiles)

        self.saveAction = QtGui.QAction('&Save', self)
        self.saveAction.triggered.connect(self.handleSave)
        
        self.saveAsAction = QtGui.QAction('&Save as...', self)
        self.saveAsAction.triggered.connect(self.handleSaveAs)

        self.saveAsSeparateAction = QtGui.QAction('&Save to separate files...', self)
        self.saveAsSeparateAction.triggered.connect(self.handleSaveAsSeparate)
        
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(self.HandleCloseApplication)

        fileMenu.addAction(openAction)
        fileMenu.addAction(openSeparateAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.saveAsSeparateAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        toolsMenu = mainMenu.addMenu('&Tools')

        self.reSortAction = QtGui.QAction('&Re-sort entries', self)
        self.reSortAction.triggered.connect(self.handleResort)

        self.importDataAction = QtGui.QAction('&Import data', self)
        self.importDataAction.triggered.connect(self.handleImport)

        self.removeEmptyAction = QtGui.QAction('&Remove empty entries', self)
        self.removeEmptyAction.triggered.connect(self.handleRemoveEmpty)

        self.exportToJSONAction = QtGui.QAction('&Export to JSON...', self)
        self.exportToJSONAction.triggered.connect(self.handleExportJSON)        

        self.importFromJSONAction = QtGui.QAction('&Insert from JSON...', self)
        self.importFromJSONAction.triggered.connect(self.handleImportJSON) 

        toolsMenu.addAction(self.reSortAction)
        toolsMenu.addAction(self.importDataAction)
        toolsMenu.addAction(self.removeEmptyAction)
        toolsMenu.addAction(self.exportToJSONAction)
        toolsMenu.addAction(self.importFromJSONAction)

        aboutMenu = mainMenu.addMenu('&Help')
        
        aboutAction = QtGui.QAction('&About', self)
        aboutAction.triggered.connect(self.handleAbout)      
    
        aboutMenu.addAction(aboutAction)

        self._changeStatusBarEnableStatus(False)

    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 1000, 600)
        self.setWindowTitle('Zelda 64 Text Editor')

        self.createMenuBar()
        self.CreateEditor()

    def CreateEditor(self):
        self.messageEditor = textEditorWidget.textEditorWidget(self)
        self.setCentralWidget(self.messageEditor)

    def HandleCloseApplication(self):
        if self.askUnsavedChanges():
            sys.exit()

    def _getDataToSave(self):
        return zeldaMessage.convertMessageList(self.messageEditor.messageList, self.messageEditor.messageMode)

    def _saveFiles(self, path1, path2):
        records, strings = self._getDataToSave()

        with open(path1, 'wb') as f:
            f.write(records)

        with open(path2, 'wb') as f:
            f.write(strings)        

    def handleSave(self):
        #if self.destPath2 is None, then assume we're saving to ROM.
        if self.destPath2 is not None:
            self._saveFiles(self.destPath1, self.destPath2)
        
    def handleSaveAs(self):
        if self.destPath2 is not None:
            self.handleSaveAsSeparate()
    
    def handleSaveAsSeparate(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            'Choose directory...',
            '', 
            QtWidgets.QFileDialog.Option.ShowDirsOnly | QtWidgets.QFileDialog.Option.DontResolveSymlinks
        )

        if folderPath == '': return
        else:     
            path1 = os.path.join(folderPath, f"{SAVE_TABLE_FILENAME}.tbl")
            path2 = os.path.join(folderPath, f"{SAVE_STRINGS_FILENAME}.tbl")
            self._saveFiles(path1, path2)      

    def handleOpenROM(self):
        if self.askUnsavedChanges():
            fileName = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                            'Choose a file...', 
                                                            '', 
                                                            'Nintendo 64 ROMs (*.z64;*.n64);;All Files(*)')[0]
            if fileName != '':
                self.messageEditor.LoadROM(fileName)
                
    def handleOpenFiles(self):
        if self.askUnsavedChanges():
            tableFileName = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                            'Choose the Message Table...', 
                                                            '', 
                                                            'Table Data (*.tbl);;All Files(*)')[0]


            if tableFileName != '':
                stringFileName = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                'Choose the String Data...', 
                                                                '', 
                                                                'String Data (*.bin);;All Files(*)')[0]

                if stringFileName != '':
                    msgBox = QtWidgets.QMessageBox(self)
                    msgBox.setWindowTitle(" ")
                    msgBox.setText("These files are...?")
                    msgBox.addButton("Ocarina", QtWidgets.QMessageBox.ButtonRole.NoRole)
                    msgBox.addButton("Majora", QtWidgets.QMessageBox.ButtonRole.NoRole)
                    msgBox.addButton("Credits", QtWidgets.QMessageBox.ButtonRole.NoRole)
                    mode = msgBox.exec()
                    mode -= 2

                    tableFile = open(tableFileName, "rb")
                    stringFile = open(stringFileName, "rb")

                    tableData = tableFile.read()
                    stringData = stringFile.read()

                    self.destPath1 = tableFileName
                    self.destPath2 = stringFileName

                    messageList = zeldaMessage.getMessageList(tableData, stringData, mode)
                    
                    if messageList is None:
                        QtWidgets.QMessageBox.information(self, 'Error', 'An error occurred while parsing the data.')
                    else:
                        self._changeStatusBarEnableStatus(True)
                        self.messageEditor.populateEditor(messageList, mode)
        return
    
    def _changeStatusBarEnableStatus(self, set):

        toEnable = [self.reSortAction, 
                    self.importDataAction, 
                    self.removeEmptyAction,
                    self.exportToJSONAction,
                    self.importFromJSONAction,
                    self.saveAction,
                    self.saveAsAction,
                    self.saveAsSeparateAction]      

        for wid in toEnable:
            wid.setEnabled(set) 

    def handleResort(self):
        return

    def handleRemoveEmpty(self):
        return
    
    def handleImport(self):
        return

    def handleExportJSON(self):
        return

    def handleImportJSON(self):
        return
    
    def askUnsavedChanges(self):
        if self.messageEditor.changesMade:
            Reply = QtWidgets.QMessageBox.question(self, 
                                                  'Unsaved changes', 
                                                  'You have unsaved changes. Would you like to save them first?', 
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

            if Reply == QtWidgets.QMessageBox.Yes:
                self.messageEditor.Save()
                return True
            elif Reply == QtWidgets.QMessageBox.Cancel:
                return False      
            else:
                return True
        else:
            return True
        
    def handleAbout(self):
        QtWidgets.QMessageBox.information(self, 'About', 'Zelda 64 Text Editor v. 0.1 by Skawo')


def main():
    global app, mainwindow
    
    app = QtWidgets.QApplication([])
    
    mainwindow = mainEditorWindow()
    mainwindow.show()
    app.exec()

if __name__ == '__main__':
    main()
