import sys
from PyQt5.QtWidgets import QApplication
from gui import NodeEditorWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = NodeEditorWindow()
    sys.exit(app.exec_())
