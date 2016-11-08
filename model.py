class Task(object):
    def __init__(self, id, priority, name, elapsed_time, boundary_time):
        self.id = id
        self.priority = priority
        self.name = name
        self.elapsed_time = elapsed_time
        self.boundary_time = boundary_time

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_priority(self):
        return self.priority

    def get_elapsed_time(self):
        return self.elapsed_time

    def get_boundary_time(self):
        return self.boundary_time
