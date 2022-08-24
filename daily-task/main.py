from pickle import NONE
from PySide6.QtWidgets import QWidget, QApplication, QAbstractItemView, QListWidgetItem, QTableWidgetItem, QMessageBox, QCheckBox
from PySide6.QtCore import QDate, QPoint, QSize
from PySide6.QtGui import QBrush, QColor, QIcon
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
        widgets.tableWidget.setColumnWidth(2,150)
        widgets.tableWidget.setColumnWidth(3,150)
        widgets.tableWidget.setColumnWidth(4,100)

        @property
        def row_count(self):
            return getattr(self, '_row_count', 1)
        
        @row_count.setter
        def row_count(self, val):
            self._row_count = val

        self.create_table()
        
        self.load_data_in_table()

        widgets.calendarWidget.selectionChanged.connect(self.calendar_date_changed)
        widgets.calendarWidget.setVisible(False)
        self.selected_task = None
        self.existent_in_db = False
        self.slc_start_date = QDate.currentDate().toPython()
        self.slc_end_date = QDate.currentDate().toPython()
        self.slc_date_cel = []
        widgets.tableWidget.cellClicked.connect(self.is_existent_in_db)
        widgets.tableWidget.itemChanged.connect(self.update_db)
        self.slc_row, self.slc_col = None, None

    def change_data(self, item):
        pass

    # Functions based on https://github.com/codefirstio/PyQt5-Daily-Task-Planner-App/blob/main/main.py repo

    def load_data_in_table(self):
        widgets.tableWidget.clear()
        
        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()
        
        count = cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

        self.row_count = count+1
        widgets.tableWidget.setRowCount(self.row_count)

        # how order by in mysql?...

        results = cursor.execute("SELECT * from tasks").fetchall()
        
        print(results)

        try:
            tablerow = 0
            for row in results:
                widgets.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[0]))
                widgets.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
                widgets.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[2]))
                widgets.tableWidget.setItem(tablerow, 3, QTableWidgetItem(row[3]))
                widgets.tableWidget.setItem(tablerow, 4, QTableWidgetItem(self.test[row[4]][1])) #row[4] = topic_id
                tablerow += 1
        except Exception:
            print('Não funfou.')
        db.close()
    
    def create_table(self):
        db = sqlite3.connect('daily-task/data.db')
        cursor = db.cursor()

        # Child Table
        cursor.execute('DROP TABLE IF EXISTS tasks')
        tbl_tasks = """ CREATE TABLE tasks (
            task_name VARCHAR(255) NOT NULL, 
            completed VARCHAR(255) NOT NULL,
            start_date VARCHAR(15) NOT NULL,
	        end_date VARCHAR(10) NOT NULL,	
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
            	REFERENCES topics (topic_id)

        );"""
        cursor.execute(tbl_tasks)
        print('table tasks is ready!')
        
        # Parent Table:
        cursor.execute('DROP TABLE IF EXISTS topics')
        tbl_topics = """ CREATE TABLE topics (
            topic_id INTEGUER PRIMARY KEY,
            topic_name VARCHAR(255) NOT NULL
        );"""
        cursor.execute(tbl_topics)

        print('table topics is ready!')

        # populate topics table
        
        poptbl = """INSERT INTO topics (topic_id, topic_name) VALUES (0, 'Math');"""
        cursor.execute(poptbl)

        poptbl = """INSERT INTO topics (topic_id, topic_name) VALUES (1, 'Geo');"""
        cursor.execute(poptbl)

        print('table topics populate with 2 instances!')

        self.test = cursor.execute("SELECT * FROM topics").fetchall()
        print(self.test)

    def saveChanges(self):
        pass

    # atributtes from each task:
    # name, topic, start_date, limit_date, checked.

    def update_db(self, item, is_date_type = False):
        row, col = item.row(), item.column()
        new_value = item.text()
        task_name = self.selected_task
        start_date = self.slc_start_date
        end_date = self.slc_end_date
        if is_date_type:
            if self.slc_col == 2:
                new_value = start_date
            elif self.slc_col == 3:
                new_value = end_date
            else:
                self.slc_start_date, self.slc_end_date = None, None

        db = sqlite3.connect("daily-task/data.db")
        cursor = db.cursor()

        field_list = ['task_name', 'completed', 'start_date', 'end_date', 'topic_id']
        act_field = field_list[col]

        #print(item.row(), item.column())
        print(f'actual field: {item.text()}')

        if self.existent_in_db:
            # existent in db, so, update old data.
            query_update = f"UPDATE tasks SET {act_field} = '{new_value}' WHERE task_name = '{task_name}'"
            print(query_update)
            cursor.execute(query_update)
            db.commit()
            self.existent_in_db = None
            self.load_data_in_table()
            
        if self.existent_in_db == False: 
            # not existent in db, so, create new data.
            query_insert = f"INSERT INTO tasks(task_name, completed, start_date, end_date, topic_id) VALUES (?,?,?,?,?)"
            print(query_insert)
            new_row_data = (new_value, "Not Started", start_date, end_date, 1)
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

        self.slc_row, self.slc_col = row, col

        if ((col == 2 or col == 3) and self.existent_in_db == True): # start_date or end_date
            self.show_calendar()
        elif col == 4:
            self.show_topics()
            print('show_topics')
        else:
            self.hide_calendar()

    def show_calendar(self):
        widgets.calendarWidget.setVisible(True)
        X_VALUE, Y_VALUE = 230, 205
        if self.slc_col == 3:
            X_VALUE = 250
        widgets.calendarWidget.move(X_VALUE, Y_VALUE+(self.slc_row*30))
        print(f'show calendar... {self.slc_row, self.slc_col}')

    def hide_calendar(self):
        widgets.calendarWidget.setVisible(False)

    def reset_calendar_date(self):
        self.slc_start_date = QDate.currentDate().toPython()
        self.slc_end_date = QDate.currentDate().toPython()
        print('reseting...')

    def calendar_date_changed(self):
        self.hide_calendar()
        print('the calendar date has changed! \n')

        if self.slc_col == 2:  #start_date cell
            self.slc_start_date = widgets.calendarWidget.selectedDate().toPython()
        elif self.slc_col == 3: # end_date cell
            self.slc_end_date = widgets.calendarWidget.selectedDate().toPython()
        else:
            print('None')

        print(f'new date: {self.slc_start_date}')
        item = widgets.tableWidget.item(self.slc_row, self.slc_col)
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