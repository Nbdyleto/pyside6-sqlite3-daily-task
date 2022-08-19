from pickle import NONE
from PySide6.QtWidgets import QWidget, QApplication, QListWidgetItem, QTableWidgetItem, QMessageBox, QCheckBox
from PySide6.QtCore import QDate, QPoint, QSize
from PySide6.QtGui import QBrush, QColor, QIcon
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

        widgets.tableWidget.setColumnWidth(0,200)
        widgets.tableWidget.setColumnWidth(1,150)
        widgets.tableWidget.setColumnWidth(2,100)
        widgets.tableWidget.setColumnWidth(3,100)
        widgets.tableWidget.setColumnWidth(4,100)
        widgets.tableWidget.setRowCount(15)
        self.columnLabels = ["Make","Model","Price"]
        widgets.tableWidget.setHorizontalHeaderLabels(self.columnLabels)

        #self.create_table()
        
        self.load_data_in_table()

        widgets.calendarWidget.selectionChanged.connect(self.calendar_date_changed)
        widgets.calendarWidget.setVisible(False)
        self.selected_task = None
        self.existent_in_db = False
        self.selected_date = QDate.currentDate().toPython()
        self.selected_date_cel = []
        widgets.tableWidget.cellClicked.connect(self.is_existent_in_db)
        widgets.tableWidget.itemChanged.connect(self.update_db)

    def change_data(self, item):
        pass

    # Functions based on https://github.com/codefirstio/PyQt5-Daily-Task-Planner-App/blob/main/main.py repo

    def load_data_in_table(self):
        widgets.tableWidget.clear()

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        # order by in mysql ...
        results = cursor.execute("SELECT * from tasks").fetchall()
        db.close()
        print(results)

        ico = QIcon()
        ico.addFile('cil-check', QSize(36, 36), QIcon.Normal, QIcon.On)

        try:
            tablerow = 0
            for row in results:
                widgets.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[0]))
                widgets.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
                widgets.tableWidget.item(tablerow, 1).setIcon(ico)
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

    def update_db(self, item, is_date_type = False):
        row, col = item.row(), item.column()
        new_value = item.text()
        task_name = self.selected_task
        date = self.selected_date
        if is_date_type:
            new_value = date

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        field_list = ['task_name', 'completed', 'date']
        act_field = field_list[col]

        print(item.row(), item.column())
        print(f'act_field: {act_field}, new value: {new_value}, task_name: {task_name}, existent in db? {self.existent_in_db}')

        if self.existent_in_db:
            # existent in db, so, update old data.
            #print(f'task_name: {task_name} EXISTENT, UPDATING...')
            query_update = f"UPDATE tasks SET {act_field} = '{new_value}' WHERE task_name = '{task_name}'"
            print(query_update)
            cursor.execute(query_update)
            db.commit()
            self.existent_in_db = None
            self.load_data_in_table()
            
        if self.existent_in_db == False: 
            # not existent in db, so, create new data.
            #print(f'task_name: {task_name} NOT EXISTENT, CREATING...')
            query_insert = "INSERT INTO tasks(task_name, completed, date) VALUES (?,?,?)"
            print(query_insert)
            new_row_data = (new_value, "Not Started", date,)
            cursor.execute(query_insert, new_row_data)
            self.existent_in_db = None
            db.commit()
            db.close()
            self.load_data_in_table()

    def is_existent_in_db(self, row, col):
        db = sqlite3.connect('daily-task/data.db')
        cursor = db.cursor()
        query = 'SELECT task_name FROM tasks WHERE task_name = ?'

        try:
            self.selected_task = widgets.tableWidget.item(row, 0).text() # task name.
            self.selected_task_data = widgets.tableWidget.item(row, col).text()
            cursor.execute(query, [self.selected_task])
            print(f'task_name: {self.selected_task} EXISTENT!')
            self.existent_in_db = True
        except Exception:
            print('NOT EXISTENT!')
            self.existent_in_db = False
        print(self.existent_in_db, '\n')

        if col == 2: # date
            self.show_calendar(row, col)
        else:
            self.hide_calendar()

    def show_calendar(self, row, col):
        widgets.calendarWidget.setVisible(True)
        X_VALUE, Y_VALUE = 230, 205
        widgets.calendarWidget.move(X_VALUE, Y_VALUE+(row*10))
        self.selected_date_cel = (row, col)
        print(f'show calendar... {self.selected_date_cel}')

    def hide_calendar(self):
        widgets.calendarWidget.setVisible(False)

    def reset_calendar_date(self):
        self.selected_date = QDate.currentDate().toPython()

    def calendar_date_changed(self):
        self.hide_calendar()
        print('the calendar date has changed! \n')
        self.selected_date = widgets.calendarWidget.selectedDate().toPython()
        print(f'new date: {self.selected_date}')
        item = widgets.tableWidget.item(self.selected_date_cel[0], self.selected_date_cel[1])
        self.update_db(item, is_date_type=True)
        self.reset_calendar_date()

    #####

    # PySide6.QtCore.QDate(2022, 8, 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setStyleSheet('background-color: #282a36;')
    window.show()
    sys.exit(app.exec())