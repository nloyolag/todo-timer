from model import Task

class TaskIterator(class):
    def __init__(self, tasks):
        self.tasks = tasks
        self.length = len(tasks)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == self.length - 1:
            raise StopIteration
        self.index += 1
        return self.tasks[self.index]
