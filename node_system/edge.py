from gui import QDMGraphicsEdgeBezier
from utils import Serializable
from node_system.socket import Socket


class Edge(Serializable):
    serialize_fields = [('start_socket', Socket), ('end_socket', Socket)]

    def __init__(self, scene=None, start_socket=None, end_socket=None, parent=None):
        super().__init__()
        self.scene = scene if scene is not None else parent
        self.start_socket = start_socket  # type Socket
        self.end_socket = end_socket  # type Socket

        self.gr_edge = QDMGraphicsEdgeBezier(self)
        self.connect_sockets()

        self.update_position()
        self.scene.add_edge(self)

    def connect_sockets(self):
        if self.start_socket is not None:
            self.start_socket.connect_to_edge(self)
        if self.end_socket is not None:
            self.end_socket.connect_to_edge(self)

    def update_position(self):
        if self.start_socket is not None:
            self.gr_edge.set_source(*self.start_socket.get_socket_global_position())
        if self.end_socket is not None:
            self.gr_edge.set_destination(*self.end_socket.get_socket_global_position())
        self.gr_edge.update()

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.disconnect()
        if self.end_socket is not None:
            self.end_socket.disconnect()

    def remove(self):
        self.remove_from_sockets()
        self.scene.remove_edge(self)
        self.gr_edge = None

    def start_node(self):
        if self.start_socket:
            return self.start_socket.node
        return None

    def end_node(self):
        if self.end_socket:
            return self.end_socket.node
        return None

    def serialized_event(self):
        self.connect_sockets()

    def __str__(self):
        return f'Edge: {self.id} (Start {self.start_node()}, End {self.end_node()})'

