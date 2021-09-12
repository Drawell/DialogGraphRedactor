from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainterPath, QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem

from sub_widgets import QDMDeleteButton


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node

        # init our flags
        self.hovered = False
        self._was_moved = False
        self._last_selected_state = False

        self.init_sizes()
        self.init_assets()
        self.init_sockets()
        self.setup_ui()

    @property
    def content(self):
        return self.node.content_widget if self.node else None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) > 17:
            pos = [i for i, e in enumerate(value + 'A') if e.isupper()]
            parts = [value[pos[j]:pos[j + 1]] for j in range(len(pos) - 1)]
            value = '\n'.join(parts)
            self.title_height += 20

        self._title = value
        self.title_item.setPlainText(self.title)

    def setup_ui(self):
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.init_title()
        self.update_content()

    def init_title(self):
        self.icon = QGraphicsPixmapItem(self)
        self.icon.setPos(5, 2)

        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(32, 0)

        delete_button_ = QDMDeleteButton()
        delete_button_.clicked.connect(self.node.remove)
        self.delete_button = self.node.scene.gr_scene.addWidget(delete_button_)
        self.delete_button.setParentItem(self)
        self.delete_button.setGeometry(QRectF(self.width - 25, 0, 25, 25))

    def init_sizes(self):
        self.width = 210
        self.height = 260
        self.edge_roundness = 10.0
        self.edge_padding = 10.0
        self.title_height = 24.0
        self.title_horizontal_padding = 4.0
        self.title_vertical_padding = 4.0

    def init_assets(self):
        self._title_color = Qt.white
        self._title_font = QFont("Consolas", 10)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#FFFFA637")
        self._color_hovered = QColor('#FFFFA637')
        #self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

    def update_content(self):
        if self.content is not None:
            self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding,
                                     self.width - 2 * self.edge_padding,
                                     self.height - 2 * self.edge_padding - self.title_height)

            img = self.content.get_image().scaled(23, 23)
            self.icon.setPixmap(img)
            self.gr_content = self.node.scene.gr_scene.addWidget(self.content)
            self.gr_content.node = self.node
            self.gr_content.setParentItem(self)

    def init_sockets(self):
        pass

    #def on_selected(self):
    #    self.node_system.scene.grScene.itemSelected.emit()

    #def do_select(self, new_state=True):
    #    self.setSelected(new_state)
    #    self._last_selected_state = new_state
    #    if new_state: self.on_selected()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.node.update_connected_edges()

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.gr_node.isSelected():
                node.update_connected_edges()
        #self._was_moved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        return
        # handle when grNode moved
        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

            self.node.scene.resetLastSelectedStates()
            self.do_select()  # also trigger itemSelected when node_system was moved

            # we need to store the last selected state, because moving does also select the nodes
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

            # now we want to skip storing selection
            return

        # handle when grNode was clicked on
        if self._last_selected_state != self.isSelected() or self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.on_selected()

    def mouseDoubleClickEvent(self, event):
        pass
        #self.node.onDoubleClicked(event)

    def hoverEnterEvent(self, event) -> None:
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event) -> None:
        self.hovered = False
        self.update()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and Qt.AltModifier & event.modifiers():
            self.node.remove()

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height).normalized()

    def paint(self, painter, option, widget=None) -> None:
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness,
                           self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness,
                             self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(-1, -1, self.width + 2, self.height + 2, self.edge_roundness, self.edge_roundness)
        painter.setBrush(Qt.NoBrush)

        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())
