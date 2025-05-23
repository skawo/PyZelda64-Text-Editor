from PyQt6.QtGui import QImage
from zeldaEnums import *

fontDataOcarina = []

for i in range(0xAB):
    fn = f"char_{hex(i)[2:].lower()}"
    img = QImage(f"res/gfx/{fn}.png")
    fontDataOcarina.append(img)