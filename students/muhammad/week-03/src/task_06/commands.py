from pydantic import BaseModel
import json



class ToDo(BaseModel):
    def add(self, task_name:str, expcted_time:float = 0.0):
        with open("data.json", 'r') as file:
            data = json.load(file)

        new_task = {
            'task_name': task_name,
            'expcted_time': expcted_time,
            'done': False
        }

        for task in data['tasks']:
            if task['task_name'] == new_task['task_name']:
                return 'Task already exists.'

        data['tasks'].append(new_task)

        with open("data.json", 'w') as file:
            json.dump(data, file, indent=4)
    
    def list(self):
        with open('data.json', 'r') as file:
            data = json.load(file)

        return data
    
    def done(self, task_name: str) -> bool:
        with open("data.json", 'r') as file:
            data = json.load(file)
        
        for task in data['tasks']:
            if task['task_name'] == task_name:
                task['done'] = True
                with open("data.json", 'w') as file:
                    json.dump(data, file, indent=4)
                return True
        return False

    def delete(self, task_name: str) -> bool:
        with open('data.json', 'r') as file:
            data = json.load(file)
        
        for i, task in enumerate(data['tasks']):
            if task['task_name'] == task_name:
                data['tasks'].pop(i)
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
                return True
        return False
