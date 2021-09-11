import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QFileDialog, QMessageBox, QDockWidget

from gui import NodeEditorWidget
from gui.drag_characters_list import DragCharactersList
from gui.drag_node_list import DragNodeList
from qss.qss_loader import load_style_sheets
from utils import ResentFileManager


class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_name = None
        self.resent_files_manager = ResentFileManager()

        load_style_sheets('nodeeditor-dark.qss', 'nodeeditor.qss')
        self.init_ui()
        self.load_resent_file()

    def init_ui(self):
        self.init_file_menu()
        self.init_window_menu()
        self.init_tool_bar()

        self.node_editor_widget = NodeEditorWidget()
        self.setCentralWidget(self.node_editor_widget)

        self.setGeometry(400, 150, 1000, 800)
        self.update_title()
        self.statusBar().show()

        self.init_nodes_dock()
        self.init_characters_dock()

        self.setWindowIcon(self.load_icon('favicon.png'))
        self.show()

    def init_file_menu(self):
        file_menu = self.menuBar().addMenu('File')

        file_menu.addAction(self.create_action('New', 'Ctrl+N', 'Create new Act', self.on_file_new))
        file_menu.addAction(self.create_action('Open', 'Ctrl+O', 'Open', self.on_file_open))
        file_menu.addMenu(self.create_open_resent_menu())
        file_menu.addSeparator()

        file_menu.addAction(self.create_action('Save', 'Ctrl+S', 'Save', self.on_file_save))
        file_menu.addAction(self.create_action('Save As', 'Ctrl+Shift+S', 'Save As', self.on_file_save_as))
        file_menu.addAction(self.create_action('Export', 'Ctrl+E', 'Export to json', self.on_file_export))
        file_menu.addSeparator()

        file_menu.addAction(self.create_action('Quit', 'Ctrl+Q', 'Exit', self.on_file_quit))

    def create_open_file_trigger_handler(self, path):
        def handler():
            is_save = self.call_message_box('Save Act?', "Save Act before open new one?")
            if is_save == QMessageBox.Yes:
                self.on_file_save()
            elif is_save == QMessageBox.Cancel:
                return
            self.open_file(path)

        return handler

    def create_open_resent_menu(self):
        menu = QMenu('Open Resent', self)
        for path in self.resent_files_manager.get_resent_files():
            file = os.path.splitext(os.path.basename(path))[0]
            callback = self.create_open_file_trigger_handler(path)
            action = self.create_action(file, None, None, callback)
            menu.addAction(action)

        return menu

    def init_window_menu(self):
        window_menu = self.menuBar().addMenu('Window')
        window_menu.addAction(self.create_action('Nodes List', 'Ctrl+L', 'Open Nodes List', self.on_window_node_list))
        window_menu.addAction(
            self.create_action('Characters List', None, 'Open Characters List', self.on_window_char_list))

    def create_action(self, name, shortcut, tooltip, callback):
        action = QAction(name, self)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tooltip is not None:
            action.setToolTip(tooltip)
        action.triggered.connect(callback)
        return action

    def init_tool_bar(self):
        toolbar = self.addToolBar('file')
        action = self.create_action('open', '', 'open', self.on_file_open)
        action.setIcon(self.load_icon('open.png'))
        toolbar.addAction(action)

        action = self.create_action('save', '', 'save', self.on_file_save)
        action.setIcon(self.load_icon('save.png'))
        toolbar.addAction(action)

        action = self.create_action('export', '', 'export', self.on_file_export)
        action.setIcon(self.load_icon('export.png'))
        toolbar.addAction(action)

    def load_icon(self, icon_name):
        return QIcon(os.path.join(os.path.dirname(__file__), 'icons', icon_name))

    def load_resent_file(self):
        if self.resent_files_manager.get_last_file() is not None:
            self.open_file(self.resent_files_manager.get_last_file())

    def update_title(self):
        file_name = self.current_file_name if self.current_file_name is not None else 'Undefined'
        self.setWindowTitle("Dialog Graph Redactor. " + file_name)

    def init_nodes_dock(self):
        self.nodes_list_widget = DragNodeList(self.node_editor_widget.get_act(), self)

        self.nodes_dock = QDockWidget('Nodes')
        self.nodes_dock.setWidget(self.nodes_list_widget)
        self.nodes_dock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodes_dock)

    def init_characters_dock(self):
        self.characers_list_widget = DragCharactersList(self)
        self.characers_list_widget.set_act(self.node_editor_widget.get_act())

        self.characters_dock = QDockWidget('Characters')
        self.characters_dock.setWidget(self.characers_list_widget)
        self.characters_dock.setFloating(False)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.characters_dock)

    def on_file_new(self):
        is_save = self.call_message_box('Save Act?', "Save Act before creating new_one?")
        if is_save == QMessageBox.Yes:
            self.on_file_save()
        elif is_save == QMessageBox.Cancel:
            return

        self.current_file_name = None
        self.node_editor_widget.create_new_scene()
        self.characers_list_widget.set_act(self.node_editor_widget.get_act())

    def on_file_open(self):
        is_save = self.call_message_box('Save Act?', "Save Act before open new one?")
        if is_save == QMessageBox.Yes:
            self.on_file_save()
        elif is_save == QMessageBox.Cancel:
            return

        file_name, filter_ = QFileDialog.getOpenFileName(self, 'Open Act File', '', 'Act Scene Files (*.act)')
        self.open_file(file_name)

    def open_file(self, file_name):
        if file_name is not None and file_name != '' and os.path.isfile(file_name):
            self.node_editor_widget.load_scene_form_file(file_name)
            self.characers_list_widget.set_act(self.node_editor_widget.get_act())
            self.current_file_name = file_name
            self.update_title()
            self.statusBar().showMessage('Load ' + self.current_file_name)
            self.resent_files_manager.add_resent_file(self.current_file_name)

    def on_file_save(self):
        if self.current_file_name is None:
            self.on_file_save_as()
        else:
            self.node_editor_widget.save_scene_to_file(self.current_file_name)
            self.statusBar().showMessage('Saved to ' + self.current_file_name)
            self.resent_files_manager.add_resent_file(self.current_file_name)

    def on_file_save_as(self):
        file_name, filter_ = QFileDialog.getSaveFileName(self, 'Save Act File', 'new_act_scene.act',
                                                         'Act Scene Files (*.act)')
        if file_name != '':
            self.node_editor_widget.save_scene_to_file(file_name)
            self.current_file_name = file_name
            self.update_title()
            self.statusBar().showMessage('Saved to ' + self.current_file_name)
            self.resent_files_manager.add_resent_file(self.current_file_name)

    def on_file_export(self):
        if self.current_file_name is None or self.current_file_name == '':
            suggest_file_name = 'new_act'
        else:
            suggest_file_name = os.path.splitext(os.path.basename(self.current_file_name))[0]

        file_name, filter_ = QFileDialog.getSaveFileName(self, 'Save Act File', suggest_file_name,
                                                         'Act Files (*.json)')
        self.node_editor_widget.export_act_to_file(file_name)
        self.statusBar().showMessage('Exported to ' + file_name)

    def on_file_quit(self):
        self.close()

    def closeEvent(self, event) -> None:
        res = self.call_message_box('Save Act before exit?', "Save Act before exit?")
        if res == QMessageBox.Yes:
            self.on_file_save()
        elif res == QMessageBox.Cancel:
            event.ignore()
        else:
            super().closeEvent(event)

    def call_message_box(self, title, text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setDefaultButton(QMessageBox.Cancel)
        return msg_box.exec()

    def on_window_node_list(self):
        self.nodes_dock.show()

    def on_window_char_list(self):
        self.characters_dock.show()
