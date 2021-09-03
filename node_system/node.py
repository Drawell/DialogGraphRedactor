from gui import QDMGraphicsNode, ActNodeWidget
from utils import Serializable
from .socket import Socket
from .socket_position import SocketPosition as sp
from .socket_type import SocketType as st


class Node(Serializable):
    serialize_fields = [('content_widget', Serializable), ('scene.id', int), ('x', float), ('y', float),
                        ('inputs', Socket),
                        ('outputs', Socket)]

    def __init__(self, scene=None, outputs_count=1, parent=None):
        super().__init__()
        self.scene = scene if scene is not None else parent
        self.act = self.scene.act

        self._content_widget = None  # type: ActNodeWidget
        self.gr_node = QDMGraphicsNode(self)

        self.scene.add_node(self)

        self.inputs = []
        self.outputs = []

        socket = Socket(self, 0, sp.LEFT_TOP, st.INPUT)
        self.inputs.append(socket)

        for idx in range(outputs_count):
            socket = Socket(self, idx, sp.RIGHT_TOP, st.OUTPUT)
            self.outputs.append(socket)

    @property
    def content_widget(self) -> ActNodeWidget:
        return self._content_widget

    @content_widget.setter
    def content_widget(self, value: ActNodeWidget):
        self._content_widget = value
        if self._content_widget is not None:
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

    #def serialized_event(self):
    #    self.gr_node.title = self.title
