import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QFileDialog, QMessageBox, QDockWidget

from gui import NodeEditorWidget
from gui.drag_node_list import DragNodeList
from qss.qss_loader import load_style_sheets


class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_name = None

        load_style_sheets('nodeeditor-dark.qss', 'nodeeditor.qss')
        self.init_ui()

    def init_ui(self):
        self.init_file_menu()
        self.init_window_menu()

        self.node_editor_widget = NodeEditorWidget()
        self.setCentralWidget(self.node_editor_widget)

        self.setGeometry(400, 150, 1000, 800)
        self.update_title()
        self.statusBar().show()

        self.init_nodes_dock()

        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icons', 'favicon.png')))
        self.show()

    def init_file_menu(self):
        file_menu = self.menuBar().addMenu('File')

        file_menu.addAction(self.create_action('New', 'Ctrl+N', 'Create new Act', self.on_file_new))
        file_menu.addSeparator()
        file_menu.addAction(self.create_action('Save', 'Ctrl+S', 'Save', self.on_file_save))
        file_menu.addAction(self.create_action('Save As', 'Ctrl+Shift+S', 'Save As', self.on_file_save_as))
        file_menu.addAction(self.create_action('Open', 'Ctrl+O', 'Open', self.on_file_open))
        file_menu.addMenu(self.create_open_resent_menu())
        file_menu.addSeparator()
        file_menu.addAction(self.create_action('Quit', 'Ctrl+Q', 'Exit', self.on_file_quit))

    def init_window_menu(self):
        window_menu = self.menuBar().addMenu('Window')
        window_menu.addAction(self.create_action('Nodes List', 'Ctrl+L', 'Open Nodes List', self.on_window_list_widget))

    def create_action(self, name, shortcut, tooltip, callback):
        action = QAction(name, self)
        action.setShortcut(shortcut)
        action.setToolTip(tooltip)
        action.triggered.connect(callback)
        return action

    def create_open_resent_menu(self):
        menu = QMenu('Open Resent', self)
        return menu

    def update_title(self):
        file_name = self.current_file_name if self.current_file_name is not None else 'Undefined'
        self.setWindowTitle("Dialog Graph Redactor. " + file_name)

    def init_nodes_dock(self):
        self.nodes_list_widget = DragNodeList(self.node_editor_widget.get_act(), self)

        self.nodes_dock = QDockWidget('Nodes')
        self.nodes_dock.setWidget(self.nodes_list_widget)
        self.nodes_dock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodes_dock)

    def on_file_new(self):
        self.node_editor_widget.create_new_scene()

    def on_file_save(self):
        if self.current_file_name is None:
            self.on_file_save_as()
        else:
            self.node_editor_widget.save_scene_to_file(self.current_file_name)
            self.statusBar().showMessage('Saved to ' + self.current_file_name)

    def on_file_save_as(self):
        file_name, filter_ = QFileDialog.getSaveFileName(self, 'Save Act File', 'new_act_scene.act',
                                                         'Act Scene Files (*.act)')
        if file_name != '':
            self.node_editor_widget.save_scene_to_file(file_name)
            self.current_file_name = file_name
            self.update_title()
            self.statusBar().showMessage('Saved to ' + self.current_file_name)

    def on_file_open(self):
        file_name, filter_ = QFileDialog.getOpenFileName(self, 'Open Act File', '', 'Act Scene Files (*.act)')
        if file_name != '' and os.path.isfile(file_name):
            self.node_editor_widget.load_scene_form_file(file_name)
            self.current_file_name = file_name
            self.update_title()
            self.statusBar().showMessage('Load ' + self.current_file_name)
        pass

    def on_file_quit(self):
        self.close()

    def closeEvent(self, event) -> None:
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Save Act before exit?')
        msg_box.setText("Save Act before exit?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setDefaultButton(QMessageBox.Cancel)
        res = msg_box.exec()
        if res == QMessageBox.Yes:
            self.on_file_save()
        elif res == QMessageBox.Cancel:
            event.ignore()
        else:
            super().closeEvent(event)

    def on_window_list_widget(self):
        self.nodes_dock.show()
