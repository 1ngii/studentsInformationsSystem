#Import necessary modules
import sys
from PyQt6.QtWidgets import QWidget,QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIntValidator

#Import the UI and database connection class
from SIS import Ui_Form
from connect_database import ConnectDatabase

#create a main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        #Initialize the UI from a seperate UI file
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #Create a database connection object
        self.db = ConnectDatabase()

        #Connect UI elements to class variables

#Application entry
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())