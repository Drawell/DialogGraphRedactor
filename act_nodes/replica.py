from act_nodes.act_node_widget import ActNodeWidget
from sub_widgets import DeleteProofTextEdit


class Replica(ActNodeWidget):
    serialize_fields = ActNodeWidget.serialize_fields + [('replica_text', str)]

    def __init__(self, node=None, parent=None):
        self._replica_text = ''
        super().__init__(node, parent)
        self.initial_delay = 1000
        self.auto_skip_delay = 0
        self.is_add_stretch = False

    @property
    def replica_text(self):
        return self._replica_text

    @replica_text.setter
    def replica_text(self, value):
        self._replica_text = value
        if self._node is not None:
            self.text_edit.setText(value)

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(1)

        self.text_edit = DeleteProofTextEdit(self._replica_text, self.node)
        self.text_edit.textChanged.connect(self.on_change_text)
        self.layout.addWidget(self.text_edit)

    def on_change_text(self):
        self._replica_text = self.text_edit.toPlainText()

    @staticmethod
    def get_name():
        return 'Replica'

    @staticmethod
    def get_image():
        return ActNodeWidget.load_from_icons('replica.png')
