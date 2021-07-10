from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class QDMNodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.label = QLabel("Some title")
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit("foo")
        self.layout.addWidget(self.text_edit)
