import json

from PyQt5.QtCore import QPoint

from acts_system import Act
from gui.graphics_scene import QDMGraphicsScene
from node_system.edge import Edge
from node_system.node import Node
from utils import Serializable


class Scene(Serializable):
    serialize_fields = [('act', Act), ('scene_width', float), ('scene_height', float), ('nodes', Node), ('edges', Edge)]

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.act = Act(self)

        self.scene_width, self.scene_height = 64000, 64000
        self.setup_ui()

    def setup_ui(self):
        self.gr_scene = QDMGraphicsScene(self)
        self.gr_scene.set_scene(self.scene_width, self.scene_height)

    def add_drag_enter_listener(self, callback):
        self.get_view().add_drag_enter_listener(callback)

    def add_drop_listener(self, callback):
        self.get_view().add_drop_listener(callback)

    def add_node(self, node):
        self.nodes.append(node)
        self.gr_scene.addItem(node.gr_node)

    def remove_node(self, node):
        self.act.remove_node(node.content_widget)
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
        self.act.clear()
        while len(self.nodes) > 0:
            self.nodes[0].remove()

    def set_editing_flag(self, is_editing: bool):
        self.get_view().is_editing = is_editing

    def mouse_pos_to_view_pos(self, x, y):
        return self.get_view().mapToScene(QPoint(x, y))

    def get_item_at(self, position):
        return self.get_view().itemAt(position)

    def get_view(self):
        return self.gr_scene.views()[0]

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf8') as file:
            file.write(json.dumps(self.serialize(), indent=4, ensure_ascii=False))

    def export_act_to_file(self, filename):
        with open(filename, 'w', encoding='utf8') as file:
            file.write(json.dumps(self.act.serialize(to_upper=True), indent=4, ensure_ascii=False))

    def load_from_file(self, filename):
        self.clear()

        with open(filename, 'r', encoding='utf8') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)
            pass
