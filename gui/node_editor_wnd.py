from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsItem, QPushButton, QTextEdit
from gui.graphics_view import QDMGraphicsView
from node.node import Node
from node.scene import Scene


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Dialog Graph Redactor")

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # create graphics scene
        self.scene = Scene()

        node = Node(self.scene, 'My node')

        # create graphics view
        self.view = QDMGraphicsView(self.scene.gr_scene, self)
        self.layout().addWidget(self.view)

        self.show()

        #self.add_debug_content()

    def add_debug_content(self):
        green_brush = QBrush(Qt.green)
        outline_pen = QPen(Qt.black)
        outline_pen.setWidth(2)

        rect = self.gr_scene.addRect(-100, -100, 80, 100, outline_pen, green_brush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.gr_scene.addText('This is text', QFont('Ubuntu'))
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton('Hello world')
        proxy1 = self.gr_scene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.gr_scene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsMovable)
        proxy2.setPos(0, 60)

        line = self.gr_scene.addLine(0, 0, 100, 200, outline_pen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)