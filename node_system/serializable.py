import inspect
from collections import OrderedDict
from enum import Enum


class Serializable:
    serialize_fields = []

    def __init__(self):
        self.id = id(self)

    def serialize(self, hash_map=None):
        if hash_map is None:
            hash_map = {}
        elif self.id in hash_map:
            return

        hash_map[self.id] = self.id

        self_as_list = [('id', self.id)]

        for ser_field, type_ in self.serialize_fields:
            # ser_field, rule, *dummy_none = tuple(ser_field.split(':') + [None])
            ser_fields = ser_field.split('.')

            if len(ser_fields) > 1:
                outer_attribute = getattr(self, ser_fields[0], None)
                attribute = getattr(outer_attribute, ser_fields[1], None)
            else:
                attribute = getattr(self, ser_field, None)

            if isinstance(attribute, list):
                self_as_list.append((ser_field, [Serializable._serialize_item(item, hash_map) for item in attribute]))
            else:
                self_as_list.append((ser_field, Serializable._serialize_item(attribute, hash_map)))

        return OrderedDict(self_as_list)

    @staticmethod
    def _serialize_item(attribute, hash_map):
        if isinstance(attribute, Serializable):
            if attribute.id in hash_map:
                return {'id': attribute.id}
            return attribute.serialize(hash_map)
        elif isinstance(attribute, Enum):
            return attribute.value
        elif hasattr(attribute, '__call__'):
            return attribute()
        elif attribute is not None:
            return attribute
        else:
            return None

    def _handle_rule(self, attribute, rule):
        if rule == 'e':
            return attribute.value

    def deserialize(self, data, hash_map=None):
        if hash_map is None:
            hash_map = {}
        self.id = data['id']
        hash_map[self.id] = self

        for ser_field, type_ in self.serialize_fields:
            if ser_field in data:
                attribute = getattr(self, ser_field, None)

                # if attribute is None:
                #    new_item = None
                if isinstance(attribute, list):
                    new_item = self._deserialize_list(type_, data[ser_field], hash_map)
                else:
                    new_item = self._deserialize_item(type_, data[ser_field], hash_map)

                if new_item is not None:
                    setattr(self, ser_field, new_item)

    def _deserialize_list(self, type_, data, hash_map):
        result = []
        for data_item in data:
            new_item = self._deserialize_item(type_, data_item, hash_map)
            result.append(new_item)

        return result

    def _deserialize_item(self, type_, data, hash_map):
        if issubclass(type_, Serializable):
            # constructor_params = Serializable._find_constructor_params(type_, hash_map)
            item_id = data['id']
            if item_id in hash_map:
                return hash_map[item_id]

            if 'parent' in inspect.signature(type_.__init__).parameters:
                new_item = type_(parent=self)
            else:
                new_item = type_()

            new_item.deserialize(data, hash_map)
            new_item.serialized_event()

        # elif issubclass(type_, Enum):
        #   pass
        else:
            new_item = type_(data)

        return new_item

    @staticmethod
    def _find_constructor_params(type_, hash_map):
        result = []
        signature = inspect.signature(type_.__init__)
        for param in signature.parameters:
            if param in hash_map:
                result.append(hash_map[param])

        return result

    def serialized_event(self):
        pass
