from act_nodes.act_node_widget import ActNodeWidget
from gui.widgets import DeleteProofLineEdit


class CharacterNode(ActNodeWidget):
    serialize_fields = ActNodeWidget.serialize_fields + [('character_id', int)]

    def __init__(self, node=None, parent=None):
        self._character_id = 0
        super().__init__(node, parent)
        self.initial_delay = 500
        self.auto_skip_delay = 0

    @property
    def character_id(self):
        return self._character_id

    @character_id.setter
    def character_id(self, value):
        self._character_id = value
        if self._node is not None:
            self.character_edit.setText(value)

    def init_ui(self):
        super().init_ui()
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(1)

        self.character_edit = DeleteProofLineEdit(str(self._character_id), self.node)
        self.character_edit.textChanged.connect(self.on_change_character)
        self.layout.addWidget(self.character_edit)

    def on_change_character(self):
        self._character_id = int(self.character_edit.text())

    @staticmethod
    def get_name():
        return 'CharacterNode'
