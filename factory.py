from model import Task

#####################################################
# Class: TaskFactory
# Description: Implements the factory pattern,
#              providing a standarized class for
#              object creation.
#####################################################

class TaskFactory(object):
    @staticmethod
    def create_task(id, priority, name, elapsed_time, boundary_time):
        with open('tasks.csv', 'a') as f:
            line = str(id) + ',' + str(priority) + ',' + str(name) + ',' + str(elapsed_time) + ',' + str(boundary_time) + '\n'
            f.write(line)
        return Task(id, priority, name, elapsed_time, boundary_time)
