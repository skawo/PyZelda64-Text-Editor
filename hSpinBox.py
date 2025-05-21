from PyQt6 import  QtGui, QtWidgets

class HexSpinBox(QtWidgets.QSpinBox):
    class HexValidator(QtGui.QValidator):
        def __init__(self, min, max):
            super(HexSpinBox.HexValidator, self).__init__()
            self.valid = set('0123456789abcdef')
            self.min = min
            self.max = max

        def validate(self, input, pos):
            try:
                input = str(input).lower()
            except:
                return self.State.Invalid, input, pos
            valid = self.valid

            for char in input:
                if char not in valid:
                    return self.State.Invalid, input, pos

            value = int(input, 16)
            if value < self.min or value > self.max:
                return self.State.Intermediate, input, pos

            return self.State.Acceptable, input, pos


    def __init__(self, format='%04X', *args):
        self.format = format
        super(HexSpinBox, self).__init__(*args)
        self.validator = self.HexValidator(self.minimum(), self.maximum())

    def setMinimum(self, value):
        self.validator.min = value
        QtWidgets.QSpinBox.setMinimum(self, value)

    def setMaximum(self, value):
        self.validator.max = value
        QtWidgets.QSpinBox.setMaximum(self, value)

    def setRange(self, min, max):
        self.validator.min = min
        self.validator.max = max
        QtWidgets.QSpinBox.setMinimum(self, min)
        QtWidgets.QSpinBox.setMaximum(self, max)

    def validate(self, text, pos):
        return self.validator.validate(text, pos)

    def textFromValue(self, value):
        return self.format % value

    def valueFromText(self, value):
        return int(str(value), 16)
    
class InputBox(QtWidgets.QDialog):
    Type_TextBox = 1
    Type_SpinBox = 2
    Type_HexSpinBox = 3

    def __init__(self, parent, type=Type_TextBox):
        super().__init__()

        self.pWidget = parent
        mw = self.pWidget.parent()
        
        while (mw.parent() is not None):
            mw = self.pWidget.parent()

        self.setWindowIcon(mw.windowIcon())

        self.label = QtWidgets.QLabel('-')
        self.label.setWordWrap(True)

        if type == InputBox.Type_TextBox:
            self.textbox = QtWidgets.QLineEdit()
            widget = self.textbox
        elif type == InputBox.Type_SpinBox:
            self.spinbox = QtWidgets.QSpinBox()
            widget = self.spinbox
        elif type == InputBox.Type_HexSpinBox:
            self.spinbox = HexSpinBox()
            widget = self.spinbox

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(widget)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def show(self, title = ' ', message = ' ', value = 0, min = 0, max = 0xFFFFFFFF):
        self.setWindowTitle(title)
        self.label.setText(message)
        self.spinbox.setValue(value)
        self.spinbox.setRange(min, max)

        self.move(self.pWidget.geometry().center().x(), self.pWidget.geometry().center().y()) 
        return self.exec()