from enum import Enum

from gui import QDMGraphicsSocket
from node_system.socket import Socket
from node_system.socket_type import SocketType as st
from node_system.edge import Edge


class State(Enum):
    NONE = 0,
    EDGE_DRAG_TO_INPUT = 1,
    EDGE_DRAG_TO_OUTPUT = 2,


class ActionResult(Enum):
    INTERRUPT_PARENT_ACTION = 0,
    CONTINUE_PARENT_ACTION = 1


class StateMachine:
    def __init__(self, scene):
        self.scene = scene
        self.state = State.NONE
        self.dragging_edge = None  # type Edge

    def is_dragging_to_input(self):
        return self.state == State.EDGE_DRAG_TO_INPUT

    def is_dragging_to_output(self):
        return self.state == State.EDGE_DRAG_TO_OUTPUT

    def on_mouse_left_press(self, item) -> ActionResult:
        if type(item) == QDMGraphicsSocket:
            socket = item.socket  # type Socket

            if self.state == self.state.NONE:
                if socket.has_edge():
                    self._handle_moving_edge(socket)
                else:
                    self._handle_creating_edge(socket)

                return ActionResult.INTERRUPT_PARENT_ACTION

        return ActionResult.CONTINUE_PARENT_ACTION

    def on_mouse_left_release(self, item) -> ActionResult:
        if self.state in [State.EDGE_DRAG_TO_OUTPUT, State.EDGE_DRAG_TO_INPUT]:
            socket = None
            if type(item) is QDMGraphicsSocket:
                socket = item.socket  # type: Socket
            elif issubclass(type(item), Socket):
                socket = item

            if socket is not None:
                if socket.socket_type == st.INPUT and self.state == State.EDGE_DRAG_TO_INPUT \
                        or socket.socket_type == st.OUTPUT and self.state == State.EDGE_DRAG_TO_OUTPUT:
                    socket.connect_to_edge(self.dragging_edge)
                    self.state = State.NONE
                    self.dragging_edge = None
                    return ActionResult.INTERRUPT_PARENT_ACTION

            self.dragging_edge.remove()
            self.dragging_edge = None
            self.state = State.NONE
        return ActionResult.CONTINUE_PARENT_ACTION

    def on_mouse_right_press(self, item) -> ActionResult:
        pass

    def on_mouse_right_release(self, item) -> ActionResult:
        pass

    def on_mouse_move(self, pos):
        if self.state in [State.EDGE_DRAG_TO_OUTPUT, State.EDGE_DRAG_TO_INPUT]:
            if self.state == State.EDGE_DRAG_TO_INPUT:
                self.dragging_edge.gr_edge.set_destination(pos.x(), pos.y())
            if self.state == State.EDGE_DRAG_TO_OUTPUT:
                self.dragging_edge.gr_edge.set_source(pos.x(), pos.y())

            self.dragging_edge.gr_edge.update()

    def _handle_moving_edge(self, socket):
        self.dragging_edge = socket.edge
        x, y = tuple(socket.get_socket_global_position())
        socket.disconnect()

        if socket.socket_type == st.INPUT:
            self.state = State.EDGE_DRAG_TO_INPUT
            self.dragging_edge.gr_edge.set_destination(x, y)
        else:
            self.dragging_edge.gr_edge.set_source(x, y)
            self.state = State.EDGE_DRAG_TO_OUTPUT

    def _handle_creating_edge(self, socket):
        self.dragging_edge = Edge(self.scene, None, None)
        x, y = tuple(socket.get_socket_global_position())
        if socket.socket_type == st.OUTPUT:
            self.state = State.EDGE_DRAG_TO_INPUT
            self.dragging_edge.gr_edge.set_destination(x, y)
        else:
            self.dragging_edge.gr_edge.set_source(x, y)
            self.state = State.EDGE_DRAG_TO_OUTPUT

        socket.connect_to_edge(self.dragging_edge)
