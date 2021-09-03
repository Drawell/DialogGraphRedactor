from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QBrush, QPen, QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsItem, QPushButton, QTextEdit, QApplication

from acts_system.node_fabric import NodeFabric
from gui import QDMGraphicsView
from gui.configs import LISTBOX_MIMETYPE
from node_system.node import Node
from node_system.scene import Scene
from state_machine.state_machine import StateMachine


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_drag_drop()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # create graphics scene
        self.scene = Scene()
        self.state_machine = StateMachine(self.scene)

        # create graphics view
        self.view = QDMGraphicsView(self.scene.gr_scene, self.state_machine, self)
        self.layout().addWidget(self.view)

    def init_drag_drop(self):
        self.scene.add_drag_enter_listener(self.on_drag_enter)
        self.scene.add_drop_listener(self.on_drop)

    def on_drag_enter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def on_drop(self, event):
        class_name = event.mimeData().text()
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            mouse_pos = event.pos()
            NodeFabric.add_node_to_scene(self.scene, class_name, mouse_pos.x(), mouse_pos.y())

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def get_act(self):
        return self.scene.act

    def load_scene_form_file(self, file_name):
        self.scene.load_from_file(file_name)

    def save_scene_to_file(self, file_name):
        self.scene.save_to_file(file_name)

    def create_new_scene(self):
        self.scene.clear()
