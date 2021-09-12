from PyQt5.QtWidgets import QWidget


class ProxyWidget(QWidget):
    def __init__(self, layout, parent):
        super().__init__(parent)
        self.setLayout(layout)