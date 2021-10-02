from act_nodes.act_node_with_delay import ActNodeWithDelay
from acts_system import Character
from acts_system.character_emotion import CharacterEmotion
from sub_widgets import DeleteProofTextEdit
from sub_widgets.character_select import CharacterSelect
from sub_widgets.emotion_select import EmotionSelect


class Replica(ActNodeWithDelay):
    icon = 'replica.png'
    serialize_fields = ActNodeWithDelay.serialize_fields + [('character_id', str), ('emotion', CharacterEmotion),
                                                            ('replica_text', str)]

    def __init__(self, node=None, parent=None):
        self._character_id = Character.teller_character().char_id
        self._emotion = CharacterEmotion.NEUTRAL
        self._replica_text = ''
        super().__init__(node, parent)
        self.initial_delay = 1000
        self.auto_skip_delay = 0
        self.is_add_stretch = False

    def set_act(self, act):
        super().set_act(act)
        self.char_select.set_act(act)

    @property
    def character_id(self):
        return self.char_select.current_character_id()

    @character_id.setter
    def character_id(self, value):
        self._character_id = value
        if self._node is not None:
            self.char_select.set_current_character_id(value)

    @property
    def emotion(self):
        return self.emotion_select.current_emotion()

    @emotion.setter
    def emotion(self, value):
        self._emotion = value
        if self._node is not None:
            self.emotion_select.set_emotion(value)


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

        self.char_select = CharacterSelect()
        self.char_select.set_current_character_id(self._character_id)
        self.layout.addWidget(self.char_select)

        self.emotion_select = EmotionSelect(self._emotion)
        self.layout.addWidget(self.emotion_select)

        self.text_edit = DeleteProofTextEdit(self._replica_text, self.node)
        self.text_edit.textChanged.connect(self.on_change_text)
        self.layout.addWidget(self.text_edit)
        super().init_sub_class_ui()

    def on_change_text(self):
        self._replica_text = self.text_edit.toPlainText()
