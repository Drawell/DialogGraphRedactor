from act_nodes import *
from .character import Character
from utils import Serializable


class Act(Serializable):
    serialize_fields = [('tale_name', str), ('act_id', int), ('characters', Character), ('start_nodes', StartNode),
                        ('character_appearances', CharacterAppearance),
                        ('character_disappearances', CharacterDisappearance),
                        ('choices', Choice), ('replicas', Replica), ('end_nodes', EndNode),
                        ]

    def __init__(self, scene=None, parent=None):
        super().__init__()
        self.scene = scene if scene is not None else parent
        self.tale_name = 'Undefined'
        self.act_id = 0

        self.teller = Character.teller_character()
        self._characters = [self.teller]
        self._characters_change_listeners = []

        self.start_nodes = []
        self.character_appearances = []
        self.character_disappearances = []
        self.choices = []
        self.replicas = []
        self.end_nodes = []
        self.serialized_event()

    @property
    def characters(self):
        return self._characters

    @characters.setter
    def characters(self, value):
        self._characters = value
        self.on_characters_change()

    def serialized_event(self):
        self.nodes = {StartNode.get_name(): self.start_nodes,
                      Replica.get_name(): self.replicas,
                      CharacterAppearance.get_name(): self.character_appearances,
                      CharacterDisappearance.get_name(): self.character_disappearances,
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
        return [Replica, Choice, CharacterAppearance, CharacterDisappearance, StartNode, EndNode]

    def get_changeable_characters(self):
        chars = list(filter(lambda char: char != Character.teller_character(), self._characters))
        return chars

    def add_character(self):
        self._characters.append(Character(self))
        self.on_characters_change()

    def remove_character(self, character):
        self._characters.remove(character)
        self.on_characters_change()

    def on_characters_change(self):
        print('characters changed')
        for listener in self._characters_change_listeners:
            listener(self._characters)

    def clear(self):
        self.characters = [self.teller]

