from PyQt5.QtWidgets import QLabel

from act_nodes.act_node_with_delay import ActNodeWithDelay
from sub_widgets import DeleteProofLineEdit


class SetLandscape(ActNodeWithDelay):
    icon = 'set_landscape.png'
    serialize_fields = ActNodeWithDelay.serialize_fields + [('landscape_id', str)]

    def __init__(self, node=None, parent=None):
        self._landscape_id = ''
        super().__init__(node, parent)
        self.initial_delay = 1000
        self.auto_skip_delay = 0

    @property
    def landscape_id(self):
        return self._landscape_id

    @landscape_id.setter
    def landscape_id(self, value):
        self._landscape_id = value
        if self._node is not None:
            self.text_edit.setText(value)

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(1)

        self.layout.addWidget(QLabel('Landscape Id:'))
        self.text_edit = DeleteProofLineEdit(self._landscape_id, self.node)
        self.text_edit.textChanged.connect(self.on_change_text)
        self.layout.addWidget(self.text_edit)

        super().init_sub_class_ui()

    def on_change_text(self):
        self._landscape_id = self.text_edit.text()
