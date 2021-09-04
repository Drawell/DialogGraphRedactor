from PyQt5.QtWidgets import QTextEdit


class DeleteProofTextEdit(QTextEdit):
    def __init__(self, text, node, parent=None):
        super().__init__(text, parent=parent)
        self.node = node

    def focusInEvent(self, e) -> None:
        self.node.scene.set_editing_flag(True)
        super().focusInEvent(e)

    def focusOutEvent(self, e) -> None:
        self.node.scene.set_editing_flag(False)
        super().focusOutEvent(e)
