from gui import QDMGraphicsSocket
from .socket_type import SocketType as st
from .socket_position import SocketPosition as sp


class Socket:
    def __init__(self, node, index=0, position=sp.LEFT_TOP, socket_type=st.INPUT):
        self.node = node
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
        elif self.socket_type == st.INPUT:
            self.edge.end_socket = self

        self.edge.update_position()

    def disconnect(self):
        if self.edge is not None:
            if self.socket_type == st.OUTPUT:
                self.edge.start_socket = None
            else:
                self.edge.end_socket = None

        self.edge = None

    def has_edge(self):
        return self.edge is not None

    def remove_edges(self):
        if self.has_edge():
            self.edge.remove()
