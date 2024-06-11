# two main APIs QT widgets and QML this course is about QT widgets
from PySide6.QtWidgets import QApplication
import sys
from class_buttonHolder import ButtonHolder

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = ButtonHolder()
  window.show()
  app.exec() #stat event loop
