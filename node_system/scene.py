import json
from gui.graphics_scene import QDMGraphicsScene
from node_system.edge import Edge
from node_system.node import Node
from node_system.serializable import Serializable


class Scene(Serializable):
    serialize_fields = [('scene_width', float), ('scene_height', float), ('nodes', Node), ('edges', Edge)]

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width, self.scene_height = 64000, 64000
        self.setup_ui()

    def setup_ui(self):
        self.gr_scene = QDMGraphicsScene(self)
        self.gr_scene.set_scene(self.scene_width, self.scene_height)

    def add_node(self, node):
        self.nodes.append(node)
        self.gr_scene.addItem(node.gr_node)

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.gr_scene.removeItem(node.gr_node)

    def add_edge(self, edge):
        self.edges.append(edge)
        self.gr_scene.addItem(edge.gr_edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            self.gr_scene.removeItem(edge.gr_edge)

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

    def set_editing_flag(self, is_editing: bool):
        self.gr_scene.views()[0].is_editing = is_editing

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))

    def load_from_file(self, filename):
        self.clear()

        with open(filename, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)
            pass



    '''def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
        ])'''
    '''
    def deserialize(self, data, hash_map={}):
        self.clear()
        hash_map = {}

        for node_data in data['nodes']:
            pass


        print('deserialize')
        pass
    '''
