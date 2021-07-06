from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout
from node_graphics_scene import QDMGraphicsScene


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Dialog Graph Redactor")

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # create graphics scene
        self.gr_scene = QDMGraphicsScene()

        # create graphics view
        self.view = QGraphicsView(self)
        self.view.setScene(self.gr_scene)
        self.layout().addWidget(self.view)

        self.show()
