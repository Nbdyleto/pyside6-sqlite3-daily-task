import json
import sqlite3

class DataBase:
    __DB_LOCATION = 'daily-task/data.db'
    def __init__(self):
        self.conn = sqlite3.connect(__DB_LOCATION)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.cursor.close()
     
    def execute(self, row):
        self.cursor.execute(row)

# Create a ImportExport class to do this.

def export_to_json():

    db = sqlite3.connect('daily-task/data.db')
    cursor = db.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM topics").fetchone()

    tasks = []
    for i in range(count[0]):
        # Order tasks by topic_id

        results = cursor.execute(f"SELECT * FROM tasks WHERE topic_id = {i}")

        rows = [row for row in results]

        cols = [col[0] for col in results.description]
        for row in rows:
            task = {}
            for field, value in zip(cols, row):
                task[field] = value
            tasks.append(task)

    print(tasks)

    with open('tasks.json', 'w') as json_file:
        json.dump(tasks, json_file, indent=4)
    
def import_to_json():
    # https://www.alixaprodev.com/2022/03/convert-json-to-sqlite-database-in-python.html
    pass

export_to_json()
