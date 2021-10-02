from enum import Enum

from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtWidgets import QLabel, QComboBox

from acts_system.character_position import CharacterPosition
from sub_widgets.position_select import PositionSelect
from .character_node import CharacterNode


class CharacterAppearance(CharacterNode):
    icon = 'character_appearance.png'
    serialize_fields = CharacterNode.serialize_fields + [('position', CharacterPosition)]

    def __init__(self, node=None, parent=None):
        self._position = CharacterPosition.LEFT_BOTTOM
        super().__init__(node, parent)
        self.position = CharacterPosition.LEFT_BOTTOM

    @property
    def position(self):
        return self.position_edit.current_position()

    @position.setter
    def position(self, value):
        self._position = value
        if self._node is not None:
            self.position_edit.set_position(value)

    def init_sub_class_ui(self):
        self.layout.addWidget(QLabel('Position:'))
        self.position_edit = PositionSelect(self._position)
        self.layout.addWidget(self.position_edit)

        super().init_sub_class_ui()

    def on_change_position(self):
        position = self.position_edit.currentData(Qt.UserRole)
        self._position = position
