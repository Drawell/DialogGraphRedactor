from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPen, QColor, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self.edge = edge

        self._color = QColor('#EEEEEE')
        self._color_selected = QColor('#00ff00')
        self._pen = QPen(self._color)
        self._pen.setWidth(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidth(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.pos_source = [0, 0]
        self.pos_destination = [0, 0]

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and Qt.AltModifier & event.modifiers():
            self.edge.remove()

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calc_path()

    def calc_path(self):
        raise NotImplemented('Method is not overriden in a child')

    def update_path(self):
        self.setPath(self.calc_path())

    def paint(self, painter, option, widget=...) -> None:
        self.update_path()
        painter.setPen(self._pen_selected if self.isSelected() else self._pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.lineTo(self.pos_destination[0], self.pos_destination[1])
        return path


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def calc_path(self):
        dist = (self.pos_destination[0] - self.pos_source[0]) * 0.5
        if self.pos_source[0] > self.pos_destination[0]:
            dist *= -1

        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.cubicTo(self.pos_source[0] + dist, self.pos_source[1], self.pos_destination[0] - dist,
                     self.pos_destination[1], self.pos_destination[0], self.pos_destination[1])
        return path
