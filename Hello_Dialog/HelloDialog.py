import sys
from PySide6.QtWidgets import QApplication, QDialog

from Hello_Dialog.UI.HelloDialog import Ui_d_helloDialog

class HelloDialog(QDialog, Ui_d_helloDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def getLocation(self):
        return self.w_locationGetter.location

if __name__ == "__main__":
    app = QApplication(sys.argv)

    i = HelloDialog()

    i.setModal(True)
    i.open()

    def result(status):
        if status:
            print(i.getLocation())
        else:
            print(f"rejected: {status}")

    i.finished.connect(result)

    sys.exit(app.exec())