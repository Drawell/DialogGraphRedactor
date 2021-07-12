from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsItem

from gui import QDMGraphicsNode


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, parent: QDMGraphicsNode = None):
        super().__init__(parent)
        self.socket = socket
        self.gr_node = parent

        self.radius = 6.0
        self.outline_width = 1.0
        self.socket_spacing = 22
        self._color_background = QColor('#FFFF7700')
        self._color_outline = QColor('#FF000000')

        self._pen = QPen(self._color_outline)
        self._pen.setWidth(self.outline_width)
        self._brush = QBrush(self._color_background)

    def set_on_position(self, index, is_left_position, is_top_position):
        x = 0 if is_left_position else self.gr_node.width
        if is_top_position:
            y = index * self.socket_spacing + self.gr_node.title_height + self.gr_node.edge_padding
        else:
            y = - index * self.socket_spacing + self.gr_node.height - self.gr_node.edge_padding
        self.setPos(x, y)

    def get_global_position(self):
        return [self.x() + self.gr_node.x(), self.y() + self.gr_node.y()]

    def boundingRect(self) -> QRectF:
        return QRectF(-self.radius - self.outline_width, -self.radius - self.outline_width,
                      2 * (self.radius + self.outline_width), 2 * (self.radius + self.outline_width)).normalized()

    def paint(self, painter, option, widget=None) -> None:
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
