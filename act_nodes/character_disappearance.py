from .act_node_widget import ActNodeWidget
from .character_node import CharacterNode


class CharacterDisappearance(CharacterNode):
    def __init__(self, node=None, parent=None):
        super().__init__(node, parent)

    @staticmethod
    def get_name():
        return 'CharacterDisappearance'

    def init_ui(self):
        super().init_ui()
        self.layout.addStretch()

    @staticmethod
    def get_image():
        return ActNodeWidget.load_from_icons('character_disappearance.png')
