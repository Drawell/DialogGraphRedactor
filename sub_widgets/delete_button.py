from PyQt5.QtWidgets import QPushButton


class QDMDeleteButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__('x', parent)

