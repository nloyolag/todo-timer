import sys
from PyQt4 import QtGui, QtCore

minutes = 0
seconds = 0
mode = 0
alarm = QtGui.QSound("alarm.mp3")

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initInterface()

    def initInterface(self):
        centralwidget = QtGui.QWidget(self)
        self.lcd = QtGui.QLCDNumber(self)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)

        self.set = QtGui.QPushButton("Set", self)
        self.set.clicked.connect(self.Set)

        self.start = QtGui.QPushButton("Start", self)
        self.start.clicked.connect(self.Start)

        self.stop = QtGui.QPushButton("Stop", self)
        self.stop.clicked.connect(lambda: self.timer.stop())

        self.reset = QtGui.QPushButton("Reset", self)
        self.reset.clicked.connect(self.Reset)

        self.time = QtGui.QTimeEdit(self)
        self.time.setDisplayFormat("mm:ss")
        grid = QtGui.QGridLayout(self)

        grid.addWidget(self.start,1,0)
        grid.addWidget(self.stop,1,1)
        grid.addWidget(self.reset,1,2)
        grid.addWidget(self.time,2,0)
        grid.addWidget(self.set,2,1)
        grid.addWidget(self.lcd,3,0,1,3)

        centralwidget.setLayout(grid)

        self.setCentralWidget(centralwidget)
        self.setGeometry(300,300,280,170)

    def Set(self):
        global t, minutes, seconds, mode

        t = self.time.time()
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

        seconds = 0
        minutes = 0

        time = "{0}:{1}".format(minutes,seconds)
        self.lcd.display(time)

    def Start(self):
        global seconds, minutes, mode
        mode = 0
        self.timer.start(1000)

    def Time(self):
        global seconds, minutes, mode

        if mode == 0:
            if seconds < 59:
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
                alarm.play()
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
