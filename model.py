class Task(object):
    def __init__(self, priority, name, elapsed_time, boundary_time):
        self.priority = priority
        self.name = name
        self.elapsed_time = elapsed_time
        self.boundary_time = boundary_time

    def get_name(self):
        return self.name

    def get_elapsed_time(self):
        return self.elapsed_time

    def get_boundary_time(self):
        return self.boundary_time
