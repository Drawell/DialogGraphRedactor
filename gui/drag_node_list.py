from PyQt5.QtCore import QSize, Qt, QMimeData, QByteArray, QPoint
from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

from acts_system import Act
from gui.configs import LISTBOX_MIMETYPE


class DragNodeList(QListWidget):
    def __init__(self, act: Act, parent=None):
        super().__init__(parent)
        self.act = act
        self.init_ui()

    def init_ui(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.init_nodes()

    def init_nodes(self):
        for node_class in self.act.get_node_class_list():
            item = QListWidgetItem(node_class.get_name(), self)
            image = node_class.get_image()
            item.setIcon(QIcon(image))
            item.setSizeHint(QSize(32, 32))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

            item.setData(Qt.UserRole, image)
            item.setData(Qt.UserRole + 1, node_class.get_name())

    def startDrag(self, *args, **kwargs) -> None:
        try:
            item = self.currentItem()
            class_name = item.data(Qt.UserRole + 1)
            pixmap = item.data(Qt.UserRole)

            itemData = QByteArray()

            mimeData = QMimeData()
            mimeData.setText(class_name)
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            pass
