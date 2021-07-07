from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView


class QDMGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.gr_scene = scene
        self.init_ui()
        self.setScene(self.gr_scene)

        self.zoom_in_factor = 1.25
        self.zoom_clamp = True
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [0, 10]

    def init_ui(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing
                            | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_button_press(event)
        elif event.button() == Qt.LeftButton:
            self.left_mouse_button_press(event)
        elif event.button() == Qt.RightButton:
            self.right_mouse_button_press(event)
        else:
            super().mousePressEvent(event)

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
        return super().mousePressEvent(event)

    def left_mouse_button_release(self, event):
        return super().mouseReleaseEvent(event)

    def right_mouse_button_press(self, event):
        return super().mousePressEvent(event)

    def right_mouse_button_release(self, event):
        return super().mouseReleaseEvent(event)

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

