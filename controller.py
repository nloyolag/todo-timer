# Unlimited Stopwatch
# Stopwatch with upper limit
# Countdown with user input
# Countdown with task time

import csv
from iterator import TaskIterator
from model import Task
from factory import TaskFactory
from settings import Settings

tasks = []
task_iterator = None
priority_mapper = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

def load_tasks():
    with open('tasks.csv', 'rb') as f:
        reader = csv.reader(f)
        tasks = list(reader)
    tasks = [Task(x[0], x[1], x[2], x[3], x[4]) for x in tasks]
    tasks.sort(key=lambda x: priority_mapper[x.priority])
    task_iterator = TaskIterator(tasks)
    return tasks

def create_task(priority, name, elapsed_time, boundary_time):
    tasks = load_tasks()
    id = len(tasks) + 1
    task = TaskFactory.create_task(id, priority, name, elapsed_time, boundary_time)
    tasks.sort(key=lambda x: priority_mapper[x.priority])
    task_iterator = TaskIterator(tasks)

def delete_task(task):
    tasks = load_tasks()
    for elem in tasks:
        if elem.id == task.id:
            task = elem
            break
    tasks.remove(task)
    tasks.sort(key=lambda x: x.id)
    for idx, elem in enumerate(tasks):
        new = elem
        new.id = idx + 1
        tasks[idx] = new
    with open('tasks.csv', 'w') as f:
        for task in tasks:
            line = str(task.id) + ',' + str(task.priority) + ',' + str(task.name) + ',' + str(task.elapsed_time) + ',' + str(task.boundary_time) + '\n'
            f.write(line)

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
