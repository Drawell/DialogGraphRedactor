from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QHBoxLayout

from act_nodes.act_node_widget import ActNodeWidget
from sub_widgets import DeleteProofLineEdit


class SwitchByItem(ActNodeWidget):
    icon = 'switch_by_item.png'
    serialize_fields = ActNodeWidget.serialize_fields + [('item_id', str), ('maximal_threshold', int),
                                                         ('minimal_threshold', int)]

    def __init__(self, node=None, parent=None):
        self._item_id = ''
        self._maximal_threshold = 1
        self._minimal_threshold = 1
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
    def maximal_threshold(self):
        return self._maximal_threshold

    @maximal_threshold.setter
    def maximal_threshold(self, value):
        self._maximal_threshold = value
        if self._node is not None:
            self.maximal_threshold_edit.setText(str(value))

    @property
    def minimal_threshold(self):
        return self._minimal_threshold

    @minimal_threshold.setter
    def minimal_threshold(self, value):
        self._minimal_threshold = int(value)
        if self._node is not None:
            self.minimal_threshold_edit.setText(str(value))

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(3)

        self.layout.addWidget(QLabel('Item Id:'))
        self.item_id_edit = DeleteProofLineEdit(self._item_id, self.node)
        self.item_id_edit.textChanged.connect(self.on_change_item_id)
        self.layout.addWidget(self.item_id_edit)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('>='))
        self.layout.addWidget(QLabel('Maximal Threshold ->'))
        self.maximal_threshold_edit = DeleteProofLineEdit(str(self._maximal_threshold), self.node)
        self.maximal_threshold_edit.setValidator(QIntValidator(-10000, 10000, self))
        self.maximal_threshold_edit.textChanged.connect(self.on_change_maximal_threshold)
        layout.addWidget(self.maximal_threshold_edit)

        self.layout.addLayout(layout)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('>='))
        self.layout.addWidget(QLabel('Minimal Threshold ->'))
        self.minimal_threshold_edit = DeleteProofLineEdit(str(self._minimal_threshold), self.node)
        self.minimal_threshold_edit.setValidator(QIntValidator(-10000, 10000, self))
        self.minimal_threshold_edit.textChanged.connect(self.on_change_minimal_threshold)
        layout.addWidget(self.minimal_threshold_edit)

        self.layout.addLayout(layout)

        self.layout.addWidget(QLabel('Else ->'))
        super().init_sub_class_ui()

    def on_change_item_id(self):
        self._item_id = self.item_id_edit.text()

    def on_change_maximal_threshold(self):
        self._maximal_threshold = int(self.maximal_threshold_edit.text())

    def on_change_minimal_threshold(self):
        self._minimal_threshold = int(self.minimal_threshold_edit.text())
