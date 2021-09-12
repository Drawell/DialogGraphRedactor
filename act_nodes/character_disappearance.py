from .character_node import CharacterNode


class CharacterDisappearance(CharacterNode):
    icon = 'character_disappearance.png'

    def __init__(self, node=None, parent=None):
        super().__init__(node, parent)
