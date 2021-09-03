from enum import Enum

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QApplication

from . import QDMGraphicsNode
from .graphics_edge import QDMGraphicsEdge
from .graphics_socket import QDMGraphicsSocket
from state_machine.state_machine import StateMachine, ActionResult


class Mode(Enum):
    NONE = 1
    DRAG_EDGE_TO_INPUT = 2
    DRAG_EDGE_TO_OUTPUT = 3


class QDMGraphicsView(QGraphicsView):
    def __init__(self, ge_scene, state_machine: StateMachine, parent=None):
        super().__init__(parent)
        self.gr_scene = ge_scene
        self.init_ui()
        self.setScene(self.gr_scene)

        self.zoom_in_factor = 1.25
        self.zoom_clamp = True
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [0, 10]
        self.state_machine = state_machine
        self.mode = Mode.NONE

        self.is_editing = False

        self._drag_enter_listeners = []
        self._drop_listeners = []

    def init_ui(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing
                            | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event) -> None:
        for callback in self._drag_enter_listeners:
            callback(event)

    def dropEvent(self, event) -> None:
        for callback in self._drop_listeners:
            callback(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_button_press(event)
        elif event.button() == Qt.LeftButton:
            self.left_mouse_button_press(event)
        elif event.button() == Qt.RightButton:
            self.right_mouse_button_press(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        pos = self.mapToScene(event.pos())
        self.state_machine.on_mouse_move(pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_button_release(event)
        elif event.button() == Qt.LeftButton:
            self.left_mouse_button_release(event)
        elif event.button() == Qt.RightButton:
            self.right_mouse_button_release(event)
        else:
            super().mouseReleaseEvent(event)

    def middle_mouse_button_press(self, event):
        release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                    Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fake_event)

    def middle_mouse_button_release(self, event):
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fake_event)
        self.setDragMode(QGraphicsView.NoDrag)

    def left_mouse_button_press(self, event):
        item = self.get_item_at_click(event)
        if self.state_machine.on_mouse_left_press(item) == ActionResult.CONTINUE_PARENT_ACTION:
            super().mousePressEvent(event)

    def left_mouse_button_release(self, event):
        item = self.get_item_at_click(event)
        if self.state_machine.on_mouse_left_release(item) == ActionResult.CONTINUE_PARENT_ACTION:
            super().mouseReleaseEvent(event)

    def right_mouse_button_press(self, event):
        super().mousePressEvent(event)

    def right_mouse_button_release(self, event):
        super().mouseReleaseEvent(event)

    def get_item_at_click(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def wheelEvent(self, event) -> None:
        # calculate zoom factor
        zoom_out_factor = 1 / self.zoom_in_factor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step

        clamped = False
        if self.zoom < self.zoom_range[0]:
            self.zoom = self.zoom_range[0]
            clamped = True
        elif self.zoom > self.zoom_range[1]:
            self.zoom = self.zoom_range[1]
            clamped = True

        # set scene scale
        if not clamped or self.zoom_clamp is False:
            self.scale(zoom_factor, zoom_factor)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Delete and not self.is_editing:
            self.delete_selected()
        elif event.key() == Qt.Key_Alt:
            QApplication.setOverrideCursor(Qt.CrossCursor)
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event) -> None:
        if event.key() == Qt.Key_Alt:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        else:
            super().keyReleaseEvent(event)

    def delete_selected(self):
        for item in self.gr_scene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif isinstance(item, QDMGraphicsNode):
                item.node.remove()

    def add_drag_enter_listener(self, callback):
        self._drag_enter_listeners.append(callback)

    def add_drop_listener(self, callback):
        self._drop_listeners.append(callback)
