from gui import QDMGraphicsNode
from gui import QDMNodeContentWidget
from .socket import Socket, ESocketPosition as esp


class Node:
    def __init__(self, scene, title='Undefined', inputs=[], outputs=[]):
        self.scene = scene
        self.title = title

        self.content_widget = QDMNodeContentWidget()
        self.gr_node = QDMGraphicsNode(self)

        self.scene.add_node(self)

        self.inputs = []
        self.outputs = []

        for idx, item in enumerate(inputs):
            socket = Socket(node=self, index=idx, position=esp.LEFT_TOP)
            self.inputs.append(socket)

        for idx, item in enumerate(outputs):
            socket = Socket(node=self, index=idx, position=esp.RIGHT_TOP)
            self.outputs.append(socket)

