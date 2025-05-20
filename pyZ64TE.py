import sys
import TextEditorWidget
import ZeldaMessage

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

        saveAction = QtGui.QAction('&Save', self)
        saveAction.triggered.connect(self.HandleSave)
        
        saveAsAction = QtGui.QAction('&Save as...', self)
        saveAsAction.triggered.connect(self.HandleSaveAs)

        saveAsSeparateAction = QtGui.QAction('&Save to separate files...', self)
        saveAsSeparateAction.triggered.connect(self.HandleSaveAsSeparate)
        
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(self.HandleCloseApplication)

        fileMenu.addAction(openAction)
        fileMenu.addAction(openSeparateAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(saveAsSeparateAction)
        fileMenu.addAction(exitAction)

        toolsMenu = mainMenu.addMenu('&Tools')

        reSortAction = QtGui.QAction('&Re-sort entries', self)
        reSortAction.triggered.connect(self.HandleResort)

        importDataAction = QtGui.QAction('&Import data', self)
        importDataAction.triggered.connect(self.HandleImport)

        removeEmptyAction = QtGui.QAction('&Remove empty entries', self)
        removeEmptyAction.triggered.connect(self.HandleRemoveEmpty)

        exportToJSONAction = QtGui.QAction('&Export to JSON...', self)
        exportToJSONAction.triggered.connect(self.HandleExportJSON)        

        importFromJSONAction = QtGui.QAction('&Insert from JSON...', self)
        importFromJSONAction.triggered.connect(self.HandleImportJSON) 

        toolsMenu.addAction(reSortAction)
        toolsMenu.addAction(importDataAction)
        toolsMenu.addAction(removeEmptyAction)
        toolsMenu.addAction(exportToJSONAction)
        toolsMenu.addAction(importFromJSONAction)

        aboutMenu = mainMenu.addMenu('&Help')
        
        aboutAction = QtGui.QAction('&About', self)
        aboutAction.triggered.connect(self.HandleAbout)      
    
        aboutMenu.addAction(aboutAction)

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

    def HandleSave(self):
        self.messageEditor.SaveCurTextboxDebug()
        return
        
    def HandleAbout(self):
        QtWidgets.QMessageBox.information(self, 'About', 'Zelda 64 Text Editor v. 0.1 by Skawo')

    def HandleSaveAs(self):
        return

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

                    messageList = ZeldaMessage.GetMessageList(tableData, stringData, mode)

                    if (messageList is None):
                        QtWidgets.QMessageBox.information(self, 'Error', 'An error occurred while parsing the data.')
                    else:
                        self.messageEditor.PopulateEditor(messageList, mode)
        return

    def HandleSaveAsSeparate(self):
        return

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

def main():
    global app, mainwindow
    
    app = QtWidgets.QApplication([])
    
    mainwindow = MainEditorWindow()
    mainwindow.show()
    app.exec()

if __name__ == '__main__':
    main()
