from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QBrush, QPen, QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsItem, QPushButton, QTextEdit, QApplication
from gui import QDMGraphicsView
from node_system.node import Node
from node_system.scene import Scene
from state_machine.state_machine import StateMachine


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = 'qss/node_style.qss'
        self.load_stylesheet(self.stylesheet_filename)
        self.init_ui()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # create graphics scene
        self.scene = Scene()
        self.state_machine = StateMachine(self.scene)

        self.add_nodes()

        # create graphics view
        self.view = QDMGraphicsView(self.scene.gr_scene, self.state_machine, self)
        self.layout().addWidget(self.view)

        # self.add_debug_content()

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

    def add_nodes(self):
        node1 = Node(self.scene, 'My node_system 1', inputs=[1, 2, 3], outputs=[1])
        node2 = Node(self.scene, 'My node_system 2', inputs=[1, 2, 3], outputs=[1])
        node3 = Node(self.scene, 'My node_system 3', inputs=[1, 2, 3], outputs=[1])

        node1.set_pos(-350, -250)
        node2.set_pos(-50, 0)
        node3.set_pos(150, -200)

        # edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[1])
        # edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[2])

    def load_stylesheet(self, stylesheet_filename):
        file = QFile(stylesheet_filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def load_scene_form_file(self, file_name):
        self.scene.load_from_file(file_name)

    def save_scene_to_file(self, file_name):
        self.scene.save_to_file(file_name)

    def create_new_scene(self):
        self.scene.clear()