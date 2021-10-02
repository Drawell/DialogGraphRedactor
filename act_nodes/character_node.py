from act_nodes.act_node_with_delay import ActNodeWithDelay
from acts_system import Character
from sub_widgets.character_select import CharacterSelect


class CharacterNode(ActNodeWithDelay):
    serialize_fields = ActNodeWithDelay.serialize_fields + [('character_id', str)]

    def __init__(self, node=None, parent=None):
        self._character_id = Character.teller_character().char_id
        super().__init__(node, parent)
        self.initial_delay = 500
        self.auto_skip_delay = 0

    @property
    def character_id(self):
        return self.char_select.current_character_id()

    @character_id.setter
    def character_id(self, value):
        self._character_id = value
        if self._node is not None:
            self.char_select.set_current_character_id(value)

    def init_sub_class_ui(self):
        self.node.set_inputs_count(1)
        self.node.set_outputs_count(1)

        self.char_select = CharacterSelect()
        self.char_select.set_current_character_id(self._character_id)
        self.layout.addWidget(self.char_select)

        super().init_sub_class_ui()

    def set_act(self, act):
        super().set_act(act)
        self.char_select.set_act(act)

    def remove(self):
        self.char_select.remove()
