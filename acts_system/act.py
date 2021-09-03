from act_nodes.replica import Replica
from utils import Serializable


class Act(Serializable):
    serialize_fields = [('replicas', Replica)]

    def __init__(self, scene=None, parent=None):
        super().__init__()
        self.scene = scene if scene is not None else parent
        self.replicas = []

    def add_node(self, node):
        name = node.get_name()
        if name == Replica.get_name():
            self.replicas.append(node)

    def remove_node(self, node):
        name = node.get_name()
        if name == Replica.get_name():
            self.replicas.remove(node)

    def clear(self):
        pass

    def get_node_class_list(self):
        return [Replica]
