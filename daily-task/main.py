from PySide6.QtWidgets import QWidget, QApplication, QListWidgetItem, QTableWidgetItem, QMessageBox, QCheckBox
from PySide6.QtCore import QDate
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

        """
        self.main.create_list('Math')
        self.main.create_task(0, str(QDate(2022, 8, 10).toPython()), '0', 'Do some exercises')
        self.main.create_task(0, str(QDate(2022, 8, 11).toPython()), '1', 'Study Functions')
        self.main.create_task(0, str(QDate(2022, 8, 11).toPython()), '2', 'Solve problems')
        self.main.create_list('Geo')
        self.main.create_task(1, str(widgets.calendarWidget.selectedDate().toPython()), '3', 'Study Rain')

        self.main.create_task(0, str(QDate(2022, 8, 10).toPython()), '1', 'Study Math')
        self.main.create_task(0, str(QDate(2022, 8, 12).toPython()), '2', 'Solve Calcule III')

        self.main.create_task(1, str(widgets.calendarWidget.selectedDate().toPython()), '3', 'Study Geopolitcs')
        """

        self.main.update_json()

        self.calendarDateChanged()

        widgets.calendarWidget.selectionChanged.connect(self.calendarDateChanged)

        #self.saveButton.clicked.connect(self.saveChanges)
        #self.addButton.clicked.connect(self.addNewTask)

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
                    print(row, it['active_list'], it['start_time'], it['end_time'], it['name'], '\n')
                    widgets.tableWidget.setItem(row, 0, QTableWidgetItem(it['active_list']))
                    widgets.tableWidget.setItem(row, 1, QTableWidgetItem(it['start_time']))
                    widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['end_time']))
                    widgets.tableWidget.setItem(row, 3, QTableWidgetItem(it['name']))
                    row += 1
                elif ORDER == 'EACH_DAY':
                    if it['start_time'] == str(date):
                        print(row, it['active_list'], it['start_time'], it['end_time'], it['name'], '\n')
                        widgets.tableWidget.setItem(row, 0, QTableWidgetItem(it['active_list']))
                        widgets.tableWidget.setItem(row, 1, QTableWidgetItem(it['start_time']))
                        widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['end_time']))
                        widgets.tableWidget.setItem(row, 3, QTableWidgetItem(it['name']))
                        row += 1
                    
    def updateTaskList(self, date):
        widgets.tasksListWidget.clear()
            
        with open('lists.json', 'r') as json_file:
            results = json.load(json_file)
    
        first_keys = []
        for l in results['lists']:
            first_key = next(iter(l))   # Get the first key for a list
            first_keys.append(first_key)

        for index, result in enumerate(results['lists']):
            items = result[first_keys[index]] # items receive all items from specific list_key.
            for it in items:
                if (it['start_time'] == str(date)):
                    print(it['active_list'], it['start_time'], it['end_time'], it['name'], '\n')
                    item = QListWidgetItem(f"{it['active_list']} - {it['name']}")
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    if it['checked'] == True:
                        item.setCheckState(Qt.Checked)
                    elif it['checked'] == False:
                        item.setCheckState(Qt.Unchecked)
                    widgets.tasksListWidget.addItem(item)
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
    window.show()
    sys.exit(app.exec())