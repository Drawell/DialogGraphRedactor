from act_nodes import *
from act_nodes.set_landscape import SetLandscape
from .character import Character
from utils import Serializable
from .character_change_listener import CharacterChangeListener


class Act(Serializable):
    serialize_fields = [('tale_name', str), ('act_id', int), ('characters', Character),
                        ('start_nodes', StartNode),
                        ('character_appearances', CharacterAppearance),
                        ('character_disappearances', CharacterDisappearance),
                        ('choices', Choice),
                        ('replicas', Replica),
                        ('set_landscapes', SetLandscape),
                        ('end_nodes', EndNode),
                        ]

    def __init__(self, scene=None, parent=None):
        super().__init__()
        self.scene = scene if scene is not None else parent
        self.tale_name = 'Undefined'
        self.act_id = 0

        self._teller = Character.teller_character()
        self._characters = [self._teller]
        self._characters_change_listeners = []  # type: List[CharacterChangeListener]

        self.start_nodes = []
        self.character_appearances = []
        self.character_disappearances = []
        self.choices = []
        self.replicas = []
        self.set_landscapes = []
        self.end_nodes = []
        self.serialized_event()

    @property
    def characters(self):
        return self._characters

    @characters.setter
    def characters(self, value):
        self._characters = value
        self.on_characters_count_change()

    def serialized_event(self):
        self.nodes = {StartNode.get_name(): self.start_nodes,
                      Replica.get_name(): self.replicas,
                      CharacterAppearance.get_name(): self.character_appearances,
                      CharacterDisappearance.get_name(): self.character_disappearances,
                      SetLandscape.get_name(): self.set_landscapes,
                      Choice.get_name(): self.choices,
                      EndNode.get_name(): self.end_nodes,
                      }

    def add_node(self, node):
        name = node.get_name()
        if name in self.nodes:
            self.nodes[name].append(node)

    def remove_node(self, node):
        name = node.get_name()
        if name in self.nodes:
            self.nodes[name].remove(node)

    def get_node_class_list(self):
        return [Replica, Choice, CharacterAppearance, CharacterDisappearance, SetLandscape, StartNode, EndNode]

    def get_changeable_characters(self):
        chars = list(filter(lambda char: char != Character.teller_character(), self._characters))
        return chars

    def add_character(self):
        self._characters.append(Character(self))
        self.on_characters_count_change()

    def remove_character(self, character):
        self._characters.remove(character)
        self.on_characters_count_change()

    def add_listener(self, listener: CharacterChangeListener):
        self._characters_change_listeners.append(listener)

    def remove_listener(self, listener: CharacterChangeListener):
        if listener in self._characters_change_listeners:
            self._characters_change_listeners.remove(listener)

    def on_characters_count_change(self):
        for listener in self._characters_change_listeners:
            listener.characters_list_change(self._characters)

    def on_character_info_change(self, character):
        for listener in self._characters_change_listeners:
            listener.character_info_change(character)

    def clear(self):
        self.characters = [self._teller]
