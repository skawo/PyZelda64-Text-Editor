from PyQt6.QtGui import QImage, QColor
from zeldaEnums import *

def reverseAlphaMask(image):

        width = image.width()
        height = image.height()
        
        result = QImage(width, height, QImage.Format.Format_ARGB32)
        
        for y in range(height):
            for x in range(width):
                oColor = QColor(image.pixel(x, y))
                new_color = QColor(255, 255, 255, oColor.red())
                result.setPixel(x, y, new_color.rgba())
        
        return result

def colorize(image, color):

    r = color.red() / 255.0
    g = color.green() / 255.0
    b = color.blue() / 255.0
    
    width = image.width()
    height = image.height()

    result = QImage(image.size(), QImage.Format.Format_ARGB32)
    
    for y in range(height):
        for x in range(width):
            pixel = image.pixel(x, y)
            alpha = (pixel >> 24) & 0xFF
            red = (pixel >> 16) & 0xFF
            green = (pixel >> 8) & 0xFF
            blue = pixel & 0xFF                

            newColor = QColor(int(red * r), int(green * g), int(blue * b), alpha)
            result.setPixel(x, y, newColor.rgba())
    
    return result


boxDefault = colorize(reverseAlphaMask(QImage('res/gfx/Box_Default.png')), QColor(0, 0, 0, 170))
boxWood = colorize(QImage('res/gfx/Box_Wooden.png'), QColor(70, 50, 30, 230))
boxBlue = colorize(reverseAlphaMask(QImage('res/gfx/Fading_Box.png')), QColor(0, 10, 50, 170))
boxStaff = colorize(QImage('res/gfx/Box_Staff.png'), QColor(255, 0, 0, 180))

leftBackground = reverseAlphaMask(QImage("res/gfx/xmes_left.png"))
rightBackground = reverseAlphaMask(QImage("res/gfx/xmes_right.png"))
arrow = reverseAlphaMask(QImage("res/gfx/Box_Arrow.png"))

boxEndTriangle = reverseAlphaMask(QImage("res/gfx/Box_Triangle.png"))
boxEndBox = reverseAlphaMask(QImage("res/gfx/Box_End.png"))

fontDataOcarina = []
fontDataShadowOcarina = []
iconDataOcarina = []

for i in range(OcarinaControlCode.D_PAD):
    fn = f"char_{hex(i)[2:].lower()}"
    img = reverseAlphaMask(QImage(f"res/gfx/{fn}.png"))
    fontDataOcarina.append(img)
    img = colorize(img, QColor(0, 0, 0))
    fontDataShadowOcarina.append(img)

for i in range(OcarinaIcon.BIG_MAGIC_JAR):
    fn = f"icon_{str(i).lower()}"   
    img = QImage(f"res/gfx/{fn}.png")
    iconDataOcarina.append(img)

boxDefaultBombers = colorize(reverseAlphaMask(QImage('res/gfx/Box_Default.png')), QColor(255, 255, 255, 255))
boxBombers = colorize(reverseAlphaMask(QImage('res/gfx/majora_Box_Bomber.png')), QColor(250, 253, 213, 255))
boxRed = colorize(reverseAlphaMask(QImage('res/gfx/Box_Default.png')), QColor(255, 0, 0, 170)) 

fontDataMajora = []
fontDataShadowMajora = []
iconDataMajora = []

for i in range(MajoraControlCode.D_PAD):
    fn = f"majora_char_{hex(i)[2:].lower()}"
    img = reverseAlphaMask(QImage(f"res/gfx/{fn}.png"))
    fontDataMajora.append(img)
    img = colorize(img, QColor(0, 0, 0))
    fontDataShadowMajora.append(img)

for i in range(MajoraIcon.EXCLAMATION_MARK):
    fn = f"majora_icon_{str(i).lower()}"   
    img = QImage(f"res/gfx/{fn}.png")
    iconDataMajora.append(img)