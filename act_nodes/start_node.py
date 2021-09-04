from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel

from act_nodes.act_node_widget import ActNodeWidget
from gui.widgets import DeleteProofLineEdit


class StartNode(ActNodeWidget):
    serialize_fields = ActNodeWidget.serialize_fields + [('act_num', int), ('act_name', str)]

    def __init__(self, node=None, parent=None):
        self._act_num = 1
        self._act_name = 'No Name'
        super().__init__(node, parent)
        #self.node.remove_input()
        self.act_num = 1
        self.act_name = 'No Name'

    @property
    def act_num(self):
        return self._act_num

    @act_num.setter
    def act_num(self, value):
        self._act_num = int(value)
        if self._node is not None:
            self.num_edit.setText(str(value))

    @property
    def act_name(self):
        return self._act_name

    @act_name.setter
    def act_name(self, value):
        self._act_name = value
        if self._node is not None:
            self.name_edit.setText(value)

    def init_ui(self):
        super().init_ui()
        self.node.set_outputs_count(1)

        self.layout.addWidget(QLabel('Act Number:'))
        self.num_edit = DeleteProofLineEdit(str(self._act_num), self.node)
        self.num_edit.setValidator(QIntValidator(0, 100, self))
        self.num_edit.textChanged.connect(self.on_change_num)
        self.layout.addWidget(self.num_edit)

        self.layout.addWidget(QLabel('Act Name:'))
        self.name_edit = DeleteProofLineEdit(str(self._act_name), self.node)
        self.name_edit.textChanged.connect(self.on_change_name)
        self.layout.addWidget(self.name_edit)

        self.layout.addStretch()

    def on_change_num(self):
        self._act_num = int(self.num_edit.text())

    def on_change_name(self):
        self._act_name = self.name_edit.text()

    @staticmethod
    def get_name():
        return 'StartNode'

    @staticmethod
    def get_image():
        return ActNodeWidget.load_from_icons('start_node.png')
