from PySide6.QtWidgets import QMainWindow, QPushButton


class ButtonHolder(QMainWindow):

    def __init__(self):
        super().__init__()
        button = QPushButton("Press")
        self.setCentralWidget(button)
        #self.show()

