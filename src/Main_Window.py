from PySide6.QtWidgets import (QMainWindow, QDockWidget, QListWidget, QTextEdit)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QStress')
        self.setWindowIcon(QIcon('../png/logo/logo_rod.png'))
        self.showMaximized()

