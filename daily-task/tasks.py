import json
import os.path

class Task:
    def __init__(self, id, active_list, start_date, limit_date, name, checked=False):
        self.id = id
        self.active_list = active_list
        self.start_date = start_date
        self.limit_date = limit_date
        self.name = name
        self.checked = checked
    
    def start(self):
        pass
    
    def end(self):
        pass

    def check(self):
        pass
    
    def serialize(self):
        return {
            'task_id' : self.id,
            'active_list' : self.active_list.topic,
            'start_date' : self.start_date,
            'limit_date' : self.limit_date,
            'name' : self.name,
            'checked' : self.checked
        }

class TaskList:
    def __init__(self, task_list=[], topic=None, color=None):
        self.task_list = task_list
        self.topic = topic
        self.color = color

    def add_task(self, task):
        self.task_list.append(task)  

    def serialize(self):
        return {
            self.topic : self.to_json()
        }
    
    def to_json(self):
        task_list_ = []
        for task in self.task_list:
            task_list_.append(task.serialize())
        return task_list_

class Main:
    def __init__(self):
        try:
            self.load_tasks()
        except Exception:
            print('not')
            with open('lists.json', 'w') as json_file:
                json.dump('', json_file)

    def load_tasks(self):
        self.instance_list = []
        self.no_instance_list = self.get_list()
        
        # Get first key (topic_name) for each list:
        list_keys = []
        for k in self.no_instance_list['lists']:
            key = next(iter(k)) 
            list_keys.append(key)
        
        # Instancing:
        for topic_id, result in enumerate(self.no_instance_list['lists']):
            items = result[list_keys[topic_id]] # items receive all items from specific list_key.
            self.create_list(list_keys[topic_id])   # create a list by the name of actual list_key
            # get each item (task), individually, and create instance from:
            for item in items:
                task_id = item['task_id']
                self.create_task(task_id, topic_id, item['start_date'], item['limit_date'], item['name'])

        self.update_json()

    def get_list(self):
        """From Json File"""
        no_instance_list_ = []
        with open('lists.json', 'r') as json_file:
            active_topics = json.load(json_file)
            no_instance_list_ = active_topics
        return no_instance_list_

    def create_list(self, topic_name):
        task_list = TaskList([], topic_name)
        self.instance_list.append(task_list)
        self.update_json()

    def create_task(self, task_id, topic_id, start_date, limit_date, name):
        task = Task(task_id, self.instance_list[topic_id], start_date, limit_date, name)
        self.instance_list[topic_id].add_task(task)
        self.update_json()

    def update_json(self):  
        with open('lists.json', 'w') as json_file:
            json.dump(self.serialize(), json_file, indent=2)

    def serialize(self):
        return {
            'lists': self.to_json()
        }

    def to_json(self):
        instance_list_ = []
        for task in self.instance_list:
            instance_list_.append(task.serialize())
        return instance_list_

    def change_data(self, topic_id, task_id, new_data, new_data_col):
        topic_list = self.instance_list[topic_id].serialize()
        topic_name = list(topic_list.keys())[0]
        for index, task in enumerate(topic_list[topic_name]):
            if str(task['task_id']) == task_id:
                
                print(f'Old task: {self.instance_list[topic_id].task_list[index].serialize()}')
                if new_data_col == 2:
                    self.instance_list[topic_id].task_list[index].start_date = new_data
                elif new_data_col == 3:
                    self.instance_list[topic_id].task_list[index].limit_date = new_data
                elif new_data_col == 4:
                    self.instance_list[topic_id].task_list[index].name = new_data
                print(f'New task: {self.instance_list[topic_id].task_list[index].serialize()}\n')
        self.update_json()