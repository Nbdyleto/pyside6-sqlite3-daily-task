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
            
    def update(self, update_list):

        new_data = []
        for new_value in update_list:
            new_data.append(new_value) 
        
        self.active_list = new_data[0]
        self.start_date = new_data[1]
        self.limit_date = new_data[2]
        self.name = new_data[3]
        self.checked = new_data[4]
    
    def serialize(self):
        return {
            'task_id' : self.id,
            'active_list' : self.active_list.topic,
            'start_time' : self.start_date,
            'end_time' : self.limit_date,
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
            with open('lists.json', 'w') as json_file:
                json.dump('', json_file)

    def load_tasks(self):
        self.instance_list = []
        self.no_instance_list = []
        self.no_instance_list = self.get_list()
        
        # Get first key (topic_name) for each list:
        list_keys = []
        for k in self.no_instance_list['lists']:
            key = next(iter(k)) 
            list_keys.append(key)
        
        # Instancing:
        task_id = 0
        for topic_id, result in enumerate(self.no_instance_list['lists']):
            items = result[list_keys[topic_id]] # items receive all items from specific list_key.
            self.create_list(list_keys[topic_id])   # create a list by the name of actual list_key
            # get each item (task), individually, and create instance from:
            for item in items:
                self.create_task(task_id, topic_id, item['start_time'], item['end_time'], item['name'])
            task_id += 1

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

    def create_task(self, task_id, topic_id, start_time, end_time, name):
        task = Task(task_id, self.instance_list[topic_id], start_time, end_time, name)
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
    
    def get_lists(self):
        return self.instance_list

    def change_data(self, topic_id, task_id, new_data):
        
        topic_list = self.instance_list[topic_id].serialize()
        for index, task in enumerate(topic_list['Math']):
            if str(task['task_id']) == task_id:
                print(f'Old task: {self.instance_list[topic_id].task_list[index].serialize()}')
                self.instance_list[topic_id].task_list[index].name = new_data
                print(f'New task: {self.instance_list[topic_id].task_list[index].serialize()}')

        self.update_json()