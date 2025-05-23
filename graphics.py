from PyQt6.QtGui import QImage, QColor

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