from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel

from act_nodes.act_node_widget import ActNodeWidget
from sub_widgets import DeleteProofLineEdit


class ActNodeWithDelay(ActNodeWidget):
    def __init__(self, node=None, parent=None):
        super().__init__(node, parent)
        self.initial_delay = 0
        self.auto_skip_delay = 0

    @property
    def initial_delay(self):
        return self._initial_delay

    @initial_delay.setter
    def initial_delay(self, value):
        self._initial_delay = int(value)
        if self._node is not None:
            self.initial_delay_edit.setText(str(value))

    @property
    def auto_skip_delay(self):
        return self._auto_skip_delay

    @auto_skip_delay.setter
    def auto_skip_delay(self, value):
        self._auto_skip_delay = int(value)
        if self._node is not None:
            self.auto_skip_delay_edit.setText(str(value))

    def init_sub_class_ui(self):
        self.layout.addWidget(QLabel('Initial Delay:'))
        self.initial_delay_edit = DeleteProofLineEdit(str(self._initial_delay), self.node)
        self.initial_delay_edit.setValidator(QIntValidator(-10, 10000, self))
        self.initial_delay_edit.textChanged.connect(self.on_initial_delay_changed)
        self.layout.addWidget(self.initial_delay_edit)

        self.layout.addWidget(QLabel('AutoSkipDelay:'))
        self.auto_skip_delay_edit = DeleteProofLineEdit(str(self.auto_skip_delay), self.node)
        self.auto_skip_delay_edit.setValidator(QIntValidator(-10, 10000, self))
        self.auto_skip_delay_edit.textChanged.connect(self.on_auto_skip_delay_changed)
        self.layout.addWidget(self.auto_skip_delay_edit)

    def on_initial_delay_changed(self):
        try:
            self._initial_delay = int(self.initial_delay_edit.text())
        except:
            pass

    def on_auto_skip_delay_changed(self):
        try:
            self._auto_skip_delay = int(self.auto_skip_delay_edit.text())
        except:
            pass
