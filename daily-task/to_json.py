from asyncio import tasks
import json
import sqlite3

def serialize():

    db = sqlite3.connect('daily-task/data.db')
    cursor = db.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM topics").fetchone()

    results = cursor.execute("SELECT * FROM tasks")
    rows = [row for row in results]
    cols = [col[0] for col in results.description]
    tasks = []

    for row in rows:
        task = {}
        for field, value in zip(cols, row):
            task[field] = value
        tasks.append(task)

    with open('tasks.json', 'w') as json_file:
        json.dump(tasks, json_file, indent=4)
    

def import_to_json():
    pass

serialize()
