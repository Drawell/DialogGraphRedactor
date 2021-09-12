from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel

from sub_widgets import DeleteProofLineEdit
from .character_node import CharacterNode


class CharacterAppearance(CharacterNode):
    icon = 'character_appearance.png'
    serialize_fields = CharacterNode.serialize_fields + [('position', int)]

    def __init__(self, node=None, parent=None):
        self._position = 1
        super().__init__(node, parent)
        self.position = 1

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = int(value)
        if self._node is not None:
            self.position_edit.setText(str(value))

    def init_sub_class_ui(self):
        super().init_sub_class_ui()

        self.layout.addWidget(QLabel('Position:'))
        self.position_edit = DeleteProofLineEdit(str(self._position), self.node)
        self.position_edit.setValidator(QIntValidator(0, 5, self))
        self.position_edit.textChanged.connect(self.on_change_position)
        self.layout.addWidget(self.position_edit)

    def on_change_position(self):
        self._position = int(self.position_edit.text())
