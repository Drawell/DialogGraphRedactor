from act_nodes.act_node_widget import ActNodeWidget
from sub_widgets import DeleteProofTextEdit


class Choice(ActNodeWidget):
    serialize_fields = ActNodeWidget.serialize_fields + [('choices', str)]

    def __init__(self, node=None, parent=None):
        self._choices = []
        super().__init__(node, parent)
        self.initial_delay = 0
        self.auto_skip_delay = -1

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        self._choices = value
        if self._node is not None:
            self.text_edit.setText('\n'.join(self._choices))

    def init_ui(self):
        super().init_ui()
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(1)

        self.text_edit = DeleteProofTextEdit('\n'.join(self._choices), self.node)
        self.text_edit.textChanged.connect(self.on_change_text)
        self.layout.addWidget(self.text_edit)

    def on_change_text(self):
        self._choices = self.text_edit.toPlainText().split('\n')

    @staticmethod
    def get_name():
        return 'Choice'

    @staticmethod
    def get_image():
        return ActNodeWidget.load_from_icons('choice.png')
