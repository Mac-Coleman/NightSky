import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap

from Hello_Dialog.UI.HelloDialog import Ui_d_helloDialog

class HelloDialog(QWidget, Ui_d_helloDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        pass

    def reject(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    i = HelloDialog()
    i.show()

    sys.exit(app.exec())