from os import path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from gui.widgets import DeleteProofLineEdit
from node_system.node import Node
from utils import Serializable


class ActNodeWidget(QWidget, Serializable):
    serialize_fields = [('initial_delay', int), ('auto_skip_delay', int),
                        ('next_nodes_id', int)]

    ICON_SIZE = 64

    def __init__(self, node=None, parent=None):
        super().__init__()
        self._node = None
        self.initial_delay = 2000
        self.auto_skip_delay = 1000

        if type(parent) is Node:
            self.node = parent
            self.node.content_widget = self
        if node is not None:
            self.node = node
            self.node.content_widget = self

        # self.node = node if node is not None else None

        self.next_nodes_id = []

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        if self._node is None:
            self._node = value
            self.init_ui()

    @property
    def initial_delay(self):
        return self._initial_delay

    @initial_delay.setter
    def initial_delay(self, value):
        self._initial_delay = int(value)
        if self._node is not None:
            self.initial_delay_edit.setText(str(value))

    @property
    def auto_skip_delay(self):
        return self._auto_skip_delay

    @auto_skip_delay.setter
    def auto_skip_delay(self, value):
        self._auto_skip_delay = int(value)
        if self._node is not None:
            self.auto_skip_delay_edit.setText(str(value))

    def init_ui(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(scroll_area)
        self.setLayout(root_layout)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        proxy_widget = QWidget(self)
        proxy_widget.setLayout(self.layout)
        scroll_area.setWidget(proxy_widget)

        self.layout.addWidget(QLabel('Initial Delay:'))
        self.initial_delay_edit = DeleteProofLineEdit(str(self._initial_delay), self.node)
        self.initial_delay_edit.setValidator(QIntValidator(-10, 10000, self))
        self.initial_delay_edit.textChanged.connect(self.on_initial_delay_changed)
        self.layout.addWidget(self.initial_delay_edit)

        self.layout.addWidget(QLabel('AutoSkipDelay:'))
        self.auto_skip_delay_edit = DeleteProofLineEdit(str(self.auto_skip_delay), self.node)
        self.auto_skip_delay_edit.setValidator(QIntValidator(-10, 10000, self))
        self.auto_skip_delay_edit.textChanged.connect(self.on_auto_skip_delay_changed)
        self.layout.addWidget(self.auto_skip_delay_edit)

    def on_initial_delay_changed(self):
        self._initial_delay = int(self.initial_delay_edit.text())

    def on_auto_skip_delay_changed(self):
        self._auto_skip_delay = int(self.auto_skip_delay_edit.text())

    def add_next_node(self, next_act_node):
        if next_act_node.id in self.next_nodes_id:
            return
        self.next_nodes_id.append(next_act_node.id)

    def remove_next_node(self, next_act_node):
        if next_act_node is None or next_act_node.id not in self.next_nodes_id:
            return
        self.next_nodes_id.remove(next_act_node.id)

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
        return ActNodeWidget.load_from_icons('no_image.png')

    @staticmethod
    def load_from_icons(image):
        return QPixmap(path.join(path.dirname(__file__), 'icons', image)) \
            .scaled(ActNodeWidget.ICON_SIZE, ActNodeWidget.ICON_SIZE)

    def __str__(self):
        return self.get_name()
