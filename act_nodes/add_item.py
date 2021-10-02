from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel

from act_nodes.act_node_widget import ActNodeWidget
from sub_widgets import DeleteProofLineEdit


class AddItem(ActNodeWidget):
    icon = 'add_item.png'
    serialize_fields = ActNodeWidget.serialize_fields + [('item_id', str), ('number', int)]

    def __init__(self, node=None, parent=None):
        self._item_id = ''
        self._number = 1
        super().__init__(node, parent)

    @property
    def item_id(self):
        return self._item_id

    @item_id.setter
    def item_id(self, value):
        self._item_id = value
        if self._node is not None:
            self.item_id_edit.setText(value)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        if self._node is not None:
            self.number_edit.setText(str(value))

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(1)

        self.layout.addWidget(QLabel('Item Id:'))
        self.item_id_edit = DeleteProofLineEdit(self._item_id, self.node)
        self.item_id_edit.textChanged.connect(self.on_change_item_id)
        self.layout.addWidget(self.item_id_edit)

        self.layout.addWidget(QLabel('Number:'))
        self.number_edit = DeleteProofLineEdit(str(self._number), self.node)
        self.number_edit.setValidator(QIntValidator(-10000, 10000, self))
        self.number_edit.textChanged.connect(self.on_change_number)
        self.layout.addWidget(self.number_edit)

        super().init_sub_class_ui()

    def on_change_item_id(self):
        self._item_id = self.item_id_edit.text()

    def on_change_number(self):
        self._number = int(self.number_edit.text())
