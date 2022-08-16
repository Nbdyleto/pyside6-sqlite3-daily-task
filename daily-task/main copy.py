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
        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        query_insert = "INSERT INTO tasks(task_name, completed, date) VALUES (?,?,?)"
        values = ('a', 'NO', '10')
        cursor.execute(query_insert, values)

        query_insert = "INSERT INTO tasks(task_name, completed, date) VALUES (?,?,?)"
        values = ('b', 'NO', '10')
        cursor.execute(query_insert, values)
        db.commit()
        db.close()
        

        self.calendar_date_changed()

        widgets.calendarWidget.selectionChanged.connect(self.calendar_date_changed)

        widgets.tableWidget.cellClicked.connect(self.is_existent_in_db)
        widgets.tableWidget.itemChanged.connect(self.update_db)

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
        self.update_table_widget(str(date_selected))

    # Functions based on https://github.com/codefirstio/PyQt5-Daily-Task-Planner-App/blob/main/main.py repo

    def update_table_widget(self, date):
        widgets.tableWidget.clear()

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        results = cursor.execute("SELECT * from tasks").fetchall()
        db.close()
        print(results)
        try:
            tablerow = 0
            for row in results:
                print('Setting values')
                widgets.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[0]))
                widgets.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
                widgets.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[2]))
                tablerow += 1
        except Exception:
            print('Não funfou.')
    
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

    def saveChanges(self):
        pass

    # atributtes from each task:
    # name, topic, start_date, limit_date, checked.

    def update_db(self, item):
        row, col = item.row(), item.column()
        new_value = item.text()
        task_name = widgets.tableWidget.item(row, 0).text()
        date = widgets.calendarWidget.selectedDate().toPython()

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        field_list = ['task_name', 'completed', 'date']
        act_field = field_list[col]

        if self.existent_in_db:  
            # existent in db, so, update old data.
            query_update = "UPDATE tasks SET ?=? WHERE task_name=?"
            new_row_data = (act_field, new_value, task_name)
            cursor.execute(query_update, new_row_data)
        else:   
            # not existent in db, so, create new data.
            print(f'task_name: {task_name} NOT EXISTENT, CREATING...')
            query_insert = "INSERT INTO tasks(task_name, completed, date) VALUES (?,?,?)"
            new_row_data = (task_name, "NO", date,)
            cursor.execute(query_insert, new_row_data)
            self.existent_in_db = True
        
        db.commit()
        db.close()
        self.update_table_widget(str(date))
    
    def is_existent_in_db(self, row):
        db = sqlite3.connect('daily-task/data.db')
        cursor = db.cursor()
        query = 'SELECT task_name FROM tasks WHERE task_name = ?'
        try:
            task_name = widgets.tableWidget.item(row, 0).text() # task name.
            print(task_name)
            cursor.execute(query, [task_name])
            print(f'task_name: {task_name} EXISTENT!')
            self.existent_in_db = True
        except Exception:
            print('NOT EXISTENT!')
            self.existent_in_db = False
        print(self.existent_in_db, '\n')

    #####

    # PySide6.QtCore.QDate(2022, 8, 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setStyleSheet('background-color: #282a36;')
    window.show()
    sys.exit(app.exec())