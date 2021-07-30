from gui import QDMGraphicsNode, QDMNodeContentWidget
from .socket import Socket
from .socket_position import SocketPosition as sp
from .socket_type import SocketType as st


class Node:
    def __init__(self, scene, title='Undefined', inputs=[], outputs=[]):
        self.scene = scene
        self.title = title

        self.content_widget = QDMNodeContentWidget(self)
        self.gr_node = QDMGraphicsNode(self)

        self.scene.add_node(self)

        self.inputs = []
        self.outputs = []

        for idx, item in enumerate(inputs):
            socket = Socket(self, idx, sp.LEFT_TOP, st.INPUT)
            self.inputs.append(socket)

        for idx, item in enumerate(outputs):
            socket = Socket(self, idx, sp.RIGHT_TOP, st.OUTPUT)
            self.outputs.append(socket)

    @property
    def position(self):
        return self.gr_node.pos()

    def set_pos(self, x, y):
        self.gr_node.setPos(x, y)

    def update_connected_edges(self):
        for socket in self.inputs + self.outputs:
            if socket.has_edge():
                socket.edge.update_position()

    def remove(self):
        for socket in self.inputs + self.outputs:
            socket.remove_edges()
        self.scene.remove_node(self)
        self.gr_node = None
