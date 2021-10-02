from os import path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from node_system.node import Node
from utils import Serializable


class ActNodeWidget(QWidget, Serializable):
    icon = 'no_icon.png'
    serialize_fields = [('initial_delay', int), ('auto_skip_delay', int),
                        ('next_nodes_id', int)]

    ICON_SIZE = 64

    def __init__(self, node=None, parent=None):
        super().__init__()
        self._node = None
        self.initial_delay = 0
        self.auto_skip_delay = 0
        self.act = None
        self.is_add_stretch = True

        if type(parent) is Node:
            self.node = parent
            self.node.content_widget = self
        if node is not None:
            self.node = node
            self.node.content_widget = self

        self.next_nodes_id = []

    def set_act(self, act):
        self.act = act

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        if self._node is None:
            self._node = value
            self.init_ui()
            self.set_act(self._node.scene.act)

    @property
    def initial_delay(self):
        return self._initial_delay

    @initial_delay.setter
    def initial_delay(self, value):
        self._initial_delay = int(value)

    @property
    def auto_skip_delay(self):
        return self._auto_skip_delay

    @auto_skip_delay.setter
    def auto_skip_delay(self, value):
        self._auto_skip_delay = int(value)

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

        self.init_sub_class_ui()

        if self.is_add_stretch:
            self.layout.addStretch()

    def init_sub_class_ui(self):
        pass

    def add_next_node(self, next_act_node, idx=0):
        if next_act_node.id in self.next_nodes_id:
            return
        if len(self.next_nodes_id) <= idx:
            for i in range(len(self.next_nodes_id), idx + 1):
                self.next_nodes_id.append(-1)

        self.next_nodes_id[idx] = next_act_node.id

    def remove_next_node(self, next_act_node):
        if next_act_node is None or next_act_node.id not in self.next_nodes_id:
            return
        idx = self.next_nodes_id.index(next_act_node.id)
        self.next_nodes_id[idx] = -1

    def remove(self):
        pass

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_image(cls):
        icon_path = path.join(path.dirname(__file__), 'icons', cls.icon)
        if not path.exists(icon_path):
            icon_path = path.join(path.dirname(__file__), 'icons', ActNodeWidget.icon)

        return QPixmap(icon_path).scaled(ActNodeWidget.ICON_SIZE, ActNodeWidget.ICON_SIZE)

    def __str__(self):
        return self.get_name()
