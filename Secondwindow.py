from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys


class secondWindow(QMainWindow):
    def __init__(self, name=None, num_buttons = 0):
        super().__init__()
        self.buttons = []
        self.name = name
        self.num_buttons = num_buttons
        self.initUI()
        
        
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
                button = QPushButton('Ting', self)
                layout.addWidget(button)
                self.buttons.append(button)
        print(self.name)