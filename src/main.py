# two main APIs QT widgets and QML this course is about QT widgets
from PySide6.QtWidgets import QApplication
import sys
from class_buttonHolder import ButtonHolder
from Main_Window import MainWindow

if __name__ == "__main__":
  app = QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  # window = ButtonHolder()
  # window.show()
  app.exec() #stat event loop
