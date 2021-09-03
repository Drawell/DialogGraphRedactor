import os

from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QApplication


def load_style_sheet(filename: str):
    filename = os.path.join(os.path.dirname(__file__), filename)
    file = QFile(filename)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))


def load_style_sheets(*args):
    res = ''
    for arg in args:
        filename = os.path.join(os.path.dirname(__file__), arg)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        res += "\n" + str(stylesheet, encoding='utf-8')

    QApplication.instance().setStyleSheet(res)