
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
        rand=Animate(self.name)
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

    def __init__(self, filnames):
        # Create figure for plotting
        self.filenames = filenames
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

    # This function is called periodically from FuncAnimation
    def _update(self, i):

        # Read temperature (Celsius) from TMP102
        temp_c = random()

        # Add x and y to lists
        self.xs.append(i)
        self.ys.append(temp_c)

        # Limit x and y lists to 20 items
        #self.xs = self.xs[-self.readings:]
        #self.ys = self.ys[-self.readings:]

        # Draw x and y lists
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax1.plot(self.xs, self.ys)
        self.ax2.plot(self.xs, self.ys)
        self.ax3.plot(self.xs, self.ys)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.ylabel('Force (N)')

    def start(self):
        print('Starting')
        # Set up plot to call animate() function periodically
        self.anim = animation.FuncAnimation(self.fig, self._update, interval=100)
        plt.show()
        
    def GetInfoFromFile(self):
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
    

if __name__== '__main__':
    app=QApplication(sys.argv)
    filenames = ['C:/Users/rafeh/Desktop/Physics/Programming/PHYS281/Project/test/Sol.txt', 'C:/Users/rafeh/Desktop/Physics/Programming/PHYS281/Project/test/Earth.txt']
    masses = [2e30,5.9e24]
    window = secondWindow(filenames, 5, masses)
    window.show()
    
    sys.exit(app.exec_())

     
'''
        
class Canvas(FigureCanvas):
    A new calss to define axes and figure as Funcanimation doesnt initialise properly when defined in the same class
    def __init__(self, parent=None):
        fig = Figure(figsize=(6, 8), dpi=100)
        self.axes=fig.add_subplot(111)
        super(Canvas, self).__init__(fig)
        
class Graph(QMainWindow):
    Class makes an animated graph of the function of Force against the function of time for the chosen body
    def __init__(self, n_data, bodies, index, masses):
        super(Graph, self).__init__()
        self.filenames = bodies
        self.index = index
        self.masses = masses
        self.bodies = []
        self.nbodies=len(self.bodies)
        self.n_data = n_data
        
        self.canvas = Canvas(self)
        
        self.setCentralWidget(self.canvas)
        self.GetInfoFromFile()

        #n_data = 50
        self.xdata = list(range(n_data))
        self.ydata=[]
        for x in range(n_data):
            self.ydata.append((np.linalg.norm(self.bodies[self.index].acceleration)*self.bodies[self.index].mass))
            self.updatenumbers()
        print(self.xdata, self.ydata)

        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self.initplot = None
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
    def update_plot(self):
        self.updatenumbers()
        self.ydata=self.ydata[1:] + [(np.linalg.norm(self.bodies[self.index].acceleration)*self.bodies[self.index].mass)]

        # Note: we no longer need to clear the axis.
        if self.initplot is None:
            initplot = self.canvas.axes.plot(self.xdata, self.ydata, 'b')
            #self.axes.set_ylim(100)
            self.initplot = initplot[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self.initplot.set_ydata(self.ydata)
            
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
        
    def updatenumbers(self):
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
                self.bodies[k].update(60, acceleration[k])
            acceleration=[]
        self.new_y = self.bodies[self.index].acceleration
            
    def GetInfoFromFile(self):
        for x in range(len(self.filenames)):
            pos1, pos2, pos3 = 0, 0, 0
            vel1, vel2, vel3 = 0, 0, 0
            names = self.filenames[x]
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
            '''