import sys
import controller
from datetime import datetime
from PyQt4 import QtGui, QtCore

t = 0
minutes = 0
seconds = 0
mode = 0
is_task = False
icon_key = {
    "High": "icons/high.png",
    "Medium": "icons/medium.png",
    "Low": "icons/low.png"
}

class AddTaskWindow(QtGui.QDialog):

    task_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.initInterface()

    def Submit(self):
        name = str(self.nameField.text())
        priority = str(self.priorityField.currentText())
        time = self.timeField.time().toString()
        elapsed_time = "00:00:00"
        controller.create_task(priority, name, elapsed_time, time)
        self.nameField.setText("")
        self.timeField.setTime(QtCore.QTime(0, 0, 0))
        self.priorityField.setCurrentIndex(0)
        self.task_signal.emit()
        self.close()

    def initInterface(self):
        self.nameField = QtGui.QLineEdit()
        self.priorityField = QtGui.QComboBox()
        self.priorityField.addItems(["High", "Medium", "Low"])
        self.timeField = QtGui.QTimeEdit(self)
        self.timeField.setDisplayFormat("mm:ss")
        self.submit = QtGui.QPushButton("Submit Task", self)
        self.submit.clicked.connect(self.Submit)
        self.formLayout = QtGui.QFormLayout()

        self.formLayout.addRow("Name", self.nameField)
        self.formLayout.addRow("Priority", self.priorityField)
        self.formLayout.addRow("Task Time", self.timeField)
        self.formLayout.addRow("", self.submit)

        self.setLayout(self.formLayout)
        self.setGeometry(300,300,780,670)

class EditTaskWindow(QtGui.QDialog):

    task_signal = QtCore.pyqtSignal()

    def __init__(self, task):
        QtGui.QDialog.__init__(self)
        self.task = task
        self.initInterface()

    def Submit(self):
        id = str(self.task.id)
        name = str(self.nameField.text())
        priority = str(self.priorityField.currentText())
        time = self.timeField.time().toString()
        elapsed_time = "00:00:00"
        controller.edit_task(id, priority, name, elapsed_time, time)
        self.task_signal.emit()
        self.close()

    def initInterface(self):
        self.nameField = QtGui.QLineEdit()
        self.priorityField = QtGui.QComboBox()
        self.priorityField.addItems(["High", "Medium", "Low"])
        self.timeField = QtGui.QTimeEdit(self)
        self.timeField.setDisplayFormat("mm:ss")
        self.submit = QtGui.QPushButton("Submit Task", self)
        self.submit.clicked.connect(self.Submit)
        self.formLayout = QtGui.QFormLayout()

        task_time = datetime.strptime(self.task.boundary_time,"%H:%M:%S")
        hours = 0
        minutes = task_time.minute
        seconds = task_time.second
        self.nameField.setText(self.task.name)
        self.timeField.setTime(QtCore.QTime(hours, minutes, seconds))
        priority = self.priorityField.findText(self.task.priority)
        self.priorityField.setCurrentIndex(priority)

        self.formLayout.addRow("Name", self.nameField)
        self.formLayout.addRow("Priority", self.priorityField)
        self.formLayout.addRow("Task Time", self.timeField)
        self.formLayout.addRow("", self.submit)

        self.setLayout(self.formLayout)
        self.setGeometry(300,300,480,270)

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initInterface()

    def updateTasks(self):
        self.list.clear()
        tasks = controller.load_tasks()
        self.items = []
        for task in tasks:
            item = QtGui.QListWidgetItem(
                QtGui.QIcon(icon_key[task.priority]),
                task.name + " - Elapsed Time: " + task.elapsed_time,
                self.list
            )
            item.setData(QtCore.Qt.UserRole, task)
            self.items.append(item)

    def deleteTask(self):
        item = self.list.currentItem()
        data = item.data(QtCore.Qt.UserRole).toPyObject()
        controller.delete_task(data)
        self.updateTasks()

    def populateActiveTask(self):
        item = self.list.currentItem()
        data = item.data(QtCore.Qt.UserRole).toPyObject()
        task_time = datetime.strptime(data.boundary_time,"%H:%M:%S")
        hours = 0
        minutes = task_time.minute
        seconds = task_time.second
        self.taskName.setText(data.name)
        self.taskTime.setTime(QtCore.QTime(hours, minutes, seconds))

    def callEditWindow(self):
        item = self.list.currentItem()
        data = item.data(QtCore.Qt.UserRole).toPyObject()
        edit_task_window = EditTaskWindow(data)
        edit_task_window.task_signal.connect(self.updateTasks)
        edit_task_window.exec_()

    def initInterface(self):
        centralwidget = QtGui.QWidget(self)
        self.lcd = QtGui.QLCDNumber(self)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)

        self.countdownInput = QtGui.QPushButton("Countdown with Input", self)
        self.countdownInput.clicked.connect(lambda: self.Countdown("input"))
        self.countdownTask = QtGui.QPushButton("Countdown with Task time", self)
        self.countdownTask.clicked.connect(lambda: self.Countdown("task"))

        self.timerUnlimited = QtGui.QPushButton("Start Unlimited Timer", self)
        self.timerUnlimited.clicked.connect(lambda: self.Timer("unlimited"))
        self.timerTask = QtGui.QPushButton("Start Task Timer", self)
        self.timerTask.clicked.connect(lambda: self.Timer("task"))

        self.stop = QtGui.QPushButton("Stop", self)
        self.stop.clicked.connect(lambda: self.timer.stop())
        self.start = QtGui.QPushButton("Continue", self)
        self.start.clicked.connect(lambda: self.timer.start())

        self.create_task = QtGui.QPushButton("Add Task", self)
        self.add_task_window = AddTaskWindow()
        self.add_task_window.task_signal.connect(self.updateTasks)
        self.create_task.clicked.connect(lambda: self.add_task_window.exec_())
        self.delete_task = QtGui.QPushButton("Delete or Complete Task", self)
        self.delete_task.clicked.connect(lambda: self.deleteTask())
        self.edit_task = QtGui.QPushButton("Edit Task", self)
        self.edit_task.clicked.connect(lambda: self.callEditWindow())

        self.reset = QtGui.QPushButton("Reset", self)
        self.reset.clicked.connect(self.Reset)

        self.list = QtGui.QListWidget()
        self.list.currentItemChanged.connect(self.populateActiveTask)
        self.updateTasks()

        self.countdownTime = QtGui.QTimeEdit(self)
        self.countdownTime.setDisplayFormat("mm:ss")

        self.taskName = QtGui.QLineEdit(self)
        self.taskName.setEnabled(False)
        self.taskTime = QtGui.QTimeEdit(self)
        self.taskTime.setDisplayFormat("mm:ss")
        self.taskTime.setEnabled(False)

        grid = QtGui.QGridLayout(self)

        grid.addWidget(QtGui.QLabel("General Controls: "),1,0)
        grid.addWidget(self.reset,1,1)
        grid.addWidget(self.stop,1,2)
        grid.addWidget(self.start,1,3)
        grid.addWidget(QtGui.QLabel("Timer Controls: "),2,0)
        grid.addWidget(self.timerUnlimited,2,1)
        grid.addWidget(self.timerTask,2,2)
        grid.addWidget(QtGui.QLabel("Countdown Controls: "),3,0)
        grid.addWidget(self.countdownTime,3,1)
        grid.addWidget(self.countdownInput,3,2)
        grid.addWidget(self.countdownTask,3,3)
        grid.addWidget(QtGui.QLabel("Selected Task: "),4,0)
        grid.addWidget(self.taskName,4,1)
        grid.addWidget(self.taskTime,4,2)
        grid.addWidget(self.lcd,5,0,1,4)
        grid.setRowMinimumHeight(5,150)
        grid.addWidget(self.create_task,6,0)
        grid.setRowMinimumHeight(6,200)
        grid.addWidget(self.list,6,1,3,4)
        grid.addWidget(self.edit_task,7,0)
        grid.addWidget(self.delete_task,8,0)

        centralwidget.setLayout(grid)

        self.setCentralWidget(centralwidget)
        self.setGeometry(300,300,780,670)

    def Countdown(self, method):
        global t, minutes, seconds, mode, is_task

        self.list.setEnabled(False)

        if method == "input":
            t = self.countdownTime.time()
            is_task = False
        elif method == "task":
            t = self.taskTime.time()
            is_task = True

        self.lcd.display(t.toString())
        self.timer.start(1000)

        minutes = t.minute()
        seconds = t.second()
        mode = 1
        time = "{0}:{1}".format(minutes,seconds)
        self.lcd.display(time)

    def Reset(self):
        global seconds, minutes

        self.timer.stop()
        self.list.setEnabled(True)

        seconds = 0
        minutes = 0

        time = "{0}:{1}".format(minutes,seconds)
        self.lcd.display(time)

    def Timer(self, method):
        global seconds, minutes, mode, t, is_task

        self.list.setEnabled(False)

        if method == "unlimited":
            t = None
            is_task = False
        elif method == "task":
            t = self.taskTime.time()
            is_task = True

        mode = 0
        self.timer.start(1000)

    def Time(self):
        global seconds, minutes, mode, t, is_task

        if is_task:
            item = self.list.currentItem()
            data = item.data(QtCore.Qt.UserRole).toPyObject()
            task_time = datetime.strptime(str(data.elapsed_time),"%H:%M:%S")
            task_time = QtCore.QTime(0, task_time.minute, task_time.second)
            task_time = task_time.addSecs(1)
            data.elapsed_time = task_time.toString()
            item.setText(data.name + " - Elapsed Time: " + data.elapsed_time)
            item.setData(QtCore.Qt.UserRole, data)
            controller.edit_task(
                data.id,
                data.priority,
                data.name,
                data.elapsed_time,
                data.boundary_time
            )

        if mode == 0:
            if t and minutes == t.minute() and seconds == t.second():
                self.timer.stop()
                stop = QtGui.QMessageBox.warning(self,"Game Over!","Game Over!")
                self.list.setEnabled(True)
            elif seconds < 59:
                seconds += 1
            else:
                minutes += 1
                seconds = 0
        elif mode == 1:
            if seconds > 0:
                seconds -= 1
            elif minutes == 0 and seconds == 0:
                self.timer.stop()
                stop = QtGui.QMessageBox.warning(self,"Game Over!","Game Over!")
                self.list.setEnabled(True)
            else:
                minutes -= 1
                seconds = 59

        time = "{0}:{1}".format(minutes,seconds)

        self.lcd.display(time)

def main():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
