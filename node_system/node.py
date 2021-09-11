from gui import QDMGraphicsNode
from utils import Serializable
from .edge import Edge
from .socket import InputSocket, OutputSocket
from .socket_position import SocketPosition as sp
from .socket_type import SocketType as st


class Node(Serializable):
    serialize_fields = [('scene.id', int), ('x', float), ('y', float),
                        ('inputs', InputSocket), ('outputs', OutputSocket), ('content_widget', Serializable)]

    def __init__(self, scene=None, parent=None):
        super().__init__()
        self.scene = scene if scene is not None else parent
        self.act = self.scene.act

        self._content_widget = None
        self.gr_node = QDMGraphicsNode(self)

        self.scene.add_node(self)

        self.inputs = []
        self.outputs = []

        # socket = Socket(self, 0, sp.LEFT_TOP, st.INPUT)
        # self.inputs.append(socket)

        # for idx in range(outputs_count):
        #    socket = Socket(self, idx, sp.RIGHT_TOP, st.OUTPUT)
        #    self.outputs.append(socket)

    @property
    def content_widget(self):
        return self._content_widget

    @content_widget.setter
    def content_widget(self, value):
        self._content_widget = value
        if self._content_widget is not None:
            self._content_widget.node = self
            self.gr_node.title = self._content_widget.get_name()
            self.gr_node.update_content()

    @property
    def position(self):
        return self.gr_node.pos()

    @property
    def x(self):
        return self.gr_node.x()

    @x.setter
    def x(self, value):
        self.gr_node.setX(value)

    @property
    def y(self):
        return self.gr_node.y()

    @y.setter
    def y(self, value):
        self.gr_node.setY(value)

    @property
    def input(self):
        return self.inputs[0] if len(self.inputs) > 0 else None

    def set_pos(self, x, y):
        self.gr_node.setPos(x, y)

    def update_connected_edges(self):
        for socket in self.inputs + self.outputs:
            if socket.has_edge():
                for edge in socket.edges:
                    edge.update_position()

    def remove(self):
        for socket in self.inputs + self.outputs:
            socket.remove_edges()
        self.scene.remove_node(self)
        self.gr_node = None

    def set_inputs_count(self, count):
        if len(self.inputs) < count:
            for _ in range(count - len(self.inputs)):
                socket = InputSocket(self, len(self.inputs), sp.LEFT_TOP, st.INPUT)
                self.inputs.append(socket)

    def set_outputs_count(self, count):
        if len(self.outputs) < count:
            for _ in range(count - len(self.outputs)):
                socket = OutputSocket(self, len(self.outputs), sp.RIGHT_TOP, st.OUTPUT)
                self.outputs.append(socket)

    def remove_output(self, idx=-1):
        pass

    def connect_input(self, edge: Edge):
        if edge.start_node() is not None:
            edge.start_node().connect_output(edge)

    def connect_output(self, edge: Edge):
        if edge.end_node() is not None:
            self.content_widget.add_next_node(edge.end_node().content_widget)

    def disconnect_input(self, edge):
        if edge.start_node() is not None:
            edge.start_node().disconnect_output(edge)

    def disconnect_output(self, edge):
        if edge.end_node() is not None:
            self.content_widget.remove_next_node(edge.end_node().content_widget)

    def __str__(self):
        return f'Node: {self.id}, ({str(self.content_widget)})'
