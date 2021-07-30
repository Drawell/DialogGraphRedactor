from gui.graphics_scene import QDMGraphicsScene


class Scene:
    def __init__(self):
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

    def set_editing_flag(self, is_editing: bool):
        self.gr_scene.views()[0].is_editing = is_editing
