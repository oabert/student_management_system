import sqlite3
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student management system')
        self.setMinimumSize(600, 500)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu_item = menubar.addMenu('&File')
        help_menu_item = menubar.addMenu('&Help')
        edit_menu_item = menubar.addMenu('&Edit')

        add_student_action = QAction(QIcon('icons/add.png'), 'Add student', self)
        # self.accepted.emit()
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole) fom mac
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon('icons/search.png'), 'Search', self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        # Create table with student data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)
        self.show()
        self.load_data()

        # Create a toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create statusbar(foot)
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_btn = QPushButton('Edit record')
        edit_btn.clicked.connect(self.edit)

        delete_btn = QPushButton('Delete record')
        delete_btn.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(delete_btn)

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        # dialog.accepted.connect(self.load_data)
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        # dialog.accepted.connect(self.load_data)
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit student data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name from selected row
        index = main_page.table.currentRow()
        student_name = main_page.table.item(index, 1).text()

        # Get student id from selected row
        self.student_id = main_page.table.item(index, 0).text()

        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # # Add combo box of courses
        course_name_edit = main_page.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name_edit)
        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile_edit = main_page.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile_edit)
        self.mobile.setPlaceholderText('Phone')
        layout.addWidget(self.mobile)

        # Add submit btn
        button = QPushButton('Register')
        button.clicked.connect(self.update_student_data)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student_data(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name = ?, course = ?, mobile = ? WHERE id =?',
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh the table data
        main_page.load_data()

        # Close the window
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit student data')

        layout = QGridLayout()
        confirmation = QLabel('Are you sure you want to delete?')
        yes = QPushButton('Yes')
        no = QPushButton('No')

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student_data)

    def delete_student_data(self):
        # Get student id from selected row
        index = main_page.table.currentRow()
        student_id = main_page.table.item(index, 0).text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE from students WHERE id = ?', (student_id,))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh the table data
        main_page.load_data()

        # Close the window
        self.close()

        # Confirmation message of delete data
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle('Success')
        confirmation_widget.setText('The record was deleted successfully!')
        confirmation_widget.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert student data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # # Add combo box of courses
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('Phone')
        layout.addWidget(self.mobile)

        # Add submit btn
        button = QPushButton('Register')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # print('Test connection.cursor')
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)',
                       (name, course, mobile))
        # print('Test cursor.execute')

        connection.commit()
        cursor.close()
        connection.close()
        main_page.load_data()

        # Close the window
        self.close()


# Class create search window
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Create btn
        search_btn = QPushButton('Search')
        search_btn.clicked.connect(self.search)
        layout.addWidget(search_btn)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        rows = list(result)
        print(rows)
        items = main_page.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_page.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        content = """
        This app was created as an portfolio example
        """
        self.setText(content)


app = QApplication(sys.argv)
main_page = MainWindow()
main_page.show()
main_page.load_data()
sys.exit(app.exec_())
