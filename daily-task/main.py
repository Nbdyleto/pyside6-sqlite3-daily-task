from PySide6.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
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

        self.main = Main()

        self.main.update_json()

        self.calendarDateChanged()

        widgets.calendarWidget.selectionChanged.connect(self.calendarDateChanged)

        #self.saveButton.clicked.connect(self.saveChanges)
        #self.addButton.clicked.connect(self.addNewTask)

    def calendarDateChanged(self):
        print('the calendar date has changed! \n')
        date_selected = widgets.calendarWidget.selectedDate().toPython()
        print(f'date: {date_selected}')
        self.updateTaskList(date_selected)

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