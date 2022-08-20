# https://www.sqlitetutorial.net/sqlite-foreign-key/

def create_table(self):
        db = sqlite3.connect('daily-task/data.db')
        cursor = db.cursor()

        cursor.execute('DROP TABLE IF EXISTS TASKS')

        # Child Table
        tbl_tasks = """ CREATE TABLE tasks (
            task_name VARCHAR(255) NOT NULL, 
            completed VARCHAR(255) NOT NULL,
            start_date VARCHAR(15) NOT NULL,
	    end_date VARCHAR(10) NOT NULL,	
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
            	REFERENCES topics (topic_id)
            	ON DELETE SET NULL
        );"""
        
        # Parent Table:
        tbl_topics = """ CREATE TABLE topics (
            topic_id INTEGUER PRIMARY KEY
            topic_name VARCHAR(255) NOT NULL,
            color VARCHAR(7) NOT NULL,
        )    
        """
        
        cursor.execute(tbl_tasks)
        print('table_tasks is ready!')
        
        cursor.execute(tbl_topics)
        print('table_topics is ready!')
		
		#2020/12/05
