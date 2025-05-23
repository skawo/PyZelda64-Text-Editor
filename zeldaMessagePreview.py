from PyQt6.QtGui import QImage, QColor, QPainter
from PyQt6.QtCore import QRect
from PyQt6.QtCore import Qt

from zeldaEnums import *
from zeldaDicts import *
from font import *

import graphics

class MessagePreview:

    def __init__(self, boxType, boxes):
        self.boxType = boxType
        self.boxes = boxes

    def getPreview(self, numBox):

        image = self._drawBox()
        return self._drawText(image, numBox)
      
    def getFullPreview(self):

        OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y = self._getImageSizes()

        destImage = QImage(OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y * len(self.boxes), QImage.Format.Format_ARGB32)
        destImage.fill(Qt.GlobalColor.transparent)

        painter = QPainter(destImage)

        for i in range(len(self.boxes)):           
            img = self.getPreview(i)
            painter.drawImage(0, OUTPUT_IMAGE_Y * i, img)

        painter.end()

        return destImage
    
    def _getImageSizes(self):
        x = 256 + 8
        y = 64 + 8

        if self.boxType == OcarinaTextboxType.Credits:
            x = 320
            y = 240 

        return (x, y)      
    
    def _drawBox(self):

        OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y = self._getImageSizes()

        destImage = QImage(OUTPUT_IMAGE_X, OUTPUT_IMAGE_Y, QImage.Format.Format_ARGB32)
        destImage.fill(Qt.GlobalColor.transparent)

        if self.boxType in [OcarinaTextboxType.None_White, OcarinaTextboxType.None_Black]:
            return destImage
        
        if self.boxType == OcarinaTextboxType.Black:
            imagePath = 'res/gfx/Box_Default.png'
            color = QColor(0, 0, 0, 170)
            revAlpha = True
        elif self.boxType == OcarinaTextboxType.Ocarina:
            imagePath = 'res/gfx/Box_Staff.png'
            color = QColor(255, 0, 0, 180)
            revAlpha = False
        elif self.boxType == OcarinaTextboxType.Wooden:
            imagePath = 'res/gfx/Box_Wooden.png'
            color = QColor(70, 50, 30, 230)
            revAlpha = False
        elif self.boxType == OcarinaTextboxType.Blue:
            imagePath = 'res/gfx/Fading_Box.png'
            color = QColor(0, 10, 50, 170)
            revAlpha = True
        else:
            destImage.fill(QColor(0, 0, 0))   
            return destImage     

        sourceImage = QImage(imagePath)  
        return self._drawBoxInternal(destImage, sourceImage, color, revAlpha)

    def _drawBoxInternal(self, destImage, sourceImage, color, rev_alpha):

        if rev_alpha:
            sourceImage = graphics.reverseAlphaMask(sourceImage)

        sourceImage = graphics.colorize(sourceImage, color)

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

        textColor = QColor(0, 0, 0) if self.boxType == OcarinaTextboxType.None_Black else QColor(255, 255, 255)
        painter = QPainter(dest_img)
        painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform)
        
        charIdx = 0

        while charIdx < len(textbox.data):
            curByte = textbox.data[charIdx]
            
            if curByte == OcarinaControlCode.TWO_CHOICES.value:
                imgArrow = QImage("res/gfx/Box_Arrow.png")
                xPosArrow = 16
                yPosArrow = 32
                
                for _ in range(2):
                    self._draw(painter, imgArrow, ABUTTON_COLOR, int(16 * scale), int(16 * scale), xPosArrow, yPosArrow, True)
                    yPosArrow += LINEBREAK_SIZE

            elif curByte == OcarinaControlCode.THREE_CHOICES.value:
                imgArrow = QImage("res/gfx/Box_Arrow.png")
                xPosArrow = 16
                yPosArrow = 20
                
                for _ in range(3):
                    self._draw(painter, imgArrow, ABUTTON_COLOR, int(16 * scale), int(16 * scale), xPosArrow, yPosArrow, True)
                    yPosArrow += LINEBREAK_SIZE

            elif curByte == OcarinaControlCode.ICON:
                icon_n = textbox.data[charIdx + 1]
                fn = f"icon_{str(icon_n).lower()}"
                img = QImage(f"res/gfx/{fn}.png")

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
                left_img = QImage("res/gfx/xmes_left.png")
                right_img = QImage("res/gfx/xmes_right.png")

                x_pos_bg = 0
                y_pos_bg = 0

                self._draw(painter, left_img, QColor(255, 255, 255), left_img.width(), left_img.height(), x_pos_bg, y_pos_bg, True)
                x_pos_bg += left_img.width()
                self._draw(painter, right_img, QColor(255, 255, 255), left_img.width(), left_img.height(), x_pos_bg, y_pos_bg, True)

                charIdx += 3
                continue

            elif curByte == OcarinaControlCode.SHIFT:
                num_shift = textbox.data[charIdx + 1]
                xPos += num_shift
                charIdx += 1

            elif curByte == OcarinaControlCode.COLOR:
                color_data_idx = textbox.data[charIdx + 1]

                if (self.boxType == OcarinaTextboxType.Wooden):
                    textColor = ocarinaWoodTextColors[color_data_idx]
                else:
                    textColor = ocarinaTextColors[color_data_idx]

                charIdx += 1

            elif curByte == OcarinaControlCode.LINE_BREAK.value:
                if self.boxType == OcarinaTextboxType.Credits:
                    xPos = 20
                    yPos += 6
                else:
                    xPos = XPOS_DEFAULT
                    yPos += LINEBREAK_SIZE

                if ((textbox.numChoices == 2 and yPos >= 32) or 
                    (textbox.numChoices  == 3 and yPos >= 20) or 
                    (textbox.iconUsed != -1 and yPos > 12)):
                    xPos = 2 * XPOS_DEFAULT

            elif curByte == ord(' '):
                xPos += (FONT_WIDTHS[0] * scale)
            
            else:
                img = fontDataOcarina[curByte]

                img = graphics.reverseAlphaMask(img)

                if self.boxType != OcarinaTextboxType.None_Black:
                    shadow = img.copy()
                    shadow = graphics.colorize(shadow, QColor(0, 0, 0))
                    painter.drawImage(QRect(int(xPos + 1), int(yPos + 1), int(16 * scale), int(16 * scale)), shadow)

                img = graphics.colorize(img, textColor)
                painter.drawImage(QRect(int(xPos), int(yPos), int(16 * scale), int(16 * scale)), img)

                try:
                    xPos += int(FONT_WIDTHS[curByte - 0x20] * scale)
                except Exception:
                    xPos += 16 * scale             

            charIdx += 1

        if textbox.endType != BoxEndType.NoEndMarker:
            if textbox.endType == BoxEndType.Triangle and textbox.isLast:
                img = QImage(f"res/gfx/Box_End.png")
            else:
                img = QImage(f"res/gfx/Box_Triangle.png")

            self._draw(painter, img, ABUTTON_COLOR, int(16 * scale), int(16 * scale), 124, 60, True)

        painter.end()
        return dest_img
    
    def _draw(self, painter, srcImage, color, x_size, y_size, x_pos, y_pos, rev_alpha):
        
        if rev_alpha:
            srcImage = graphics.reverseAlphaMask(srcImage)

        srcImage = graphics.colorize(srcImage, color)
        
        target_rect = QRect(int(x_pos), int(y_pos), x_size, y_size)
        painter.drawImage(target_rect, srcImage)
