import sys
import os
import TextEditorWidget
import ZeldaMessage

from ZeldaEnums import *
from PyQt6 import QtGui, QtWidgets

class MainEditorWindow(QtWidgets.QMainWindow):

    def CreateMenuBar(self):

        self.setWindowIcon(QtGui.QIcon('res/z64text.ico'))

        self.statusBar()
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')
      
        openAction = QtGui.QAction('&Open...', self)
        openAction.triggered.connect(self.HandleOpenROM)

        openSeparateAction = QtGui.QAction('&Open separate files...', self)
        openSeparateAction.triggered.connect(self.HandleOpenFiles)

        self.saveAction = QtGui.QAction('&Save', self)
        self.saveAction.triggered.connect(self.HandleSave)
        
        self.saveAsAction = QtGui.QAction('&Save as...', self)
        self.saveAsAction.triggered.connect(self.HandleSaveAs)

        self.saveAsSeparateAction = QtGui.QAction('&Save to separate files...', self)
        self.saveAsSeparateAction.triggered.connect(self.HandleSaveAsSeparate)
        
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
        self.reSortAction.triggered.connect(self.HandleResort)

        self.importDataAction = QtGui.QAction('&Import data', self)
        self.importDataAction.triggered.connect(self.HandleImport)

        self.removeEmptyAction = QtGui.QAction('&Remove empty entries', self)
        self.removeEmptyAction.triggered.connect(self.HandleRemoveEmpty)

        self.exportToJSONAction = QtGui.QAction('&Export to JSON...', self)
        self.exportToJSONAction.triggered.connect(self.HandleExportJSON)        

        self.importFromJSONAction = QtGui.QAction('&Insert from JSON...', self)
        self.importFromJSONAction.triggered.connect(self.HandleImportJSON) 

        toolsMenu.addAction(self.reSortAction)
        toolsMenu.addAction(self.importDataAction)
        toolsMenu.addAction(self.removeEmptyAction)
        toolsMenu.addAction(self.exportToJSONAction)
        toolsMenu.addAction(self.importFromJSONAction)

        aboutMenu = mainMenu.addMenu('&Help')
        
        aboutAction = QtGui.QAction('&About', self)
        aboutAction.triggered.connect(self.HandleAbout)      
    
        aboutMenu.addAction(aboutAction)

        self.__ChangeStatusBarEnableStatus(False)

    def __init__(self):
        super(MainEditorWindow, self).__init__()
        self.setGeometry(50, 50, 1000, 600)
        self.setWindowTitle('Zelda 64 Text Editor')

        self.CreateMenuBar()
        self.CreateEditor()

    def CreateEditor(self):
        self.messageEditor = TextEditorWidget.TextEditorWidget(self)
        self.setCentralWidget(self.messageEditor)

    def HandleCloseApplication(self):
        if self.UnsavedChanges():
            sys.exit()

    def __GetDataToSave(self):
        return ZeldaMessage.ConvertMessageList(self.messageEditor.messageList, self.messageEditor.messageMode)

    def __SaveFiles(self, path1, path2):
        records, strings = self.__GetDataToSave()

        with open(path1, 'wb') as f:
            f.write(records)

        with open(path2, 'wb') as f:
            f.write(strings)        

    def HandleSave(self):
        #if self.destPath2 is None, then assume we're saving to ROM.
        if self.destPath2 is not None:
            self.__SaveFiles(self.destPath1, self.destPath2)
        
    def HandleSaveAs(self):
        if self.destPath2 is not None:
            self.HandleSaveAsSeparate()
    
    def HandleSaveAsSeparate(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(self, 
                                                                'Choose directory...', "", 
                                                                QtWidgets.QFileDialog.Option.ShowDirsOnly | QtWidgets.QFileDialog.Option.DontResolveSymlinks);
        if folderPath == '': return
        else:     
            path1 = os.path.join(folderPath, f"{SAVE_TABLE_FILENAME}.tbl")
            path2 = os.path.join(folderPath, f"{SAVE_STRINGS_FILENAME}.tbl")
            self.__SaveFiles(path1, path2)      

    def HandleOpenROM(self):
        if self.UnsavedChanges():
            fileName = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                            'Choose a file...', 
                                                            '', 
                                                            'Nintendo 64 ROMs (*.z64;*.n64);;All Files(*)')[0]
            if fileName == '': return
            else:     
                self.messageEditor.LoadROM(fileName)
                
    def HandleOpenFiles(self):
        if self.UnsavedChanges():
            tableFileName = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                            'Choose the Message Table...', 
                                                            '', 
                                                            'Table Data (*.tbl);;All Files(*)')[0]


            if tableFileName == '': return
            else:
                stringFileName = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                'Choose the String Data...', 
                                                                '', 
                                                                'String Data (*.bin);;All Files(*)')[0]

                if stringFileName == '': return
                else:
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

                    messageList = ZeldaMessage.GetMessageList(tableData, stringData, mode)
                    
                    if (messageList is None):
                        QtWidgets.QMessageBox.information(self, 'Error', 'An error occurred while parsing the data.')
                    else:
                        self.__ChangeStatusBarEnableStatus(True)
                        self.messageEditor.PopulateEditor(messageList, mode)
        return
    
    def __ChangeStatusBarEnableStatus(self, set):

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

    def HandleResort(self):
        return

    def HandleRemoveEmpty(self):
        return
    
    def HandleImport(self):
        return

    def HandleExportJSON(self):
        return

    def HandleImportJSON(self):
        return
    
    def UnsavedChanges(self):
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
        
    def HandleAbout(self):
        QtWidgets.QMessageBox.information(self, 'About', 'Zelda 64 Text Editor v. 0.1 by Skawo')


def main():
    global app, mainwindow
    
    app = QtWidgets.QApplication([])
    
    mainwindow = MainEditorWindow()
    mainwindow.show()
    app.exec()

if __name__ == '__main__':
    main()
