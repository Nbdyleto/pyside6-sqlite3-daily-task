from PySide6.QtWidgets import QWidget, QApplication, QListWidgetItem, QTableWidgetItem, QMessageBox, QCheckBox
from PySide6.QtCore import QDate, QPoint
from PySide6.QtGui import QBrush, QColor
from matplotlib import widgets
from ui_main import Ui_Form
import sys
import sqlite3

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        widgets.tableWidget.setColumnWidth(0,100)
        widgets.tableWidget.setColumnWidth(1,100)
        widgets.tableWidget.setColumnWidth(2,100)
        widgets.tableWidget.setColumnWidth(3,150)
        widgets.tableWidget.setRowCount(15)
        widgets.tableWidget.setItem(0, 0, QTableWidgetItem('test'))

        self.calendar_date_changed()

        widgets.calendarWidget.selectionChanged.connect(self.calendar_date_changed)

        widgets.tableWidget.itemChanged.connect(self.add_new_task)

    def event_test(self, row, col):
        print(row, col)
        item = widgets.tableWidget.item(row, col)
        print(item.text())

    def change_data(self, item):
        pass

    def calendar_date_changed(self):
        print('the calendar date has changed! \n')
        date_selected = widgets.calendarWidget.selectedDate().toPython()
        print(f'date: {date_selected}')
        self.update_table_widget(date_selected)

    # Functions based on https://github.com/codefirstio/PyQt5-Daily-Task-Planner-App/blob/main/main.py repo

    def update_table_widget(self, date):
        widgets.tableWidget.clear()

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()
        #self.create_table()
        try:
            query = "SELECT task, completed FROM tasks WHERE date = ?"
            row_date = (date,)
        except Exception:  
            self.create_table()
            query = "SELECT task, completed FROM tasks WHERE date = ?"
            row_date = (date,)

        results = cursor.execute(query, row_date).fetchall()
        for row, result in enumerate(results):
            print('aaa ', result[0], result[1])
            widgets.tableWidget.setItem(row, 0, QTableWidgetItem(result[0]))
            widgets.tableWidget.setItem(row, 1, QTableWidgetItem(result[1]))
            #widgets.tableWidget.setItem(row, 2, QTableWidgetItem(result[2]))
            print(result, '\n')
    
    def create_table(self):
        db = sqlite3.connect('daily-task/data.db')
        cursor = db.cursor()

        cursor.execute('DROP TABLE IF EXISTS TASKS')

        table = """ CREATE TABLE TASKS (
                    task VARCHAR(255) NOT NULL, 
                    completed VARCHAR(255) NOT NULL,
                    date VARCHAR(15) NOT NULL
        );"""
        
        cursor.execute(table)
        print('table is ready!')

    def saveChanges(self):
        pass

    # atributtes from each task:
    # name, topic, start_date, limit_date, checked.

    def add_new_task(self, item):
        row = item.row()

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        new_task = widgets.tableWidget.item(row, 0).text()

        #newTask = str(self.taskLineEdit.text())
        date = widgets.calendarWidget.selectedDate().toPython()

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row_data = (new_task, "NO", date,)

        cursor.execute(query, row_data)
        db.commit()
        self.update_table_widget(date)

    #####

    # PySide6.QtCore.QDate(2022, 8, 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setStyleSheet('background-color: #282a36;')
    window.show()
    sys.exit(app.exec())