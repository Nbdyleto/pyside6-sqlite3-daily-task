def change_data(self, item):
        row, col = item.row(), item.column()
        new_data_row, new_data_col = item.row(), item.column()
        new_data = item.text()
        print(f'new data: {item.text()} at pos {row, col}')
        print(f'new data: {item.text()} at pos {new_data_row, new_data_col}')

        topic_id = 0
        if (widgets.tableWidget.item(row, 1) == 'Math'):
        if (widgets.tableWidget.item(new_data_row, 1).text() == 'Math'):
            topic_id = 0
        elif (widgets.tableWidget.item(row, 1) == 'Geo'):
        elif (widgets.tableWidget.item(new_data_row, 1).text() == 'Geo'):
            topic_id = 1
        task_id = (widgets.tableWidget.item(row, 0)).text()
        new_data = (widgets.tableWidget.item(row, col)).text()

        self.main.change_data(topic_id, task_id, new_data)


        task_id = widgets.tableWidget.item(new_data_row, 0).text()
        new_data = widgets.tableWidget.item(new_data_row, new_data_col).text()

        if new_data_col == 0 or new_data_col == 1:
            print("can't change id or topic from this task!")
        else:
            self.main.change_data(topic_id, task_id, new_data, int(new_data_col))

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
                    print(it['task_id'], it['active_list'], it['start_date'], it['limit_date'], it['name'], '\n')
                    widgets.tableWidget.setItem(row, 0, QTableWidgetItem(str(it['task_id'])))
                    widgets.tableWidget.setItem(row, 1, QTableWidgetItem(it['active_list']))
                    widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['start_time']))
                    widgets.tableWidget.setItem(row, 3, QTableWidgetItem(it['end_time']))
                    widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['start_date']))
                    widgets.tableWidget.setItem(row, 3, QTableWidgetItem(it['limit_date']))
                    widgets.tableWidget.setItem(row, 4, QTableWidgetItem(it['name']))
                    row += 1
                elif ORDER == 'EACH_DAY':
                    if it['start_time'] == str(date):
                        print(it['task_id'], it['active_list'], it['start_time'], it['end_time'], it['name'], '\n')
                    if it['start_date'] == str(date):
                        print(it['task_id'], it['active_list'], it['start_date'], it['limit_date'], it['name'], '\n')
                        widgets.tableWidget.setItem(row, 0, QTableWidgetItem(it['active_list']))
                        widgets.tableWidget.setItem(row, 1, QTableWidgetItem(it['start_time']))
                        widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['end_time']))
                        widgets.tableWidget.setItem(row, 1, QTableWidgetItem(it['start_date']))
                        widgets.tableWidget.setItem(row, 2, QTableWidgetItem(it['limit_date']))
                        widgets.tableWidget.setItem(row, 3, QTableWidgetItem(it['name']))
                        row += 1