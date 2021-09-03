import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

from gui.widgets import QDMTextEdit
from utils import Serializable


class ActNodeWidget(QWidget, Serializable):
    serialize_fields = [('initial_delay', int), ('auto_skip_delay', int),
                        ('next_nodes_id', int)]

    def __init__(self, node=None, parent=None):
        super().__init__()
        self.node = node if node is not None else parent
        self.node.content_widget = self

        self.initial_delay = 2000
        self.auto_skip_delay = 1000
        self.next_nodes_id = []

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.layout)

        self.label = QLabel("Some title")
        self.layout.addWidget(self.label)

    def connect_to_socket(self, socket):
        pass

    @property
    def actual_class_name(self):
        return type(self).__name__

    @actual_class_name.setter
    def actual_class_name(self, value):
        pass

    @staticmethod
    def get_name():
        return 'Undefined'

    @staticmethod
    def get_image():
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'icons', 'no_image.png'))
        pixmap = pixmap.scaled(64, 64)
        return pixmap
