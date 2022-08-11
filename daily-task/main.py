from PySide6.QtWidgets import QWidget, QApplication, QListWidgetItem, QTableWidgetItem, QMessageBox, QCheckBox
from PySide6.QtCore import QDate, QPoint
from PySide6.QtGui import QBrush, QColor
from matplotlib import widgets
from ui_main import Ui_Form
import sys

#from qtconsole.qt import QtCore

import json
from tasks import *

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

        self.main = Main()

        
        self.main.create_list('Math')
        self.main.create_task(0, 0, str(QDate(2022, 8, 10).toPython()), str(QDate(2022, 8, 13).toPython()), 'Do some exercises')
        self.main.create_task(1, 0, str(QDate(2022, 8, 11).toPython()), str(QDate(2022, 8, 15).toPython()), 'Study Functions')
        self.main.create_task(2, 0, str(QDate(2022, 8, 11).toPython()), str(QDate(2022, 8, 17).toPython()), 'Solve problems')
        self.main.create_list('Geo')
        self.main.create_task(3, 1, str(widgets.calendarWidget.selectedDate().toPython()), str(QDate(2022, 8, 17).toPython()), 'Study Rain')

        self.main.create_task(4, 0, str(QDate(2022, 8, 10).toPython()), str(QDate(2022, 8, 12).toPython()), 'Study Math')
        self.main.create_task(5, 0, str(QDate(2022, 8, 12).toPython()), str(QDate(2022, 8, 17).toPython()), 'Solve Calcule III')

        self.main.create_task(6, 1, str(widgets.calendarWidget.selectedDate().toPython()), str(QDate(2022, 8, 19).toPython()), 'Study Geopolitcs')
        
        self.main.update_json()

        self.calendarDateChanged()

        widgets.calendarWidget.selectionChanged.connect(self.calendarDateChanged)

        #widgets.tableWidget.cellClicked.connect(self.event_test)
        widgets.tableWidget.itemChanged.connect(self.change_data)

    def event_test(self, row, col):
        print(row, col)
        item = widgets.tableWidget.item(row, col)
        print(item.text())

    def change_data(self, item):
        row, col = item.row(), item.column()
        print(f'new data: {item.text()} at pos {row, col}')
        task_id = (widgets.tableWidget.item(row, 0)).text()

        with open('lists.json', 'r') as json_file:
            results = json.load(json_file)

        first_keys = []
        for l in results['lists']:
            first_key = next(iter(l))   # Get the first key for a list
            first_keys.append(first_key)

        for index, result in enumerate(results['lists']):
            items = result[first_keys[index]] # items receive all items from specific list_key.
            widgets.tableWidget.setRowCount(15) # [ ] Set a valid row count...
            for it in items:
                if it['task_id'] == int(task_id):
                    pass

        
        #self.main.update_json()

    global ORDER
    ORDER = ['ALL_TASKS', 'EACH_DAY']
    def calendarDateChanged(self):
        print('the calendar date has changed! \n')
        date_selected = widgets.calendarWidget.selectedDate().toPython()
        print(f'date: {date_selected}')
        self.updateTableWidget(date_selected, ORDER[0])

    # PySide6.QtCore.QDate(2022, 8, 10)

    def updateTableWidget(self, date, ORDER):
        widgets.tableWidget.clear()

        with open('lists.json', 'r') as json_file:
            results = json.load(json_file)

        first_keys = []
        for l in results['lists']:
            first_key = next(iter(l))   # Get the first key for a list
            first_keys.append(first_key)

        row = 0
        for index, result in enumerate(results['lists']):
            items = result[first_keys[index]] # items receive all items from specific list_key.
            widgets.tableWidget.setRowCount(15) # [ ] Set a valid row count...
            for it in items:
                if ORDER == 'ALL_TASKS':
                    print(it['task_id'], it['active_list'], it['start_time'], it['end_time'], it['name'], '\n')
                    widgets.tableWidget.setItem(row, 0, QTableWidgetItem(str(it['task_id'])))
                    widgets.tableWidget.setItem(row, 1, QTableWidgetItem(it['active_list']))
                    widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['start_time']))
                    widgets.tableWidget.setItem(row, 3, QTableWidgetItem(it['end_time']))
                    widgets.tableWidget.setItem(row, 4, QTableWidgetItem(it['name']))
                    row += 1
                elif ORDER == 'EACH_DAY':
                    if it['start_time'] == str(date):
                        print(it['task_id'], it['active_list'], it['start_time'], it['end_time'], it['name'], '\n')
                        widgets.tableWidget.setItem(row, 0, QTableWidgetItem(it['active_list']))
                        widgets.tableWidget.setItem(row, 1, QTableWidgetItem(it['start_time']))
                        widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['end_time']))
                        widgets.tableWidget.setItem(row, 3, QTableWidgetItem(it['name']))
                        row += 1
"""
    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()
    

    def addNewTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        newTask = str(self.taskLineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)

        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setStyleSheet('background-color: #282a36;')
    window.show()
    sys.exit(app.exec())