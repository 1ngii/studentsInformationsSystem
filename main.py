#Import necessary modules
import sys
from PyQt6.QtWidgets import QWidget,QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIntValidator

#Import the UI and database connection class
from SIS import Ui_Form
from connect_database import ConnectDatabase

#create a main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        #Initialize the UI from a separate UI file
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #Create a database connection object
        self.db = ConnectDatabase()

        #Connect UI elements to class
        self.student_id = self.ui.lineEdit

        #Restrict input to integers
        self.student_id.setValidator(QIntValidator())

        self.first_name = self.ui.lineEdit_2
        self.last_name = self.ui.lineEdit_3
        self.email = self.ui.lineEdit_4
        self.state = self.ui.comboBox
        self.city = self.ui.comboBox_2

        self.add_btn = self.ui.add_btn
        self.update_btn = self.ui.update_btn
        self.select_btn = self.ui.select_btn
        self.search_btn = self.ui.search_btn
        self.clear_btn = self.ui.clear_btn
        self.delete_btn = self.ui.delete_btn

        self.state.setEditable(1)
        self.city.setEditable(1)

        self.result_table = self.ui.tableWidget
        self.result_table.setSortingEnabled(False)
        self.buttons_list = self.ui.function_frame.findChildren(QPushButton)

        # Initialize signal-slot connections
        self.init_signal_slot()

        #pupulate the initial data in the table and state/city dropdown
        self.search_info()
        self.update_state_city()

    def init_signal_slot(self):
        #Connect buttons to their respective functions
        self.add_btn.clicked.connect(self.add_info)
        self.search_btn.clicked.connect(self.search_info)
        self.clear_btn.clicked.connect(self.clear_form_info)
        self.select_btn.clicked.connect(self.select_info)
        self.update_btn.clicked.connect(self.update_info)
        self.delete_btn.clicked.connect(self.delete_info)

    def add_info(self):
        # Function to add student information
        self.disable_buttons()

        student_info = self.get_student_info()

        if student_info["student_id"] and student_info["firstName"]:
            check_result = self.check_student_id(student_id=int(student_info["student_id"]))

            if check_result:
                QMessageBox.information(self, "Warning", "Please input a new student ID",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttons()
                return

            add_result = self.db.add_info(studentId = int(student_info["student_id"]),
                                          first_name=student_info["firstName"],
                                          last_name=student_info["lastName"],
                                          state=student_info["state"],
                                          city=student_info["city"],
                                          email=student_info["emailAddress"])

            if add_result:
                QMessageBox.information(self, "Warning", f"Add fail: {add_result}, Please try again.",
                                        QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Warning", "Please input student ID and first name",
                                    QMessageBox.StandardButton.Ok)

        self.search_info()
        self.enable_buttons()

    def update_info(self):
        # Function to update student information
        new_student_info = self.get_student_info()

        if new_student_info["student_id"]:
            update_result = self.db.update_info(
                studentId=new_student_info["student_id"],
                first_name=new_student_info["firstName"],
                last_name=new_student_info["lastName"],
                state=new_student_info["state"],
                city=new_student_info["city"],
                email=new_student_info["emailAddress"]
            )

            if update_result:
                QMessageBox.information(self, "Warning", f"Fail to update the information: {update_result}, Please try again.",
                                        QMessageBox.StandardButton.Ok)

            else:
                self.search_info()

        else:
            QMessageBox.information(self, "Warning", "Please select one student information to update.")




    def select_info(self):
        # Function to select and populate student information in the form
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.student_id.setEnabled(False)
            student_id = self.result_table.item(select_row, 0).text().strip()
            first_name = self.result_table.item(select_row, 1).text().strip()
            last_name = self.result_table.item(select_row, 2).text().strip()
            email = self.result_table.item(select_row, 5).text().strip()
            state = self.result_table.item(select_row, 3).text().strip()
            city = self.result_table.item(select_row, 4).text().strip()

            self.student_id.setText(student_id)
            self.first_name.setText(first_name)
            self.last_name.setText(last_name)
            self.email.setText(email)
            self.state.setCurrentText(state)
            self.city.setCurrentText(city)

        else:

            QMessageBox.information(self, "Warning", "Please select on student information",
                                    QMessageBox.StandardButton.Ok)

    def disable_buttons(self):
        # Disable all the buttons
        for button in self.buttons_list:
            button.setDisabled(True)

    def enable_buttons(self):
        # Enable all the buttons
        for button in self.buttons_list:
            button.setDisabled(False)

    def search_info(self):
        # Function to search for student information and populate the table
        self.update_state_city()
        student_info = self.get_student_info()
        student_result = self.db.search_info(
            studentId=student_info["student_id"],
            first_name=student_info["firstName"],
            last_name=student_info["lastName"],
            state=student_info["state"],
            city=student_info["city"],
            email=student_info["emailAddress"]
        )

        self.show_data(student_result)

    def clear_form_info(self):
        # Function to clear the form
        self.update_state_city()
        self.student_id.clear()
        self.student_id.setEnabled(True)
        self.first_name.clear()
        self.last_name.clear()
        self.email.clear()
        self.state.setCurrentText("")
        self.city.setCurrentText("")

    def delete_info(self):
        # Function to delete student information
        select_row = self.result_table.currentRow()
        if select_row != -1:
            select_option = QMessageBox.warning(self, "Warning", "Are you sure about deleting this?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if select_option == QMessageBox.StandardButton.Yes:
                student_id = self.result_table.item(select_row, 0).text().strip()

                delete_result = self.db.delete_info(studentId=student_id)
                if not delete_result:
                    self.search_info()
                else:
                    QMessageBox.information(self, "Warning", f"Fail to delete the information: {delete_result}, please try again",
                                            QMessageBox.StandardButton.OK)

        else:
            QMessageBox.information(self, "Warning", "Please select one student information to delete",
                                    QMessageBox.StandardButton.Ok)

    def show_data(self, result):
        # Function to populate the table with student information
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list =[
                    info["studentId"],
                    info["firstName"],
                    info["lastName"],
                    info["state"],
                    info["city"],
                    info["emailAddress"],
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)
        else:
            self.result_table.setRowCount(0)
            return

    def get_student_info(self):
        # Function to retrieve student information from the form

        student_id = self.student_id.text().strip()
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        email = self.email.text().strip()
        state = self.state.currentText().strip()
        city = self.city.currentText().strip()

        student_info = {
            "student_id": student_id,
            "firstName": first_name,
            "lastName": last_name,
            "state": state,
            "city": city,
            "emailAddress": email,
        }

        return student_info

    def check_student_id(self, student_id):
        #Function to check if a student ID already exists
        result = self.db.search_info(studentId=student_id)
        return result

    def update_state_city(self):
        # Function to populate the state and city dropdowns
        state_result = self.db.get_all_states()
        city_result = self.db.get_all_cities()

        self.state.clear()
        self.city.clear()

        state_list = [""]
        for item in state_result:
            for k, v in item.items():
                if v != "":
                    state_list.append(v)

        city_list = [""]
        for item in city_result:
            for k, v in item.items():
                if v != "":
                    city_list.append(v)

        if len(state_list) > 0:
            self.state.addItems(state_list)

        if len(city_list) > 0:
            self.city.addItems(city_list)
#Application entry
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())