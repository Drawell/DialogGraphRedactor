from gui import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier


class Edge:
    def __init__(self, scene, start_socket, end_socket):
        self.scene = scene
        self.start_socket = start_socket  # type Socket
        self.end_socket = end_socket  # type Socket

        if self.start_socket is not None:
            self.start_socket.connect_to_edge(self)
        if self.start_socket is not None:
            self.end_socket.connect_to_edge(self)

        self.gr_edge = QDMGraphicsEdgeBezier(self)

        self.update_position()
        self.scene.add_edge(self)

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
