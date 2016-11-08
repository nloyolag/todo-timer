import csv
from iterator import TaskIterator
from model import Task
from factory import TaskFactory
from settings import Settings

settings = Settings()

#####################################################
# Controller file
# Description: File that implements the controller,
#              providing methods that interact with
#              the model and send results to the
#              view.
#####################################################

tasks = []
task_iterator = None
priority_mapper = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

#####################################################
# Method: load_tasks
# Description: Method that loads the tasks from
#              the model using the TaskIterator.
#####################################################

def load_tasks():
    with open('tasks.csv', 'rb') as f:
        reader = csv.reader(f)
        tasks = list(reader)
    tasks = [Task(x[0], x[1], x[2], x[3], x[4]) for x in tasks if x[0] != "-1"]
    tasks.sort(key=lambda x: priority_mapper[x.priority])
    task_iterator = TaskIterator(tasks)
    return tasks

#####################################################
# Method: create_task
# Description: Method that creates a new task
#              using the TaskFactory.
#####################################################

def create_task(priority, name, elapsed_time, boundary_time):
    tasks = load_tasks()
    id = len(tasks) + 1
    task = TaskFactory.create_task(id, priority, name, elapsed_time, boundary_time)
    tasks.sort(key=lambda x: priority_mapper[x.priority])
    task_iterator = TaskIterator(tasks)

#####################################################
# Method: delete_task
# Description: Method that deletes a task based
#              on its id and updates the model.
#####################################################

def delete_task(task):
    tasks = load_tasks()
    for elem in tasks:
        if elem.id == task.id:
            task = elem
            break
    tasks.remove(task)
    tasks.sort(key=lambda x: x.id)
    for idx, elem in enumerate(tasks):
        if elem.id != -1:
            new = elem
            new.id = idx + 1
            tasks[idx] = new
    with open('tasks.csv', 'w') as f:
        for task in tasks:
            line = str(task.id) + ',' + str(task.priority) + ',' + str(task.name) + ',' + str(task.elapsed_time) + ',' + str(task.boundary_time) + '\n'
            f.write(line)

#####################################################
# Method: complete_task
# Description: Method that deactivates a task based
#              on its id and updates the model.
#####################################################

def complete_task(task):
    tasks = load_tasks()
    loc = 0
    for idx, elem in enumerate(tasks):
        if elem.id == task.id:
            loc = idx
            break

    tasks[loc].id = -1
    with open('tasks.csv', 'w') as f:
        for task in tasks:
            line = str(task.id) + ',' + str(task.priority) + ',' + str(task.name) + ',' + str(task.elapsed_time) + ',' + str(task.boundary_time) + '\n'
            f.write(line)

#####################################################
# Method: edit_task
# Description: Method that edits the fields of a task
#              based on its id.
#####################################################

def edit_task(id, priority, name, elapsed_time, boundary_time):
    tasks = load_tasks()
    loc = 0
    for idx, elem in enumerate(tasks):
        if elem.id == id:
            loc = idx
            break

    task = TaskFactory.create_task(id, priority, name, elapsed_time, boundary_time)
    tasks[idx] = task
    with open('tasks.csv', 'w') as f:
        for task in tasks:
            line = str(task.id) + ',' + str(task.priority) + ',' + str(task.name) + ',' + str(task.elapsed_time) + ',' + str(task.boundary_time) + '\n'
            f.write(line)

#####################################################
# Method: get_color
# Description: Method that gets the color from the
#              settings.
#####################################################

def get_color():
    return settings.get_color()

#####################################################
# Method: change_settings
# Description: Method that edits the fields of a task
#              based on its id.
#####################################################

# Example of Adapter pattern. Given that the view cannot
# interact directly with the logic, this adapter provides
# a gateway to a method of the settings class.
def change_settings(color):
    settings.change_settings(color)
