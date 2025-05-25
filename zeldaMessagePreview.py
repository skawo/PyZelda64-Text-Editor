from PyQt6.QtGui import QImage, QColor, QPainter
from PyQt6.QtCore import QRect
from PyQt6.QtCore import Qt

from zeldaEnums import *
from zeldaDicts import *

import graphics

SPACER_HEIGHT = 5

class MessagePreviewOcarina:

    def __init__(self, boxType, boxes):
        self.boxType = boxType
        self.boxes = boxes
        self.textColor = ocarinaTextColors[OcarinaMsgColor.BLK] if self.boxType == OcarinaTextboxType.None_Black else ocarinaTextColors[OcarinaMsgColor.D]

    def getPreview(self, numBox):

        image = self._drawBox()
        return self._drawText(image, numBox)
      
    def getFullPreview(self):

        OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y = self.getImageSizes()

        destImage = QImage(OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y * len(self.boxes) + SPACER_HEIGHT * len(self.boxes) , QImage.Format.Format_ARGB32)
        destImage.fill(Qt.GlobalColor.transparent)

        painter = QPainter(destImage)

        for i in range(len(self.boxes)):           
            img = self.getPreview(i)
            painter.drawImage(0, OUTPUT_IMAGE_Y * i + SPACER_HEIGHT * i, img)

        painter.end()

        return destImage
    
    def getImageSizes(self):
        x = 256
        y = 72

        if self.boxType == OcarinaTextboxType.Credits:
            x = 320
            y = 240
        elif self.boxType >= OcarinaTextboxType.None_White:
            x = 320

        return (x, y)      
    
    def _drawBox(self):

        OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y = self.getImageSizes()

        destImage = QImage(OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y, QImage.Format.Format_ARGB32)
        destImage.fill(Qt.GlobalColor.transparent)

        if self.boxType == OcarinaTextboxType.None_White:
            destImage.fill(Qt.GlobalColor.black)
            return destImage
        elif self.boxType == OcarinaTextboxType.None_Black:
            destImage.fill(Qt.GlobalColor.white)
            return destImage
        else:
            destImage.fill(Qt.GlobalColor.transparent)
        
        if self.boxType == OcarinaTextboxType.Black:
            sourceImage = graphics.boxDefault
        elif self.boxType == OcarinaTextboxType.Ocarina:
            sourceImage = graphics.boxStaff
        elif self.boxType == OcarinaTextboxType.Wooden:
            sourceImage = graphics.boxWood
        elif self.boxType == OcarinaTextboxType.Blue:
            sourceImage = graphics.boxBlue
        else:
            destImage.fill(QColor(0, 0, 0))   
            return destImage     
        
        painter = QPainter(destImage)
        painter.drawImage(0, 0, sourceImage)
        painter.drawImage(sourceImage.width(), 0, sourceImage.mirrored(True, False))
        painter.end()

        return destImage

    def _drawText(self, dest_img, numBox):

        textbox = self.boxes[numBox]
        
        xPos = XPOS_DEFAULT
        yPos = 36 if self.boxType == OcarinaTextboxType.None_White else max(YPOS_DEFAULT, (52 - (LINEBREAK_SIZE * textbox.numLinebreaks)) / 2)
        scale = SCALE_DEFAULT

        if self.boxType == OcarinaTextboxType.Credits:
            xPos = 20
            yPos = 48
            scale = 0.85

        painter = QPainter(dest_img)
        painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform)
        
        charIdx = 0

        while charIdx < len(textbox.data):
            curByte = textbox.data[charIdx]
            
            if curByte == OcarinaControlCode.TWO_CHOICES:
                xPosArrow = 16
                yPosArrow = 32
                
                for _ in range(2):
                    self._draw(painter, graphics.arrow, A_BUTTON_COLOR, int(16 * scale), int(16 * scale), xPosArrow, yPosArrow, False)
                    yPosArrow += LINEBREAK_SIZE

            elif curByte == OcarinaControlCode.THREE_CHOICES:
                xPosArrow = 16
                yPosArrow = 20
                
                for _ in range(3):
                    self._draw(painter, graphics.arrow, A_BUTTON_COLOR, int(16 * scale), int(16 * scale), xPosArrow, yPosArrow, False)
                    yPosArrow += LINEBREAK_SIZE

            elif curByte == OcarinaControlCode.ICON:
                icon_n = textbox.data[charIdx + 1]

                if icon_n < len(graphics.iconDataOcarina):
                    img = graphics.iconDataOcarina[icon_n]
                
                    if img and not img.isNull():
                        if icon_n < OcarinaIcon.FOREST_MEDALLION:
                            xPosIcon = xPos - 10
                            yPosIcon = 36 if self.boxType == OcarinaTextboxType.None_White else 0x10
                            self._draw(painter, img, QColor(255, 255, 255), 32, 32, xPosIcon, yPosIcon, False)
                        else:
                            xPosIcon = xPos - 7
                            yPosIcon = 36 if self.boxType == OcarinaTextboxType.None_White else 0x14
                            self._draw(painter, img, QColor(255, 255, 255), 24, 24, xPosIcon, yPosIcon, False)

                xPos += 0x20
                charIdx += 1

            elif curByte == OcarinaControlCode.BACKGROUND:
                x_pos_bg = 0
                y_pos_bg = 0

                width = graphics.leftBackground.width()
                height = graphics.leftBackground.height()

                self._draw(painter, graphics.leftBackground, QColor(255, 255, 255), width, height, x_pos_bg, y_pos_bg, False)
                x_pos_bg += width
                self._draw(painter, graphics.rightBackground, QColor(255, 255, 255), width, height, x_pos_bg, y_pos_bg, False)

                charIdx += 3

            elif curByte == OcarinaControlCode.SHIFT:
                num_shift = textbox.data[charIdx + 1]
                xPos += num_shift
                charIdx += 1

            elif curByte == OcarinaControlCode.COLOR:
                colorId = textbox.data[charIdx + 1]

                if colorId in ocarinaTextColors:
                    if self.boxType == OcarinaTextboxType.Wooden:
                        self.textColor = ocarinaWoodTextColors[colorId]
                    elif self.boxType == OcarinaTextboxType.None_Black and colorId == OcarinaMsgColor.D:
                        self.textColor = ocarinaTextColors[OcarinaMsgColor.BLK]     
                    else:
                        self.textColor = ocarinaTextColors[colorId]

                charIdx += 1

            elif curByte == OcarinaControlCode.LINE_BREAK.value:
                if self.boxType == OcarinaTextboxType.Credits:
                    xPos = 20
                    yPos += 6
                else:
                    xPos = XPOS_DEFAULT
                    yPos += LINEBREAK_SIZE

                if ((textbox.numChoices == 2 and yPos >= 32) or 
                    (textbox.numChoices == 3 and yPos >= 20) or 
                    (textbox.iconUsed != -1 and yPos > 12)):
                    xPos = 2 * XPOS_DEFAULT
            else:
                xPos, yPos = self._drawChar(painter, curByte, scale, self.textColor, xPos, yPos)           

            charIdx += 1

        if textbox.endType != BoxEndType.NoEndMarker:
            if textbox.endType == BoxEndType.Triangle and textbox.isLast:
                img = graphics.boxEndBox
            else:
                img = graphics.boxEndTriangle

            self._draw(painter, img, A_BUTTON_COLOR, int(16 * scale), int(16 * scale), 124, 60, False)

        painter.end()
        return dest_img
    
    def _drawChar(self, painter, curByte, scale, color, xPos, yPos):
        if curByte == ord(' '):
            xPos += (OCARINA_FONT_WIDTHS[0] * scale)
        else:
            if curByte < len(graphics.fontDataOcarina):
                img = graphics.fontDataOcarina[curByte]
                
                if self.boxType != OcarinaTextboxType.None_Black:
                    shadow = graphics.fontDataShadowOcarina[curByte]
                    painter.drawImage(QRect(int(xPos + 1), int(yPos + 1), int(16 * scale), int(16 * scale)), shadow)

                img = graphics.colorize(img, color)
                painter.drawImage(QRect(int(xPos), int(yPos), int(16 * scale), int(16 * scale)), img)

            if curByte < len(OCARINA_FONT_WIDTHS):
                xPos += int(OCARINA_FONT_WIDTHS[curByte - 0x20] * scale)
            else:
                xPos += 16 * scale

        return xPos, yPos


    def _draw(self, painter, srcImage, color, x_size, y_size, x_pos, y_pos, rev_alpha):
        
        if rev_alpha:
            srcImage = graphics.reverseAlphaMask(srcImage)

        srcImage = graphics.colorize(srcImage, color)
        
        target_rect = QRect(int(x_pos), int(y_pos), x_size, y_size)
        painter.drawImage(target_rect, srcImage)

class MessagePreviewMajora:

    def __init__(self, boxType, isBomberNotebook, boxes):
        self.boxType = boxType
        self.boxes = boxes
        self.isBomberNotebook = isBomberNotebook

        self.textColorIndex = 3 if self.isBomberNotebook else boxTextColorIndexes[self.boxType]
        self.textColor = majoraTextColors[MajoraControlCode.COLOR_DEFAULT][self.textColorIndex]

    def getPreview(self, numBox):

        image = self._drawBox()
        return self._drawText(image, numBox)
      
    def getFullPreview(self):

        OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y = self.getImageSizes()

        destImage = QImage(OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y * len(self.boxes) + SPACER_HEIGHT * len(self.boxes) , QImage.Format.Format_ARGB32)
        destImage.fill(Qt.GlobalColor.transparent)

        painter = QPainter(destImage)

        for i in range(len(self.boxes)):           
            img = self.getPreview(i)
            painter.drawImage(0, OUTPUT_IMAGE_Y * i + SPACER_HEIGHT * i, img)

        painter.end()

        return destImage
    
    def getImageSizes(self):
        x = 256
        y = 72

        if self.isBomberNotebook:
            x = 280
            y = 58
        elif self.boxType == MajoraTextboxType.Credits:
            x = 320
            y = 240
        elif self.boxType in (MajoraTextboxType.None_White,
                              MajoraTextboxType.None_Black):
            x = 320

        return (x, y)      
    
    def _drawBox(self):

        OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y = self.getImageSizes()

        destImage = QImage(OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y, QImage.Format.Format_ARGB32)
        destImage.fill(Qt.GlobalColor.transparent)

        if self.boxType == MajoraTextboxType.None_White:
            destImage.fill(Qt.GlobalColor.black)
            return destImage
        elif self.boxType == MajoraTextboxType.None_Black:
            destImage.fill(Qt.GlobalColor.white)
            return destImage
        else:
            destImage.fill(Qt.GlobalColor.transparent)
        
        if self.isBomberNotebook:
            sourceImage = graphics.boxBombers
        elif self.boxType in (MajoraTextboxType.Black,
                              MajoraTextboxType.Black2):
            sourceImage = graphics.boxDefault
        elif self.boxType == MajoraTextboxType.Ocarina:
            sourceImage = graphics.boxStaff
        elif self.boxType == MajoraTextboxType.Wooden:
            sourceImage = graphics.boxWood
        elif self.boxType in (MajoraTextboxType.Blue,
                              MajoraTextboxType.Blue2):
            sourceImage = graphics.boxBlue
        elif self.boxType in (MajoraTextboxType.Red,
                              MajoraTextboxType.Red2):
            sourceImage = graphics.boxRed
        else:
            destImage.fill(QColor(0, 0, 0))   
            return destImage     
        
        painter = QPainter(destImage)
        painter.drawImage(0, 0, sourceImage)
        painter.drawImage(sourceImage.width(), 0, sourceImage.mirrored(True, False))
        painter.end()

        return destImage

    def _getTextProperties(self, numLines, numChoices):
        xPos = XPOS_DEFAULT
        xPosDefault = XPOS_DEFAULT
        yPos = YPOS_DEFAULT
        scale = SCALE_DEFAULT

        if numChoices == 2:
            if self.isBomberNotebook:
                xPos = XPOS_DEFAULT
            else:
                xPos = XPOS_DEFAULT
                yPos = 26 - (6 * numLines)
                
        elif numChoices == 3:
            if self.isBomberNotebook:
                xPos = XPOS_DEFAULT + 13
            else:
                xPos = XPOS_DEFAULT + 22
                yPos = 26 - (6 * numLines)
        else:
            if self.isBomberNotebook:
                xPosDefault = 8
                xPos = xPosDefault
                yPos = max(6, 18 - (6 * numLines))
            else:
                xPosDefault = 32

                if self.boxType == MajoraTextboxType.None_White:
                    yPos = 36
                elif self.boxType == MajoraTextboxType.Ocarina:
                    yPos = 2
                elif self.boxType == MajoraTextboxType.Credits:
                    xPos = 20
                    yPos = 48
                    scale = 0.85
                else:
                    yPos = max(YPOS_DEFAULT, (52 - (LINEBREAK_SIZE * numLines)) / 2)
        
        return xPos, xPosDefault, yPos, scale

    def _drawText(self, dest_img, numBox):

        textbox = self.boxes[numBox]
        
        xPos, xPosDefault, yPos, scale = self._getTextProperties(textbox.numLinebreaks, textbox.numChoices)

        painter = QPainter(dest_img)
        painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform)
        
        charIdx = 0
        numCurLineBreak = 0

        while charIdx < len(textbox.data):
            curByte = textbox.data[charIdx]

            if MajoraControlCode.A_BUTTON <= curByte <= MajoraControlCode.D_PAD:
                xPos, yPos = self._drawChar(painter, curByte, scale, majoraSpecificTagTextColor[curByte][self.textColorIndex], xPos, yPos)

            elif curByte == MajoraControlCode.TWO_CHOICES:
                xPosArrow = 13
                yPosArrow = 25

                if textbox.numLineBreaks >= 3:
                    yPosArrow += 7
                
                for _ in range(2):
                    self._draw(painter, graphics.arrow, A_BUTTON_COLOR, int(16 * scale), int(16 * scale), xPosArrow, yPosArrow, False)
                    yPosArrow += LINEBREAK_SIZE

            elif curByte == MajoraControlCode.THREE_CHOICES:
                xPosArrow = 13
                yPosArrow = 13

                if textbox.numLineBreaks >= 3:
                    yPosArrow += 7
                
                for _ in range(3):
                    self._draw(painter, graphics.arrow, A_BUTTON_COLOR, int(16 * scale), int(16 * scale), xPosArrow, yPosArrow, False)
                    yPosArrow += LINEBREAK_SIZE

            elif curByte == MajoraControlCode.BACKGROUND:
                x_pos_bg = 0
                y_pos_bg = 0

                width = graphics.leftBackground.width()
                height = graphics.leftBackground.height()

                self._draw(painter, graphics.leftBackground, QColor(255, 255, 255), width, height, x_pos_bg, y_pos_bg, False)
                x_pos_bg += width
                self._draw(painter, graphics.rightBackground, QColor(255, 255, 255), width, height, x_pos_bg, y_pos_bg, False)

                charIdx += 3

            elif curByte == MajoraControlCode.SHIFT:
                num_shift = textbox.data[charIdx + 1]
                xPos += num_shift
                charIdx += 1

            elif curByte in (MajoraControlCode.COLOR_DEFAULT,
                             MajoraControlCode.COLOR_RED,
                             MajoraControlCode.COLOR_GREEN,
                             MajoraControlCode.COLOR_BLUE,
                             MajoraControlCode.COLOR_YELLOW,
                             MajoraControlCode.COLOR_NAVY,
                             MajoraControlCode.COLOR_PINK,
                             MajoraControlCode.COLOR_SILVER,
                             MajoraControlCode.COLOR_ORANGE):
                
                self.textColor = majoraTextColors[curByte][self.textColorIndex]

            elif curByte == MajoraControlCode.LINE_BREAK:

                numCurLineBreak += 1
                yPos += LINEBREAK_SIZE

                if (textbox.iconUsed  != 0xFE and numCurLineBreak > 1) or (textbox.iconUsed  != 0xFE and textbox.numChoices == 0):
                    xPos = xPosDefault + (0x1C if self.isBomberNotebook else 0xE)
                else:
                    xPos = xPosDefault

                if textbox.numChoices == 2 and numCurLineBreak >= (self.numLinebreaks - 1):
                    xPos = xPosDefault + (30 if self.isBomberNotebook else 10)

                if textbox.numChoices == 3 and numCurLineBreak >= (self.numLinebreaks - 2):
                    xPos = xPosDefault + (13 if self.isBomberNotebook else 22)
                
            else:
                xPos, yPos = self._drawChar(painter, curByte, scale, self.textColor, xPos, yPos)             

            charIdx += 1

        if textbox.endType != BoxEndType.NoEndMarker and self.isBomberNotebook == False:
            if textbox.endType == BoxEndType.Triangle and textbox.isLast:
                img = graphics.boxEndBox
            else:
                img = graphics.boxEndTriangle

            self._draw(painter, img, A_BUTTON_COLOR, int(16 * scale), int(16 * scale), 124, 60, False)

        painter.end()
        return dest_img
    
    def _drawChar(self, painter, curByte, scale, color, xPos, yPos):
        if curByte == ord(' '):
            xPos += 3 if self.isBomberNotebook else (MAJORA_FONT_WIDTHS[0] * scale)
        else:
            if curByte < len(graphics.fontDataMajora):
                img = graphics.fontDataMajora[curByte]
                
                if self.boxType not in (MajoraTextboxType.None_Black, MajoraTextboxType.Bombers_Notebook) and self.isBomberNotebook == False:
                    shadow = graphics.fontDataShadowMajora[curByte]
                    painter.drawImage(QRect(int(xPos + 1), int(yPos + 1), int(16 * scale), int(16 * scale)), shadow)

                img = graphics.colorize(img, color)
                painter.drawImage(QRect(int(xPos), int(yPos), int(16 * scale), int(16 * scale)), img)

            if curByte < len(MAJORA_FONT_WIDTHS):
                xPos += int(MAJORA_FONT_WIDTHS[curByte - 0x20] * scale)
            else:
                xPos += 16 * scale

        return xPos, yPos
    
    def _draw(self, painter, srcImage, color, x_size, y_size, x_pos, y_pos, rev_alpha):
        
        if rev_alpha:
            srcImage = graphics.reverseAlphaMask(srcImage)

        srcImage = graphics.colorize(srcImage, color)
        
        target_rect = QRect(int(x_pos), int(y_pos), x_size, y_size)
        painter.drawImage(target_rect, srcImage)
