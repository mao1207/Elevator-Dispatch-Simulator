from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer

from elevatorUI import *
import numpy as np
import time, threading
import numpy as np
from functools import partial

# Create elevator class
class Elevator:
    def __init__(self, no, Elev):
        self.no = no
        self.floor = 1
        self.damage = False
        self.open = False
        self.number = 0
        self.move = 1
        self.target = 1
        self.goal = []
        self.elev = Elev
        self.prior = []

        self.close_timer = QTimer()
        self.close_timer.timeout.connect(self.closeDoor_Anim)
        self.stop_timer = QTimer()
        self.stop_timer.timeout.connect(self.stop_Anim)


    # Elevator movement function
    def moving(self):
        if len(self.goal) != 0:
            if self.floor == self.goal[0] and self.open == False:
                self.target = self.goal.pop(0)
                button = self.elev.findChild(QtWidgets.QPushButton, "button " + str(self.no) + ' ' + str(self.floor))
                button.setStyleSheet("background-color: rgb(200, 200, 200);")
                self.open = True
                self.elev.open[self.floor - 1][self.no] = 1
                index = 0
                if self.elev.floor == self.floor:
                    self.openDoor_Anim()
                else:
                    self.stop_timer.start(3000)
                if self.move == 1 and len(self.goal) != 0:
                    index = 0
                elif self.move == -1 and len(self.goal) != 0:
                    index = 1
                else:
                    if self.elev.pressed[self.floor - 1][0] == 1:
                        index = 0
                    elif self.elev.pressed[self.floor - 1][1] == 1:
                        index = 1
                self.elev.pressed[self.floor - 1][index] = 0
                self.elev.request[self.elev.floor - 1][index] = -1

            else:
                self.target = self.goal[0]
        else:
            self.move = 0
            self.elev.stateshow[self.no].setStyleSheet(
                "QGraphicsView{border-image: url(../Resources/Button/state.png)}")
            if len(self.prior) != 0:
                self.prior.sort(reverse=(self.prior[0] < self.floor))
                self.goal = self.prior
                self.prior = []

        self.elev.open_button[self.no].setEnabled(True)
        self.elev.close_button[self.no].setEnabled(True)
        if self.open == False:
            self.update_elevator_position()

    # Update the state of elevators
    def update_elevator_position(self):
        if self.floor > self.target:
            self.elev.open_button[self.no].setEnabled(False)
            self.elev.close_button[self.no].setEnabled(False)
            self.elev.stateshow[self.no].setStyleSheet(
                "QGraphicsView{border-image: url(../Resources/Button/state_down.png)}")
            self.floor -= 1
            self.move = -1
        elif self.floor < self.target:
            self.elev.open_button[self.no].setEnabled(False)
            self.elev.close_button[self.no].setEnabled(False)
            self.elev.stateshow[self.no].setStyleSheet(
                "QGraphicsView{border-image: url(../Resources/Button/state_up.png)}")
            self.floor += 1
            self.move = 1

        self.elev.lcd_number[self.no].setProperty("value", self.floor)
        self.elev.lcd_number_floor[self.no].setProperty("value", self.floor)

    # Update the status after pressing the button
    def press_button(self, floor):
        if floor == self.floor:
            return 0

        else:
            button = self.elev.findChild(QtWidgets.QPushButton, "button " + str(self.no) + ' ' + str(floor))
            button.setStyleSheet("background-color: orange;")
            if (floor - self.floor) * self.move > 0 or self.move == 0:
                if floor not in self.goal:
                    self.goal.append(floor)
                self.goal.sort(reverse=(self.move==-1))

            else:
                if floor not in self.prior:
                    self.prior.append(floor)

    # Play the door opening animation
    def openDoor_Anim(self):
        self.elev.elevator_Anim[2 * self.no].setDirection(QAbstractAnimation.Forward)  # 正向设定动画
        self.elev.elevator_Anim[2 * self.no + 1].setDirection(QAbstractAnimation.Forward)
        self.elev.elevator_Anim[2 * self.no].start()  # 开始播放
        self.elev.elevator_Anim[2 * self.no + 1].start()

    # Play the door closing animation
    def closeDoor_Anim(self):
        self.elev.elevator_Anim[2 * self.no].setDirection(QAbstractAnimation.Backward)  # 反向设定动画
        self.elev.elevator_Anim[2 * self.no + 1].setDirection(QAbstractAnimation.Backward)
        self.elev.elevator_Anim[2 * self.no].start()  # 开始播放
        self.elev.elevator_Anim[2 * self.no + 1].start()

    # Animation pause
    def stop_Anim(self):
        self.elev.open[self.floor - 1][self.no] = 0
        self.open = False
        self.stop_timer.stop()

    # Functions executed at the end of the animation
    def anim_end(self, anim):
        if anim.direction() == QAbstractAnimation.Backward:
            self.close_timer.stop()
            self.elev.open[self.floor - 1][self.no] = 0
            self.open = False
        else:
            self.close_timer.start(2000)

    # Functions executed after pressing the door open button
    def keep_open(self):
        if self.open == False:
            self.open = True
            self.elev.open[self.floor - 1][self.no] = 1
            if self.elev.floor == self.floor:
                self.openDoor_Anim()
                self.elev.elevator_Anim[2 * self.no].finished.disconnect()

    # Functions executed after pressing the door close button
    def keep_close(self):
        if self.open == True:
            if self.elev.floor == self.floor:
                self.closeDoor_Anim()
                self.elev.elevator_Anim[2 * self.no].finished.connect(partial(self.anim_end, anim = self.elev.elevator_Anim[2 * self.no]))
            else:
                self.elev.open[self.floor - 1][self.no] = 0
                self.open = False


# Create Controller class
class Controller(object):
    def __init__(self, Elev):
        self.elev = Elev
        self.request_queue=[]
        self.elevators = []
        self.floor = 1

        for i in range(5):
            self.elevators.append(Elevator(i, self.elev))

        self.dispatch_timer = QTimer()
        self.dispatch_timer.timeout.connect(self.update_elevator_position)
        self.dispatch_timer.start(1000)
        self.fix_timer = QTimer()

    # Calculate priority
    def calculate_prior(self, move):
        scores = []
        for i in range(5):
            score = 0
            if self.elevators[i].damage == True:
                score = -1
            elif (self.floor - self.elevators[i].floor) * self.elevators[i].move < 0:
                score = -2
            else:
                result = [0]
                for j in self.elevators[i].goal:
                    result.append(abs(j - self.floor))
                score = 20 - max(result)
                if self.elevators[i].move == 0:
                    score = 20 - abs(self.elevators[i].floor - self.floor)
                goal_len = len(self.elevators[i].goal)
                if goal_len != 0:
                    if (self.elevators[i].goal[goal_len - 1] - self.floor) * move < 0:
                        score = -2
                if move == 1:
                    index = 0
                else:
                    index = 1
                if i == self.elev.request[self.floor - 1][1 - index]:
                    score = -4

            scores.append(score)
        return scores

    # Performe elevator dispatching
    def dispatch(self, move):
        self.floor = self.elev.floor
        priors = self.calculate_prior(move)

        for i in range(5):
            if move == 1:
                self.elev.pressed[self.floor - 1][0] = 1
            if move == -1:
                self.elev.pressed[self.floor - 1][1] = 1

        max_index = np.argmax(priors)
        max_value = max(priors)

        if move == 1:
            index = 0
        else:
            index = 1
        self.elev.request[self.floor - 1][index] = max_index

        if max_value == -1:
            QtWidgets.QMessageBox.critical(self.elev, "Error", "All elevators have been damaged!")
        elif max_value == -2:
            if self.floor not in self.elevators[max_index].prior:
                self.elevators[max_index].prior.append(self.floor)
        else:
            if self.floor not in self.elevators[max_index].goal:
                self.elevators[max_index].goal.append(self.floor)

    # Update the state of elevators
    def update_elevator_position(self):
        self.floor = self.elev.floor
        for i in range(5):
            self.elevators[i].moving()
            if self.elev.pressed[self.floor - 1][0] == 1:
                self.elev.up_button[i].setDown(True)
            else:
                self.elev.up_button[i].setDown(False)
            if self.elev.pressed[self.floor - 1][1] == 1:
                self.elev.down_button[i].setDown(True)
            else:
                self.elev.down_button[i].setDown(False)

    # Functions executed after clicking the alarm button
    def alarm(self, no):
        self.elev.alarm_button[no].setStyleSheet("background-color: rgb(255, 248, 0);")
        self.elevators[no].damage = True
        for i in range(20):
            button = self.elev.findChild(QtWidgets.QPushButton, "button " + str(no) + ' ' + str(i + 1))
            button.setEnabled(False)
        self.elev.open_button[no].setEnabled(False)
        self.elev.close_button[no].setEnabled(False)
        self.fix_timer.timeout.connect(partial(self.fix, no = no))
        self.fix_timer.start(20000)

    # Regular elevator repair
    def fix(self, no):
        self.elev.alarm_button[no].setStyleSheet("background-color: rgb(240, 0, 0);")
        self.elevators[no].damage = False
        for i in range(20):
            button = self.elev.findChild(QtWidgets.QPushButton, "button " + str(no) + ' ' + str(i + 1))
            button.setEnabled(True)
        self.elev.open_button[no].setEnabled(True)
        self.elev.close_button[no].setEnabled(True)
        self.elev.up_button[no].setEnabled(True)
        self.elev.down_button[no].setEnabled(True)
