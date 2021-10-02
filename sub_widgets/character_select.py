from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtWidgets import QComboBox

from acts_system import Character
from acts_system.character_change_listener import CharacterChangeListener


class CharacterSelect(QComboBox, CharacterChangeListener):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.act = None
        self._current_character_id = Character.teller_character().char_id

    def set_act(self, act):
        self.act = act
        act.add_listener(self)
        self.characters_list_change(self.act.characters)

    def set_characters(self, characters):
        self.clear()
        for character in characters:
            self.add_item(character)

    def add_item(self, character: Character):
        character_data = QVariant(character)
        self.addItem(character.name, character_data)

    def set_current_character_id(self, char_id: str):
        self._current_character_id = char_id
        for idx in range(self.count()):
            character = self.itemData(idx, Qt.UserRole)
            if character.char_id == char_id:
                self.setCurrentIndex(idx)
                break

    def current_character_id(self):
        character = self.currentData(Qt.UserRole)
        return character.char_id

    def characters_list_change(self, new_characters):
        character = self.currentData(Qt.UserRole)
        current_id = character.id if character is not None else None
        self.set_characters(new_characters)

        for idx in range(self.count()):
            character = self.itemData(idx, Qt.UserRole)
            if character.id == current_id or character.char_id == self._current_character_id:
                self.setCurrentIndex(idx)
                return

        self.setCurrentIndex(0)

    def character_info_change(self, new_character):
        for idx in range(self.count()):
            character = self.itemData(idx, Qt.UserRole)
            if character.id == new_character.id:
                self.setItemData(idx, QVariant(new_character))
                self.setItemText(idx, new_character.name)
                break

    def remove(self):
        if self.act is not None:
            self.act.remove_listener(self)
