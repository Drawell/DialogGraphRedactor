from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea

from .charcter_widget import CharacterWidget
from sub_widgets import ProxyWidget


class DragCharactersList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._act = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.chars_layout = QVBoxLayout()
        self.chars_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumSize(200, 200)

        proxy_widget = ProxyWidget(self.chars_layout, self)
        scroll_area.setWidget(proxy_widget)
        main_layout.addWidget(scroll_area)

        add_new_button = QPushButton('Add New Character', self)
        add_new_button.clicked.connect(self.on_add_new)
        main_layout.addWidget(add_new_button)

        self.setLayout(main_layout)

    def set_act(self, act):
        self._act = act
        self.clear()
        self.init_items()

    def clear(self):
        for i in reversed(range(self.chars_layout.count())):
            if self.chars_layout.itemAt(i).widget():
                self.chars_layout.itemAt(i).widget().setParent(None)
            else:
                item = self.chars_layout.takeAt(i)
                self.chars_layout.removeItem(item)

        self.update()

    def init_items(self):
        for character in self._act.get_changeable_characters():
            item = CharacterWidget(character, self, self.on_delete)
            self.chars_layout.addWidget(item)

        self.chars_layout.addStretch()

    def on_delete(self, character_widget):
        for i in reversed(range(self.chars_layout.count())):
            widget = self.chars_layout.itemAt(i).widget()
            if widget and type(widget) == CharacterWidget and widget == character_widget:
                self.chars_layout.itemAt(i).widget().setParent(None)

    def on_add_new(self):
        self._act.add_character()
        self.clear()
        self.init_items()
