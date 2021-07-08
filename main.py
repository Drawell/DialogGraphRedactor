import sys
from PyQt5.QtWidgets import QApplication
from gui.node_editor_wnd import NodeEditorWnd

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = NodeEditorWnd()
    sys.exit(app.exec_())
