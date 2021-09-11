from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

from acts_system import Character


class CharacterWidget(QWidget):

    def __init__(self, character: Character, parent=None):
        super().__init__(parent)
        self.character = character
        self.init_ui()
        self.id_edit.setText(character.char_id)
        self.name_edit.setText(character.name)
        self.connect_events()

    def init_ui(self):
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.id_edit = QLineEdit('', self)
        self.name_edit = QLineEdit('', self)
        self.delete_button = QPushButton('x', self)
        self.delete_button.setMaximumSize(32, 32)
        layout.addWidget(self.id_edit)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(5, 0, 5, 0)

    def connect_events(self):
        self.id_edit.textChanged.connect(self.on_id_change)
        self.name_edit.textChanged.connect(self.on_name_change)
        self.delete_button.clicked.connect(self.on_delete)

    def on_id_change(self):
        self.character.char_id = self.id_edit.text()

    def on_name_change(self):
        self.character.name = self.name_edit.text()

    def on_delete(self):
        self.character.remove()
