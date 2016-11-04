import Task

class TaskFactory(object):
    @staticmethod
    def create_task(priority, name, elapsed_time, boundary_time):
        return Task(priority, name, elapsed_time, boundary_time)
