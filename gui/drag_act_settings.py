from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit


class DragActSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.act = None  # type: Act

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout.addWidget(QLabel('Act Name:', self))
        self.tale_name_edit = QLineEdit('', self)
        self.tale_name_edit.textChanged.connect(self.on_tale_name_changed)
        layout.addWidget(self.tale_name_edit)

        layout.addWidget(QLabel('Act Id:', self))
        self.act_id_edit = QLineEdit('', self)
        self.act_id_edit.textChanged.connect(self.on_act_id_changed)
        self.act_id_edit.setValidator(QIntValidator(0, 1000, self))
        layout.addWidget(self.act_id_edit)

        layout.addStretch()

    def set_act(self, act):
        self.act = act
        self.act_id_edit.setText(str(act.act_id))
        self.tale_name_edit.setText(act.tale_name)

    def on_act_id_changed(self):
        self.act.act_id = int(self.act_id_edit.text())

    def on_tale_name_changed(self):
        self.act.tale_name = self.tale_name_edit.text()

