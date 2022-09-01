import json
import sqlite3

#https://codereview.stackexchange.com/questions/182700/python-class-to-manage-a-table-in-sqlite

class DailyTaskDB:
    __DB_LOCATION = 'daily-task/tasks_db_operations.db'

    def __init__(self):
        self.conn = sqlite3.connect(DailyTaskDB.__DB_LOCATION)
        self.cursor = self.conn.cursor()

    # Context Manager Capabilities

    def __enter__(self):
        return self
    
    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def __del__(self):
        self.conn.close()

    # DB Functions 

    def create_tables(self):

        # Child Table
        self.cursor.execute("DROP TABLE IF EXISTS tasks")
        qry_tasks = """ CREATE TABLE tasks (
            task_name VARCHAR(255) NOT NULL, 
            status VARCHAR(255) NOT NULL,
            start_date DATE NOT NULL,
	        end_date DATE NOT NULL,	
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
            	REFERENCES topics (topic_id)
        );"""
        self.cursor.execute(qry_tasks)
        print('table tasks is ready!')
        
        # Parent Table
        self.cursor.execute("DROP TABLE IF EXISTS topics")
        qry_topics = """ CREATE TABLE topics (
            topic_id INTEGUER PRIMARY KEY,
            topic_name VARCHAR(255) NOT NULL
        );"""
        self.cursor.execute(qry_topics)
        print('table topics is ready!')

        poptbl = """INSERT INTO topics (topic_id, topic_name) VALUES (0, '');"""
        self.execute(poptbl)
        poptbl = """INSERT INTO topics (topic_id, topic_name) VALUES (1, 'Geo');"""
        self.execute(poptbl)
        poptbl = """INSERT INTO topics (topic_id, topic_name) VALUES (2, 'Math');"""
        self.execute(poptbl)
        poptbl = """INSERT INTO topics (topic_id, topic_name) VALUES (3, 'Chemistry');"""
        self.execute(poptbl)

    def execute(self, qry):
        self.cursor.execute(qry)
        self.conn.commit()
        
        #self.topics = self.cursor.execute("SELECT * FROM topics").fetchall()
    