from act_nodes.act_node_with_delay import ActNodeWithDelay
from sub_widgets import DeleteProofLineEdit


class Choice(ActNodeWithDelay):
    icon = 'choice.png'
    serialize_fields = ActNodeWithDelay.serialize_fields + [('choices', str)]

    def __init__(self, node=None, parent=None):
        self._choices = 4 * ['']
        super().__init__(node, parent)
        self.initial_delay = 0
        self.auto_skip_delay = -1
        self.next_nodes_id = 4 * [-1]

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        self._choices = value
        if self._node is not None:
            for idx, choice in enumerate(self._choices):
                self.text_edits[idx].setText(choice)

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(4)
        self.text_edits = []
        for idx in range(4):
            self.add_choice_text_edit(idx)

        super().init_sub_class_ui()

    def add_choice_text_edit(self, idx):
        self.text_edits.append(DeleteProofLineEdit(self._choices[idx], self.node))
        self.text_edits[idx].textChanged.connect(self.create_on_change_text(idx))
        self.layout.addWidget(self.text_edits[idx])

    def create_on_change_text(self, idx):
        def on_change_text(value):
            self._choices[idx] = value

        return on_change_text



