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

def load_tasks():
    with open('tasks.csv', 'rb') as f:
        reader = csv.reader(f)
        tasks = list(reader)
    tasks = [Task(x[0], x[1], x[2], x[3]) for x in tasks]
    tasks.sort(key=lambda x: x.priority, reverse=True)
    task_iterator = TaskIterator(tasks)
    #TODO update interface

def create_task(priority, name, elapsed_time, boundary_time):
    task = TaskFactory.create_task(priority, name, elapsed_time, boundary_time)
    tasks.append(task)
    tasks.sort(key=lambda x: x.priority, reverse=True)
    task_iterator = TaskIterator(tasks)
    #TODO update interface

def alarm():
    pass

    
