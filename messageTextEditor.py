from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QKeySequence

from zeldaEnums import *
from zeldaDicts import *
from contextMenuData import *

class CustomPlainTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = None

    def setMode(self, mode):
        self.mode = mode
        
    def contextMenuEvent(self, event):
        if self.mode is None:
            return
        
        contextMenu = QMenu(self)
        
        cutAction = QAction("Cut", self)
        cutAction.setShortcut(QKeySequence.StandardKey.Cut)
        cutAction.triggered.connect(self.cut)
        
        copyAction = QAction("Copy", self)
        copyAction.setShortcut(QKeySequence.StandardKey.Copy)
        copyAction.triggered.connect(self.copy)
        
        pasteAction = QAction("Paste", self)
        pasteAction.setShortcut(QKeySequence.StandardKey.Paste)
        pasteAction.triggered.connect(self.paste)
        
        copyCAction = QAction("Copy C String", self)
        copyCAction.triggered.connect(self.copyAsC)
        
        pasteCAction = QAction("Paste C String", self)
        pasteCAction.triggered.connect(self.pasteAsC)
        
        contextMenu.addAction(cutAction)
        contextMenu.addAction(copyAction)
        contextMenu.addAction(pasteAction)
        contextMenu.addAction(copyCAction)
        contextMenu.addAction(pasteCAction)
        
        controlTagsMenu = QMenu("Control Tags...", self)
        
        if self.mode == MessageMode.Majora:
            colorMenu = QMenu("Color", self)
            #colorMenu.setToolTip("Text until the next Color tag will be of this color. The color will persist even to the next textbox.")
            
            buttonsMenu = QMenu("Buttons", self)
            #buttonsMenu.setToolTip("Add a button icon to the textbox.")
            
            scores_menu = QMenu("Scores and timers", self)
            #scores_menu.setToolTip("Various scores and timers.")
            
            prompts_menu = QMenu("Prompts", self)
            #prompts_menu.setToolTip("Tags relating to player input.")
            
            completion_menu = QMenu("Completion-related", self)
            #completion_menu.setToolTip("Tags relating to quest completion.")
            
            soundAction = QAction("Sound...", self)
            #soundAction.setToolTip("Plays a sound effect.")
            soundAction.triggered.connect(self.soundEffClicked)
            
            self.addTagsToMenu(colorMenu, ContextMenuData.MajoraColors)
            self.addTagsToMenu(buttonsMenu, ContextMenuData.Buttons)
            self.addTagsToMenu(scores_menu, ContextMenuData.ScoresMajora)
            self.addTagsToMenu(completion_menu, ContextMenuData.CompletionMajora)
            self.addTagsToMenu(prompts_menu, ContextMenuData.PromptsMajora)
            self.addTagsToMenu(controlTagsMenu, ContextMenuData.GenericTagMajora)
            
            controlTagsMenu.addMenu(colorMenu)
            controlTagsMenu.addMenu(buttonsMenu)
            controlTagsMenu.addMenu(scores_menu)
            controlTagsMenu.addMenu(prompts_menu)
            controlTagsMenu.addMenu(completion_menu)
            controlTagsMenu.addAction(soundAction)
        else:
            colorMenu = QMenu("Color", self)
            #colorMenu.setToolTip("Text until the next Color tag (or until the end of the textbox if none are present) will be of this color.")
            
            highScoreMenu = QMenu("High Score", self)
            #highScoreMenu.setToolTip("Prints a player's high score.")
            
            buttonsMenu = QMenu("Buttons", self)
            #buttonsMenu.setToolTip("Add a button icon to the textbox.")
            
            scoreMenu = QMenu("Score", self)
            #scoreMenu.setToolTip("Prints a player's score.")
            
            iconMenu = QMenu("Icon...", self)
            #iconMenu.setToolTip("Draws specified icon inside the textbox.")
            
            soundAction = QAction("Sound...", self)
            soundAction.setToolTip("Plays a sound effect. Only one sound effect can be played per textbox.")
            soundAction.triggered.connect(self.soundEffClicked)
            
            self.addTagsToMenu(colorMenu, ContextMenuData.ColorsOcarina)
            self.addTagsToMenu(highScoreMenu, ContextMenuData.HighScoresOcarina)
            self.addTagsToMenu(buttonsMenu, ContextMenuData.Buttons)
            self.addTagsToMenu(scoreMenu, ContextMenuData.ScoresOcarina)
            self.addTagsToMenu(controlTagsMenu, ContextMenuData.GenericTagOcarina)
            
            icons = []
            for icon in OcarinaIcon:
                icons.append((icon.name, f"{OcarinaControlCode.ICON.name}:{icon.name}", ""))

            self.addTagsToMenu(iconMenu, icons)
            
            controlTagsMenu.addMenu(colorMenu)
            controlTagsMenu.addMenu(highScoreMenu)
            controlTagsMenu.addMenu(buttonsMenu)
            controlTagsMenu.addMenu(scoreMenu)
            controlTagsMenu.addMenu(iconMenu)
            controlTagsMenu.addAction(soundAction)
            
        
        contextMenu.addMenu(controlTagsMenu)
        contextMenu.exec(event.globalPos())
    
    def addTagsToMenu(self, menu, items):
        for item in items:
            if item:
                action = QAction(item[0], self)
                action.triggered.connect(lambda checked, text=item: self.insertTag(text))
                action.setToolTip(item[2])
                action.hovered.connect(self.showToolTipAction)
                menu.addAction(action)
    
    def copyAsC(self):
        pass
    
    def pasteAsC(self):
        pass
    
    def soundEffClicked(self):
        pass
    
    def insertTag(self, tag):
        cursor = self.textCursor()
        cursor.insertText(f'<{tag[1]}>')
    
    def showToolTipAction(self):
        QtWidgets.QToolTip.showText(QCursor.pos(), self.sender().toolTip())