from gui.act_node_widget import ActNodeWidget
from gui.widgets import QDMTextEdit


class Replica(ActNodeWidget):
    serialize_fields = ActNodeWidget.serialize_fields + [('replica_text', str)]

    def __init__(self, node=None, parent=None):
        super().__init__(node, parent)
        self._replica_text = 'Hi'

    @property
    def replica_text(self):
        return self._replica_text

    @replica_text.setter
    def replica_text(self, value):
        self._replica_text = value
        self.text_edit.setText(value)

    def init_ui(self):
        super().init_ui()
        self.text_edit = QDMTextEdit("foo", self.node)
        self.text_edit.textChanged.connect(self.on_change_text)
        self.layout.addWidget(self.text_edit)

    def on_change_text(self):
        self._replica_text = self.text_edit.toPlainText()

    @staticmethod
    def get_name():
        return 'Replica'

