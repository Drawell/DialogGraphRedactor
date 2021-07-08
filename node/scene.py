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
        self.nodes.remove(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)
