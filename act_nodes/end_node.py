from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel

from act_nodes.act_node_widget import ActNodeWidget
from sub_widgets import DeleteProofLineEdit


class EndNode(ActNodeWidget):
    serialize_fields = ActNodeWidget.serialize_fields + [('ending_id', int)]

    def __init__(self, node=None, parent=None):
        self._ending_id = 1
        super().__init__(node, parent)
        self.ending_id = 1

    @property
    def ending_id(self):
        return self._ending_id

    @ending_id.setter
    def ending_id(self, value):
        self._ending_id = int(value)
        if self._node is not None:
            self.num_edit.setText(str(value))

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)

        self.layout.addWidget(QLabel('Ending Id'))
        self.num_edit = DeleteProofLineEdit(str(self._ending_id), self.node)
        self.num_edit.setValidator(QIntValidator(0, 1000, self))
        self.num_edit.textChanged.connect(self.on_change_ending_id)
        self.layout.addWidget(self.num_edit)

    def on_change_ending_id(self):
        self._ending_id = int(self.num_edit.text())

    @staticmethod
    def get_name():
        return 'EndNode'

    @staticmethod
    def get_image():
        return ActNodeWidget.load_from_icons('end_node.png')
