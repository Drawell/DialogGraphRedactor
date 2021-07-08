from gui.graphics_node import QDMGraphicsNode


class Node:
    def __init__(self, scene, title='Undefined'):
        self.scene = scene
        self.title = title
        self.content = None

        self.gr_node = QDMGraphicsNode(self)

        self.scene.add_node(self)



