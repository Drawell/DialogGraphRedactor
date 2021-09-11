from utils import Serializable


class Character(Serializable):
    _teller_char = None
    serialize_fields = [('char_id', str), ('name', str)]

    def __init__(self, act=None, parent=None):
        super().__init__()
        self.act = act if act is not None else parent
        self._char_id = ''
        self._name = ''

    @property
    def char_id(self):
        return self._char_id

    @char_id.setter
    def char_id(self, value):
        self._char_id = value
        if self.act:
            self.act.on_characters_change()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self.act:
            self.act.on_characters_change()

    def remove(self):
        if self.act:
            self.act.remove_character(self)

    @staticmethod
    def teller_character():
        _teller_char = Character()
        _teller_char.id = 0
        _teller_char.char_id = 'teller'
        _teller_char.name = 'Teller'

        return _teller_char

    def __str__(self):
        return f'Char: {self.id}, {self._char_id}'

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id
