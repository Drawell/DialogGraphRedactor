from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtWidgets import QComboBox

from acts_system.character_position import CharacterPosition


class PositionSelect(QComboBox):
    def __init__(self, position=CharacterPosition.LEFT_BOTTOM, parent=None):
        super().__init__(parent)
        for position_ in CharacterPosition:
            variant = QVariant(position_)
            self.addItem(str(position_), variant)

        self.set_position(position)

    def set_position(self, position):
        for idx in range(self.count()):
            position_ = self.itemData(idx, Qt.UserRole)
            if position_ == position:
                self.setCurrentIndex(idx)
                break

    def current_position(self):
        return self.currentData(Qt.UserRole)
