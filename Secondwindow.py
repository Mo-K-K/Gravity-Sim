
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import random
import sys
import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import PlotOfParticles2

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random


from PlotOfParticles import *


class secondWindow(QMainWindow):
    def __init__(self, name=None, timepassed = 0, masses = []):
        super().__init__()
        self.buttons = []
        self.name = name
        self.num_buttons = len(name)
        self.timepassed = timepassed
        self.initUI()
        self.Window = None
        self.Window2 = None
        self.masses = masses
        
        
    def initUI(self):
        '''initialises second window UI'''
        #initialise layout
        cwidget = QWidget(self)
        self.setCentralWidget(cwidget)
        layout = QVBoxLayout(cwidget)
        
        for i in range(self.num_buttons+1):
            if i != (self.num_buttons):
                button = QPushButton(f'Button {i+1}', self)
                button.clicked.connect(lambda _, index = i: self.LaunchGraphOfForce(index))
                layout.addWidget(button)
                self.buttons.append(button)
            elif i == (self.num_buttons):
                button = QPushButton('Diagram of bodies', self)
                layout.addWidget(button)
                self.buttons.append(button)
        self.buttons[self.num_buttons].clicked.connect(self.DiagramOfBodies)
      
    
    def LaunchGraphOfForce(self, index):
        '''Launces the Animate class which creates the force graphs'''
        rand=Animate(self.name, self.masses, index)
        rand.start()
    
    def DiagramOfBodies(self):
        '''Opens the window which shows the system animation'''
        
        if self.Window is None:
            self.Window = SystemAnimation(self.name, timepassed = self.timepassed, masses = self.masses)
        self.Window.show()
        '''
        PlotOfParticles2.main(self.name, self.masses)
        '''

    
class Animate:

    def __init__(self, filenames, masses, index):
        #initilise the figure
        self.index = index
        self.name = filenames
        self.masses = masses
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(3, 1, 1)
        self.ax2 = self.fig.add_subplot(3, 1, 2)
        self.ax3 = self.fig.add_subplot(3, 1, 3)
        self.xs = []
        self.ys = []
        self.xs1 = []
        self.ys1 = []
        self.xs2 = []
        self.ys2 = []
        self.readings = 30
        self.bodies=[]
        self.GetInfoFromFile()

    def _update(self, i):
        '''updates the graphs'''
        #update the numbers
        self.updatenumbers()

        #init x and y values
        self.xs.append(i)
        self.ys.append(self.bodies[0].position[0])
        self.ys1.append(self.bodies[0].position[1])
        self.ys2.append(self.bodies[0].position[2])

        #clears and then plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax1.plot(self.xs, self.ys)
        self.ax2.plot(self.xs, self.ys1)
        self.ax3.plot(self.xs, self.ys2)

        #changes axis
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.ylabel('Force (N)')

    def start(self):
        #starts animation
        self.anim = animation.FuncAnimation(self.fig, self._update, interval=100)
        plt.show()
        
    def GetInfoFromFile(self):
        '''gets initial values from the ephemerides saved in the test folder'''
        for x in range(len(self.name)):
            pos1, pos2, pos3 = 0, 0, 0
            vel1, vel2, vel3 = 0, 0, 0
            names = self.name[x]
            name = names[64:-4]
            m = self.masses[x]
            with open("test/"+name+".txt") as file:
                for line in file:
                    if line[:4] == " X =":
                        pos1=float(line[4:26])
                        pos2=float(line[30:52])
                        pos3=float(line[57:78])
                    if line[:4] == " VX=":
                        vel1=float(line[4:26])
                        vel2=float(line[30:52])
                        vel3=float(line[57:78])
                        break
                    
            pos = np.array([pos1*1e3, pos2*1e3, pos3*1e3], dtype=float) 
            vel = np.array([vel1*1e3, vel2*1e3, vel3*1e3], dtype=float)  
            self.bodies.append(Particle(
                position=pos,
                velocity=vel,
                acceleration=np.array([0, 0, 0]),
                name = name,
                mass = m
            ))
            
    def updatenumbers(self):
        '''calculates the new acceleration on a body with respect to all other bodies and updates the position and veloicty vectors of all the bodies'''
        acc=0
        acceleration=[]
        for h in range(2000):
            for i in range(len(self.bodies)):
                for j in range(len(self.bodies)):
                    if i != j:
                        self.bodies[i].updateGravitationalAcceleration(self.bodies[j])
                        acc+=self.bodies[i].acceleration
                acceleration.append(acc)
                acc=0
            for k in range(len(self.bodies)):
                self.bodies[k].update(60, acceleration[k], 'E')
            acceleration=[]
    


    