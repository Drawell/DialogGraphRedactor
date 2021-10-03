from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel

from act_nodes.act_node_widget import ActNodeWidget
from sub_widgets import DeleteProofLineEdit


class AddItem(ActNodeWidget):
    icon = 'add_item.png'
    serialize_fields = ActNodeWidget.serialize_fields + [('item_id', str), ('amount', int)]

    def __init__(self, node=None, parent=None):
        self._item_id = ''
        self._amount = 1
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
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
        if self._node is not None:
            self.amount_edit.setText(str(value))

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(1)

        self.layout.addWidget(QLabel('Item Id:'))
        self.item_id_edit = DeleteProofLineEdit(self._item_id, self.node)
        self.item_id_edit.textChanged.connect(self.on_change_item_id)
        self.layout.addWidget(self.item_id_edit)

        self.layout.addWidget(QLabel('amount:'))
        self.amount_edit = DeleteProofLineEdit(str(self._amount), self.node)
        self.amount_edit.setValidator(QIntValidator(-10000, 10000, self))
        self.amount_edit.textChanged.connect(self.on_change_amount)
        self.layout.addWidget(self.amount_edit)

        super().init_sub_class_ui()

    def on_change_item_id(self):
        self._item_id = self.item_id_edit.text()

    def on_change_amount(self):
        try:
            self._amount = int(self.amount_edit.text())
        except:
            pass
