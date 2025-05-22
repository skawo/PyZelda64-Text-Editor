import sys
import os
import textEditorWidget
import zeldaMessage

from zeldaEnums import *
from pathlib import Path
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QProgressDialog, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class MainEditorWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.resize(1000, 600)
        self.setWindowTitle('Zelda 64 Text Editor')

        self.createMenuBar()
        self.CreateEditor()

    def createMenuBar(self):

        self.setWindowIcon(QtGui.QIcon('res/z64text.ico'))

        self.statusBar()
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('File')
      
        openAction = QtGui.QAction('Open...', self)
        openAction.triggered.connect(self.handleOpenROM)

        openSeparateAction = QtGui.QAction('Open separate files...', self)
        openSeparateAction.triggered.connect(self.handleOpenFiles)

        self.saveAction = QtGui.QAction('Save', self)
        self.saveAction.triggered.connect(self.handleSave)
        
        self.saveAsAction = QtGui.QAction('Save as...', self)
        self.saveAsAction.triggered.connect(self.handleSaveAs)

        self.saveAsSeparateAction = QtGui.QAction('Save to separate files...', self)
        self.saveAsSeparateAction.triggered.connect(self.handleSaveAsSeparate)
        
        exitAction = QtGui.QAction('Exit', self)
        exitAction.triggered.connect(self.HandleCloseApplication)

        fileMenu.addAction(openAction)
        fileMenu.addAction(openSeparateAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.saveAsSeparateAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        toolsMenu = mainMenu.addMenu('Tools')

        self.reSortAction = QtGui.QAction('Re-sort entries', self)
        self.reSortAction.triggered.connect(self.handleResort)

        self.importDataAction = QtGui.QAction('Import data', self)
        self.importDataAction.triggered.connect(self.handleImport)

        self.removeEmptyAction = QtGui.QAction('Remove empty entries', self)
        self.removeEmptyAction.triggered.connect(self.handleRemoveEmpty)

        self.exportToJSONAction = QtGui.QAction('Export to JSON...', self)
        self.exportToJSONAction.triggered.connect(self.handleExportJSON)        

        self.importFromJSONAction = QtGui.QAction('Insert from JSON...', self)
        self.importFromJSONAction.triggered.connect(self.handleImportJSON) 

        toolsMenu.addAction(self.reSortAction)
        toolsMenu.addAction(self.importDataAction)
        toolsMenu.addAction(self.removeEmptyAction)
        toolsMenu.addAction(self.exportToJSONAction)
        toolsMenu.addAction(self.importFromJSONAction)

        aboutMenu = mainMenu.addMenu('Help')
        
        aboutAction = QtGui.QAction('About', self)
        aboutAction.triggered.connect(self.handleAbout)      
    
        aboutMenu.addAction(aboutAction)

        self._changeStatusBarEnableStatus(False)

    def CreateEditor(self):
        self.messageEditor = textEditorWidget.TextEditorWidget(self)
        self.setCentralWidget(self.messageEditor)

    def HandleCloseApplication(self):
        if self.askUnsavedChanges():
            sys.exit()

    def _getDataToSave(self):
        progress = QProgressDialog("Saving messages...", None, 0, 100, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setWindowTitle(" ")
        progress.setMinimumDuration(0)
        progress.setValue(0)
        
        self.worker = MessageSavingThread(self.messageEditor)
        
        def handle_progress(current, total):
            if total > 0:
                percentage = (current * 100) // total
                progress.setValue(percentage)
                progress.setLabelText(f"Saving messages... ({current}/{total})")
        
        def handle_result(result):
            progress.close()
            errors, data1, data2 = result
            
            if errors == ParseErrors.Parse:
                QMessageBox.warning(self, 'Error', f"Errors parsing message {zeldaMessage.formatMessageID(data1)}:\n" + "\n".join(data2))
            elif errors == ParseErrors.Length:
                QMessageBox.warning(self, 'Error', f"Message ID {zeldaMessage.formatMessageID(data1)} is too long.")
            
            self.thread_result = (data1, data2) if errors == ParseErrors.NoError else (None, None)
        
        self.worker.progress.connect(handle_progress)
        self.worker.finished.connect(handle_result)
        self.worker.start()
        
        progress.exec()
        
        self.worker.wait()
        return self.thread_result

    def _saveFiles(self, path1, path2):
        records, strings = self._getDataToSave()

        if records is not None and strings is not None:
            Path(path1).write_bytes(records)
            Path(path2).write_bytes(strings)      

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

        if folderPath != '':
            path1 = os.path.join(folderPath, f"{SAVE_TABLE_FILENAME}.tbl")
            path2 = os.path.join(folderPath, f"{SAVE_STRINGS_FILENAME}.bin")
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
                    msgBox.setText("Select the file type:")
                    msgBox.addButton("Ocarina", QMessageBox.ButtonRole.NoRole)
                    msgBox.addButton("Majora", QMessageBox.ButtonRole.NoRole)
                    msgBox.addButton("Credits", QMessageBox.ButtonRole.NoRole)
                    mode = msgBox.exec()
                    mode -= 2

                    tableData = Path(tableFileName).read_bytes()
                    stringData = Path(stringFileName).read_bytes()

                    self.destPath1 = tableFileName
                    self.destPath2 = stringFileName

                    messageList = zeldaMessage.getMessageList(tableData, stringData, mode)
                    
                    if messageList is None:
                        QMessageBox.information(self, 'Error', 'An error occurred while parsing the data. Are you sure you chose the right game?')
                    else:
                        self._changeStatusBarEnableStatus(True)
                        self.messageEditor.populateEditor(messageList, mode)
    
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


class MessageSavingThread(QThread):
    finished = pyqtSignal(tuple)
    progress = pyqtSignal(int, int)
    
    def __init__(self, messageEditor):
        super().__init__()
        self.messageEditor = messageEditor
        
    def progress_callback(self, current, total):
        self.progress.emit(current, total)
        
    def run(self):
        errors, data1, data2 = zeldaMessage.convertMessageList(
            self.messageEditor.messageList, 
            self.messageEditor.messageMode,
            progress_callback=self.progress_callback 
        )
        
        self.finished.emit((errors, data1, data2))


def main():
    global app, mainwindow
    
    app = QtWidgets.QApplication([])
    
    mainwindow = MainEditorWindow()
    mainwindow.show()
    app.exec()

if __name__ == '__main__':
    main()