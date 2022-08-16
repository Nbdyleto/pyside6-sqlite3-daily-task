from pickle import TRUE
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

        self.create_table()

        self.calendar_date_changed()

        widgets.calendarWidget.selectionChanged.connect(self.calendar_date_changed)

        widgets.tableWidget.cellClicked.connect(self.is_existent_in_db)
        widgets.tableWidget.itemChanged.connect(self.add_or_update_in_db)

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

    def create_table(self):
        db = sqlite3.connect('daily-task/data.db')
        cursor = db.cursor()

        cursor.execute('DROP TABLE IF EXISTS TASKS')

        table = """ CREATE TABLE TASKS (
                    task_name VARCHAR(255) NOT NULL, 
                    completed VARCHAR(255) NOT NULL,
                    date VARCHAR(15) NOT NULL
        );"""
        
        cursor.execute(table)
        print('table is ready!')

    # Functions based on https://github.com/codefirstio/PyQt5-Daily-Task-Planner-App/blob/main/main.py repo

    def update_table_widget(self, date):
        widgets.tableWidget.clear()

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()
        
        query = "SELECT task_name, completed FROM tasks WHERE date = ?"
        row_date = (date,)

        results = cursor.execute(query, row_date).fetchall()
        #print(f'in date {date}... {results}')
        try:
            for row, result in enumerate(results):
                widgets.tableWidget.setItem(row, 0, QTableWidgetItem(result[0]))
                widgets.tableWidget.setItem(row, 1, QTableWidgetItem(result[1]))
                widgets.tableWidget.setItem(row, 2, QTableWidgetItem(result[2]))
                print(result, '\n')
        except Exception:
            print('Não funfou.')

    def add_or_update_in_db(self, item):
        row, col = item.row(), item.column()
        new_value = item.text()
        task_name = widgets.tableWidget.item(row, 0).text()
        date = widgets.calendarWidget.selectedDate().toPython()

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        field_list = ['task_name', 'completed', 'date']
        act_field = field_list[col]

        if self.existent_in_db:  
            # cell clicked is existent in db, so, update old data.
            query_update = "UPDATE tasks SET ?=? WHERE task_name=?"
            new_row_data = (act_field, new_value, task_name,)
            cursor.execute(query_update, new_row_data)
        else:   
            # cell clicked is not existent in db, so, create new data.
            query_insert = "INSERT INTO tasks(task_name, completed, date) VALUES (?,?,?)"
            new_row_data = (task_name, "NO", date,)
            cursor.execute(query_insert, new_row_data)
        
        db.commit()
        self.update_table_widget(date)
        #db.close()
    
    def is_existent_in_db(self, row):
        db = sqlite3.connect('daily-task/data.db')
        cursor = db.cursor()
        query = """
            SELECT colunm_name FROM tasks WHERE EXISTS task_name = ?
        """
        task_name = widgets.tableWidget.itemAt(row, 0) # task name.
        if task_name != None:
            print(f'task_name: {task_name} EXISTENT!')
            cursor.execute(query, (task_name,))
            self.existent_in_db = True
        else:
            print(f'task_name: {task_name} NOT EXISTENT!')
            self.existent_in_db = False

    #####

    # PySide6.QtCore.QDate(2022, 8, 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setStyleSheet('background-color: #282a36;')
    window.show()
    sys.exit(app.exec())