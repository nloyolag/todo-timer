class Task(object):
    def __init__(self, name, priority, elapsed_time, boundary_time):
        self.name = name
        self.priority = priority
        self.elapsed_time = elapsed_time
        self.boundary_time = boundary_time
