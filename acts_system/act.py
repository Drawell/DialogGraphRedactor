from act_nodes.replica import Replica
from act_nodes.start_node import StartNode
from utils import Serializable


class Act(Serializable):
    serialize_fields = [('start_nodes', StartNode), ('replicas', Replica)]

    def __init__(self, scene=None, parent=None):
        super().__init__()
        self.scene = scene if scene is not None else parent
        self.tale_name = 'Undefined'
        self.act_id = 0
        self.characters = []
        self.start_nodes = []
        self.character_appearances = []
        self.choice_nodes = []
        self.replicas = []
        self.end_nodes = []
        self.serialized_event()
        #self.clear()


    def serialized_event(self):
        self.nodes = {StartNode.get_name(): self.start_nodes,
                      Replica.get_name(): self.replicas,
                      }

    def add_node(self, node):
        name = node.get_name()
        if name in self.nodes:
            self.nodes[name].append(node)

    def remove_node(self, node):
        name = node.get_name()
        if name == Replica.get_name():
            self.replicas.remove(node)

    def get_node_class_list(self):
        return [Replica, StartNode]

    def clear(self):
        pass