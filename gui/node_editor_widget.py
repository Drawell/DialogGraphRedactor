from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction

from acts_system.node_fabric import NodeFabric
from gui import QDMGraphicsView
from gui.configs import LISTBOX_MIMETYPE
from node_system.scene import Scene
from state_machine.state_machine import StateMachine


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_drag_drop()
        self.init_context_menu_actions()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # create graphics scene
        self.scene = Scene()
        self.state_machine = StateMachine(self.scene)

        # create graphics view
        self.view = QDMGraphicsView(self.scene.gr_scene, self.state_machine, self)
        self.layout().addWidget(self.view)

    def init_context_menu_actions(self):
        self.context_menu_actions = []
        for node_class in self.get_act().get_node_class_list():
            action = QAction(QIcon(node_class.get_image()), node_class.get_name())
            self.context_menu_actions.append(action)

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

    def export_act_to_file(self, file_name):
        self.scene.export_act_to_file(file_name)

    def create_new_scene(self):
        self.scene.clear()

    def contextMenuEvent(self, event) -> None:
        try:
            item = self.scene.get_item_at(event.pos())
            if item is None:
                self.handle_new_node_context_menu(event)
        except Exception as e:
            print(str(e))

    def handle_new_node_context_menu(self, event):
        context_menu_new_node = QMenu(self)
        for action in self.context_menu_actions:
            context_menu_new_node.addAction(action)
        action = context_menu_new_node.exec_(self.mapToGlobal(event.pos()))

        if action is not None:
            class_name = action.text()
            mouse_pos = event.pos()
            node = NodeFabric.add_node_to_scene(self.scene, class_name, mouse_pos.x(), mouse_pos.y())
            if node is not None and self.state_machine.is_dragging_to_input():
                self.state_machine.on_mouse_left_release(node.input)
