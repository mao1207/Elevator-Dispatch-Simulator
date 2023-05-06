# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from dispatch import Controller
from PyQt5.QtCore import *
from functools import partial
import re


class Ui_MainWindow(object):
    def __init__(self):
        self.Ctrl = Controller(self)

        # Initialize UI elements
        self.buttonQwidget = []
        self.buttonLayout = []
        self.lcd_number = []
        self.lcd_number_floor = []
        self.elevator_number = []
        self.open_button = []
        self.close_button = []
        self.alarm_button = []
        self.label = []
        self.combo_box = []

        self.stateshow = []
        self.elevator_back = []
        self.elevator_front = []
        self.elevator_Anim = []
        self.up_button = []
        self.down_button = []

        # Initialize pressed and open status for floors
        self.pressed = []
        for i in range(20):
            self.pressed.append([0,0])

        self.open = []
        for i in range(20):
            self.open.append([0,0,0,0,0])

        # Initialize request status for floors
        self.request = []
        for i in range(20):
            self.request.append([-1,-1])

        # Initialize floor
        self.floor = 0

    def setupUi(self, MainWindow):
        # Set up the main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 900)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set style of font
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        label_font = QtGui.QFont()
        label_font.setFamily("Arial")
        label_font.setPointSize(14)

        # Elevator View

        self.label.append(QtWidgets.QLabel(self.centralwidget))
        self.label[0].setGeometry(QtCore.QRect(620, 20, 200, 30))
        self.label[0].setObjectName("elevatorView")
        self.label[0].setText('Elevator View')
        self.label[0].setFont(label_font)

        # create button region
        button_Qwidget_pos = [80, 350, 630, 910, 1190]
        for i in range(0, len(button_Qwidget_pos)):
            self.buttonQwidget.append(QtWidgets.QWidget(self.centralwidget))
            self.buttonQwidget[i].setGeometry(QtCore.QRect(button_Qwidget_pos[i], 60, 81, 451))
            self.buttonQwidget[i].setObjectName("buttonWidget" + str(i))
            self.buttonLayout.append(QtWidgets.QGridLayout(self.buttonQwidget[i]))
            self.buttonLayout[i].setContentsMargins(0, 0, 0, 0)
            self.buttonLayout[i].setObjectName("buttonLayout" + str(i))

        # Draw buttons of each elevator
        names = ['19', '20', '17', '18', '15', '16', '13', '14', '11', '12', '9', '10', '7', '8', '5', '6', '3', '4',
                 '1', '2']
        positions = [(i, j) for i in range(10) for j in range(2)]

        for i in range(0, len(button_Qwidget_pos)):
            for position, name in zip(positions, names):
                button = QtWidgets.QPushButton(name)
                button.setFont(font)
                button.setObjectName("button " + str(i) + ' ' + name)
                button.setStyleSheet("background-color: rgb(200, 200, 200);")
                button.clicked.connect(partial(self.press_button,elevator_no = i, floor = int(name)))
                self.buttonLayout[i].addWidget(button, *position)

        # Draw LED floor digital display
        lcdNumber_pos = [200, 470, 750, 1030, 1310]

        # Draw switch buttons and alarm buttons
        for i in range(0, len(lcdNumber_pos)):
            self.elevator_number.append(QtWidgets.QLabel(self.centralwidget))
            self.elevator_number[i].setGeometry(QtCore.QRect(lcdNumber_pos[i], 70, 100, 30))
            self.elevator_number[i].setObjectName("elevatorNumber" + str(i) + ' ' + name)
            self.elevator_number[i].setText('elevator' + str(i+1))
            self.elevator_number[i].setFont(font)

            self.lcd_number.append(QtWidgets.QLCDNumber(self.centralwidget))
            self.lcd_number[i].setGeometry(QtCore.QRect(lcdNumber_pos[i], 110, 50, 40))
            self.lcd_number[i].setDigitCount(2)
            self.lcd_number[i].setProperty("value", 1.0)
            self.lcd_number[i].setObjectName("lcdNumber" + str(i))

            self.open_button.append(QtWidgets.QPushButton(self.centralwidget))
            self.open_button[i].setGeometry(QtCore.QRect(lcdNumber_pos[i], 230, 50, 30))
            self.open_button[i].setObjectName("openButton" + str(i) + ' ' + name)
            self.open_button[i].setStyleSheet("background-color: rgb(200, 200, 200);")
            self.open_button[i].setText('open')
            self.open_button[i].setFont(font)
            self.open_button[i].clicked.connect(self.Ctrl.elevators[i].keep_open)

            self.close_button.append(QtWidgets.QPushButton(self.centralwidget))
            self.close_button[i].setGeometry(QtCore.QRect(lcdNumber_pos[i], 280, 50, 30))
            self.close_button[i].setObjectName("closeButton" + str(i) + ' ' + name)
            self.close_button[i].setStyleSheet("background-color: rgb(200, 200, 200);")
            self.close_button[i].setText('close')
            self.close_button[i].setFont(font)
            self.close_button[i].clicked.connect(self.Ctrl.elevators[i].keep_close)

            self.alarm_button.append(QtWidgets.QPushButton(self.centralwidget))
            self.alarm_button[i].setGeometry(QtCore.QRect(lcdNumber_pos[i], 400, 50, 30))
            self.alarm_button[i].setObjectName("alarmButton" + str(i) + ' ' + name)
            self.alarm_button[i].setStyleSheet("background-color: rgb(240, 0, 0);")
            self.alarm_button[i].setText('alarm')
            self.alarm_button[i].setFont(font)
            self.alarm_button[i].clicked.connect(partial(self.Ctrl.alarm, i))


        # Floor View

        # Draw dividing line
        dividing_line = QtWidgets.QGraphicsView(self.centralwidget)
        dividing_line.setGeometry(QtCore.QRect(0, 520, 1400, 5))
        dividing_line.setStyleSheet("background-color: rgb(87, 87, 87);")

        # Draw text tips and floor selection box
        self.label.append(QtWidgets.QLabel(self.centralwidget))
        self.label[1].setGeometry(QtCore.QRect(580, 540, 200, 30))
        self.label[1].setObjectName("floorView")
        self.label[1].setText('Floor View')
        self.label[1].setFont(label_font)

        self.combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box.setGeometry(QtCore.QRect(700, 540, 111, 31))
        self.combo_box.setObjectName("comboBox")
        self.combo_box.setFont(font)
        for i in range(0, 20):
            self.combo_box.addItem('floor ' + str(i + 1))  # 加入楼层信息
            self.combo_box.activated[int].connect(self.switch_floor)

        # Draw LED screen
        for i in range(0, len(lcdNumber_pos)):
            self.lcd_number_floor.append(QtWidgets.QLCDNumber(self.centralwidget))
            self.lcd_number_floor[i].setGeometry(QtCore.QRect(lcdNumber_pos[i] - 140, 600, 50, 40))
            self.lcd_number_floor[i].setDigitCount(2)
            self.lcd_number_floor[i].setProperty("value", 1.0)
            self.lcd_number_floor[i].setObjectName("lcdFloorNumber" + str(i))

        # Draw elevators
        elevator_pos = [40, 310, 590, 870, 1150]
        for i in range(0, len(elevator_pos)):

            # Draw the elevator background behind
            self.elevator_back.append(QtWidgets.QGraphicsView(self.centralwidget))
            self.elevator_back[i].setGeometry(QtCore.QRect(elevator_pos[i], 650, 130, 160))
            self.elevator_back[i].setStyleSheet("background-color: rgb(87, 87, 87);")
            self.elevator_back[i].setObjectName("elevator_back" + str(i))

            # Draw the two elevator doors in front
            self.elevator_front.append(QtWidgets.QGraphicsView(self.centralwidget))
            self.elevator_front[2 * i].setGeometry(QtCore.QRect(elevator_pos[i], 650, 64, 161))
            self.elevator_front[2 * i].setStyleSheet("background-color: rgb(160, 160, 160);")
            self.elevator_front[2 * i].setObjectName("elevator_front" + str(2 * i))
            self.elevator_Anim.append(QPropertyAnimation(self.elevator_front[2 * i], b"geometry"))
            self.elevator_Anim[2 * i].setDuration(1000)  # 设定动画时间
            self.elevator_Anim[2 * i].setStartValue(QtCore.QRect(elevator_pos[i], 650, 64, 161))  # 设置起始大小
            self.elevator_Anim[2 * i].setEndValue(QtCore.QRect(elevator_pos[i], 650, 8, 161))  # 设置终止大小
            self.elevator_Anim[2 * i].finished.connect(partial(self.Ctrl.elevators[i].anim_end, anim = self.elevator_Anim[2 * i]))

            self.elevator_front.append(QtWidgets.QGraphicsView(self.centralwidget))
            self.elevator_front[2 * i + 1].setGeometry(QtCore.QRect(elevator_pos[i] + 67, 650, 64, 161))
            self.elevator_front[2 * i + 1].setStyleSheet("background-color: rgb(160, 160, 160);")
            self.elevator_front[2 * i + 1].setObjectName("elevator_front" + str(2 * i + 1))
            self.elevator_Anim.append(QPropertyAnimation(self.elevator_front[2 * i + 1], b"geometry"))
            self.elevator_Anim[2 * i + 1].setDuration(1000)
            self.elevator_Anim[2 * i + 1].setStartValue(QtCore.QRect(elevator_pos[i] + 67, 650, 64, 161))
            self.elevator_Anim[2 * i + 1].setEndValue(QtCore.QRect(elevator_pos[i] + 123, 650, 8, 161))

        # Show whether the elevator is going up or down
        stateshow_pos = [115, 385, 665, 945, 1225]
        for i in range(0, len(stateshow_pos)):
            self.stateshow.append(QtWidgets.QGraphicsView(self.centralwidget))
            self.stateshow[i].setGeometry(QtCore.QRect(stateshow_pos[i], 590, 70, 60))
            self.stateshow[i].setStyleSheet("QGraphicsView{border-image: url(../Resources/Button/state.png)}")
            self.stateshow[i].setObjectName("stateshow" + str(i))

        # Draw the up and down buttons
        for i in range(0, len(elevator_pos)):
            self.up_button.append(QtWidgets.QPushButton(self.centralwidget))
            self.up_button[i].setGeometry(QtCore.QRect(stateshow_pos[i] + 50, 670, 60, 40))
            self.up_button[i].setStyleSheet("QPushButton{border-image: url(../Resources/Button/doorup.png)}"
                                       "QPushButton:hover{border-image: url(../Resources/Button/doorup_hover.png)}"
                                       "QPushButton:pressed{border-image: url(../Resources/Button/doorup_pressed.png)}")
            self.up_button[i].setObjectName("upButton" + str(i))
            self.up_button[i].clicked.connect(partial(self.up_down_button,move = 1))

            self.down_button.append(QtWidgets.QPushButton(self.centralwidget))
            self.down_button[i].setGeometry(QtCore.QRect(stateshow_pos[i] + 50, 720, 60, 40))
            self.down_button[i].setStyleSheet("QPushButton{border-image: url(../Resources/Button/doordown.png)}"
                                            "QPushButton:hover{border-image: url(../Resources/Button/doordown_hover.png)}"
                                            "QPushButton:pressed{border-image: url(../Resources/Button/doordown_pressed.png)}")
            self.down_button[i].setObjectName("downButton" + str(i))
            self.down_button[i].clicked.connect(partial(self.up_down_button,move = -1))
        self.switch_floor(0)

        # Drawing the main menu and status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Up and down button slot function
    def up_down_button(self, move):
        self.floor = int(re.search(r'\d+', self.combo_box.currentText()).group())
        self.Ctrl.dispatch(move = move)

    # Elevator button slot function
    def press_button(self, elevator_no, floor):
        self.Ctrl.elevators[elevator_no].press_button(floor)

    # Floor selection box slot function
    def switch_floor(self, floor):
        self.floor = floor + 1
        for i in range(len(self.elevator_Anim)//2):
            if floor == 0:
                self.down_button[i].setEnabled(False)
            else:
                self.down_button[i].setEnabled(True)
            if floor == 19:
                self.up_button[i].setEnabled(False)
            else:
                self.up_button[i].setEnabled(True)
            if self.open[self.floor - 1][i] == 1:
                self.elevator_Anim[2 * i].setDirection(QAbstractAnimation.Forward)
                self.elevator_Anim[2 * i + 1].setDirection(QAbstractAnimation.Forward)
            else:
                self.elevator_Anim[2 * i].setDirection(QAbstractAnimation.Backward)
                self.elevator_Anim[2 * i + 1].setDirection(QAbstractAnimation.Backward)
            self.elevator_Anim[2 * i].setDuration(0)
            self.elevator_Anim[2 * i + 1].setDuration(0)
            self.elevator_Anim[2 * i].start()
            self.elevator_Anim[2 * i + 1].start()
            self.elevator_Anim[2 * i].setDuration(1000)
            self.elevator_Anim[2 * i + 1].setDuration(1000)