from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from PlotOfParticles import *


class secondWindow(QMainWindow):
    def __init__(self, name=None, num_buttons = 0):
        super().__init__()
        self.buttons = []
        self.name = name
        self.num_buttons = num_buttons
        self.initUI()
        self.Window = None
        
        
    def initUI(self):
        #initialise layout
        cwidget = QWidget(self)
        self.setCentralWidget(cwidget)
        layout = QVBoxLayout(cwidget)
        
        for i in range(self.num_buttons+1):
            if i != (self.num_buttons):
                button = QPushButton(f'Button {i+1}', self)
                layout.addWidget(button)
                self.buttons.append(button)
            elif i == (self.num_buttons):
                button = QPushButton('Diagram of bodies', self)
                layout.addWidget(button)
                self.buttons.append(button)
        self.buttons[self.num_buttons].clicked.connect(self.DiagramOfBodies)
        
    def DiagramOfBodies(self):
        '''Opens the window which shows the system animation'''
        if self.Window is None:
            self.Window = SystemAnimation(bodies = self.name)
        self.Window.show()
        