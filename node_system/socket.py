from gui import QDMGraphicsSocket
from utils import Serializable
from .socket_type import SocketType as st
from .socket_position import SocketPosition as sp


class Socket(Serializable):
    serialize_fields = [('index', int), ('position', sp), ('socket_type', st)]

    def __init__(self, node=None, index=0, position=sp.LEFT_TOP, socket_type=st.INPUT, parent=None):
        super().__init__()
        self.node = node if node is not None else parent
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.gr_socket = QDMGraphicsSocket(self, self.node.gr_node)
        self.gr_socket.set_on_position(index, position)

        self.edge = None

    def get_socket_global_position(self):
        return self.gr_socket.get_global_position()

    def connect_to_edge(self, edge):
        if self.edge is not None and self.edge != edge:
            self.edge.remove()

        self.edge = edge
        if self.socket_type == st.OUTPUT:
            self.edge.start_socket = self
            self.node.connect_output(self.edge)
        elif self.socket_type == st.INPUT:
            self.edge.end_socket = self
            self.node.connect_input(self.edge)

        self.edge.update_position()

    def disconnect(self):
        if self.edge is not None:
            if self.socket_type == st.OUTPUT:
                self.node.disconnect_output(self.edge)
                self.edge.start_socket = None
            else:
                self.node.disconnect_input(self.edge)
                self.edge.end_socket = None

        self.edge = None


    def has_edge(self):
        return self.edge is not None

    def remove_edges(self):
        if self.has_edge():
            self.edge.remove()

    def serialized_event(self):
        self.gr_socket.set_on_position(self.index, self.position)

    def remove(self):
        self.remove_edges()
        self.node.scene.gr_scene.removeItem(self.gr_socket)
        self.gr_socket = None

    def __str__(self):
        return f'Socket {self.socket_type}: {self.id}'
