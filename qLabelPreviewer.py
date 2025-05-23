from PyQt6 import  QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QColor

class QLabelPreviewer(QtWidgets.QLabel):
    def __init__(self):
        super(QLabelPreviewer, self).__init__()
        img = QPixmap(1, 1)
        img.fill(Qt.GlobalColor.transparent)
        self.pixmapOg = img
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Preferred)

    def setPixmap(self, pixmap, setOg = True):
        if setOg:
            self.pixmapOg = pixmap.copy()

        return super().setPixmap(pixmap)

    def resizeEvent(self, a0):
        if self.pixmapOg is not None:
            self.setPixmap(self.pixmapOg.scaledToWidth(self.width(), Qt.TransformationMode.SmoothTransformation), False)
    
        return super().resizeEvent(a0)
    
