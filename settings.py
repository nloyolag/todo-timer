import csv

#####################################################
# Class: Singleton
# Description: Method that implements the Singleton
#              pattern, which is implemented by the
#              settings class.
#####################################################

class Singleton(object):
    instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_.instance, class_):
            class_.instance = object.__new__(class_, *args, **kwargs)
        return class_.instance

#####################################################
# Class: BaseSettings
# Description: Basic implementation of the settings.
#              It provides methods to load and
#              change settings from a CSV file.
#####################################################

class BaseSettings(object):
    def __init__(self):
        self.filename = "settings.csv"
        self.gui_color = ""
        self.default_timer = ""

    def load_settings(self):
        values = None
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f)
            values = list(reader)
        self.gui_color = values[0][0]
        self.default_timer = values[0][1]

    def change_settings(self, gui_color, default_timer):
        self.gui_color = gui_color
        self.default_timer = default_timer
        with open(self.filename, 'w') as f:
            f.write(gui_color + ',' + default_timer)

#####################################################
# Class: Settings
# Description: Class that inherits from the Singleton
#              and BaseSettings classes, becoming
#              a singleton and getting the settings
#              functionality.
#####################################################

class Settings(Singleton, BaseSettings):
    pass
