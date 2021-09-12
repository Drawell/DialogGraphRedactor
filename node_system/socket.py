from gui import QDMGraphicsSocket
from utils import Serializable
from .socket_type import SocketType as st
from .socket_position import SocketPosition as sp


class Socket(Serializable):
    # serialize_fields = [('index', int), ('position', sp), ('socket_type', st)]

    def __init__(self, node=None, index=0, position=sp.LEFT_TOP, socket_type=st.INPUT, parent=None):
        super().__init__()
        self.node = node if node is not None else parent
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.gr_socket = QDMGraphicsSocket(self, self.node.gr_node)
        self.gr_socket.set_on_position(index, position)

    def get_socket_global_position(self):
        return self.gr_socket.get_global_position()

    def connect_to_edge(self, edge):
        raise NotImplemented('Function has_edge need to implement')

    def disconnect(self):
        raise NotImplemented('Function has_edge need to implement')

    def has_edge(self):
        raise NotImplemented('Function has_edge need to implement')

    def remove_edges(self):
        raise NotImplemented('Function has_edge need to implement')
        # if self.has_edge():
        #   self.edge.remove()

    def remove(self):
        self.remove_edges()
        self.node.scene.gr_scene.removeItem(self.gr_socket)
        self.gr_socket = None

    def serialized_event(self):
        self.gr_socket.set_on_position(self.index, self.position)

    def __str__(self):
        return f'Socket {self.socket_type}: {self.id}'


class InputSocket(Socket):
    serialize_fields = [('index', int), ('position', sp)]

    def __init__(self, node=None, index=0, position=sp.LEFT_TOP, parent=None):
        super().__init__(node, index, position, st.INPUT, parent)
        self._edges = []

    @property
    def edge(self):
        if len(self.edges) > 0:
            return self.edges[len(self.edges) - 1]
        return None

    @property
    def edges(self):
        return self._edges

    def has_edge(self):
        return len(self.edges) > 0

    def connect_to_edge(self, edge):
        self.edges.append(edge)
        self.edge.end_socket = self
        self.node.connect_input(self.edge)
        self.edge.update_position()

    def disconnect(self):
        if self.has_edge():
            edge = self.edge
            if edge is not None:
                self.node.disconnect_input(self.edge)
                edge.end_socket = None
                self.edges.remove(edge)

    def remove_edges(self):
        edges = self._edges.copy()
        for edge in edges:
            edge.remove()


class OutputSocket(Socket):
    serialize_fields = [('index', int), ('position', sp)]

    def __init__(self, node=None, index=0, position=sp.LEFT_TOP, parent=None):
        super().__init__(node, index, position, st.OUTPUT, parent)
        self._edge = None

    @property
    def edge(self):
        return self._edge

    @property
    def edges(self):
        return [self._edge]

    def has_edge(self):
        return self._edge is not None

    def connect_to_edge(self, edge):
        if self._edge is not None and self._edge != edge:
            self._edge.remove()

        self._edge = edge
        if self.socket_type == st.OUTPUT:
            self.edge.start_socket = self
            self.node.connect_output(self.edge)

        self._edge.update_position()

    def disconnect(self):
        if self._edge is not None:
            self.node.disconnect_output(self.edge)
            self._edge.start_socket = None

        self._edge = None

    def remove_edges(self):
        if self.has_edge():
            self._edge.remove()
