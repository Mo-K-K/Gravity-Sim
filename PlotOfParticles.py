import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math
import copy

from Particle import *

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class SystemAnimation(QMainWindow):
    def __init__(self, fname, timepassed = 0, masses = []):
        super().__init__()
        #
        self.nbodies = len(fname)
        #
        self.filenames = fname
        self.masses = masses
        self.bodies=[]
        self.timepassed = timepassed
        self.colours = self.randomisecolours(exclude='navy')
        self.GetInfoFromFile()
        self.Data = []
        self.time = 0
        self.BData =[]
        self.tdata = []
        self.xdata = []
        self.ydata = []
        self.zdata = []
        
        #print(self.bodies[0].velocity, bodies[1].velocity)
        #print(self.bodies[0].position, bodies[1].position)
        #print(self.bodies[0].acceleration, bodies[1].acceleration)
        self.initparticlesx = [self.bodies[i].position[0] for i in range(len(self.bodies))]
        self.initparticlesy = [self.bodies[j].position[1] for j in range(len(self.bodies))]
        
        self.limit = max(np.fabs(self.initparticlesy))*2.5
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('System Animation')
        self.setGeometry(100, 100, 800, 600)
        
        #main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        #Matplotlib figure and the canvas
        self.fig, self.ax = plt.subplots(facecolor = 'navy')
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        
        #create animation
        self.ani = animation.FuncAnimation(self.fig, self.updatePlot, frames = 100, interval=50, blit = False)
        #self.bodies.append(Bodies(name = 'test'))

        
    def randomisecolours(self, exclude=None):
        cmap = plt.cm.jet
        normalisecolours = mcolors.Normalize(vmin=0, vmax= self.nbodies)
        scalarmap = plt.cm.ScalarMappable(cmap=cmap, norm=normalisecolours)
        
        colours = [scalarmap.to_rgba(i) for i in range(self.nbodies)]
        
        if exclude:
            excludergba = mcolors.hex2color(mcolors.cnames[exclude])
            colours = [c for c in colours if colours[:3] != excludergba]
                    
        return colours
    

    
    def updatePlot(self, frame):
        #use function to update position of particle
        self.updatenumbers()
        #send updated positions to graph class
        
        #self.particles += 0.01 * np.random.randn(self.nbodies, 2)
        
        #print("pos of x: ", self.particlesx)
        #print("pos of y: ", self.particlesy)
        
        #clear plot
        self.ax.clear()
        
        self.ax.set_facecolor('navy')
        #self.ax.axis('off')

        #plot particle with updated position
        self.ax.scatter(self.particlesx, self.particlesy, c='Red')
        #print(self.particlesx, self.particlesy)
        self.ax.set_xlim(-self.limit, self.limit)
        self.ax.set_ylim(-self.limit,self.limit)
            
        if self.time == 6000000:
            for x in range(len(self.Data)):
                self.tdata.append(self.Data[x][0])
                self.xdata.append(self.Data[x][1])
                self.ydata.append(self.Data[x][2])
                self.zdata.append(self.Data[x][3])
            Data = [self.tdata, self.xdata, self.ydata, self.zdata]
            with open('Data.txt', 'w') as file:
                for item in Data:
                    file.write("%s\n" % item)
                
        self.canvas.draw()
        
    def GetInfoFromFile(self):
        '''gets information from the selected file and produces an object.
        This is done by calling the class Bodies'''
        #pos is the initial positions of the body and vec are the initial velocites
    
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
            

    def updatenumbers(self):
        method = 'V'
        acc=0
        acceleration=[]
        self.BData=[]
        if method == 'ER':
            for x in range(2000):
                for i in range(len(self.bodies)):
                    for j in range(len(self.bodies)):
                        if i!=j:
                            self.bodies[i].updateGravitationalAcceleration(self.bodies[j])
                            acc += self.bodies[i].acceleration
                    acceleration.append(acc)
                    acc = 0
                for k in range(len(self.bodies)):
                    self.bodies[k].update(60/2, acceleration[k], 'E')
                acceleration=[]
                acc=0
                for a in range(len(self.bodies)):
                    for b in range(len(self.bodies)):
                        if a!=b:
                            self.bodies[a].updateGravitationalAcceleration(self.bodies[b])
                            acc += self.bodies[a].acceleration
                    acceleration.append(acc)
                    acc = 0
                for c in range(len(self.bodies)):
                    self.bodies[c].update(60, acceleration[c], 'E')
                acceleration=[]
                acc=0
                self.time += 60
                     
        else: 
            for h in range(2000):
                for x in range(len(self.bodies)):
                    acceleration0=[self.bodies[x].acceleration for x in range(len(self.bodies))]
                for i in range(len(self.bodies)):
                    for j in range(len(self.bodies)):
                        if i != j:
                            self.bodies[i].updateGravitationalAcceleration(self.bodies[j])
                            acc+=self.bodies[i].acceleration
                    acceleration.append(acc)
                    acc=0
                for k in range(len(self.bodies)):
                    if method == 'V':
                        self.bodies[k].update(60, acceleration[k], method, acceleration0[k])
                    else:
                        self.bodies[k].update(60, acceleration[k], method)
                self.time += 60
                acceleration=[]
                acceleration0=[]
                    
            
        
        self.particlesx = [self.bodies[i].position[0] for i in range(len(self.bodies))]
        self.particlesy = [self.bodies[j].position[1] for j in range(len(self.bodies))]
        
        self.BData=[self.time]
        for x in range(0, 3):
            self.BData.append(self.bodies[0].position[x])
        self.Data.append(self.BData)

        #tranforms the axis to set the first body at the origin
        
        for k in range(1, self.nbodies-1):
            self.particlesx[k]=self.particlesx[k]-self.initparticlesx[0]
            self.particlesy[k]=self.particlesy[k]-self.initparticlesy[0]
            
        

if __name__ == "__main__":
    app=QApplication(sys.argv)
    '''
    earthMass = 2.00e30
    earthRadius = 696340
    Sol = Particle(
        position=np.array([-1.214048065520218e9, -4.013795987957321e8, 0]),
        velocity=np.array([8.012077096627646e-5, -1.271120897662364e-5, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Sol",
        mass=earthMass
        )
    satPosition = earthRadius + 1.49e11
    satVelocity = np.sqrt(Sol.G * Sol.mass / satPosition)

    Earth = Particle(
        position=np.array([5.361071004514999e10, 1.365682433995717e11, 0]),
        velocity=np.array([-2.813245183269979e4, 1.094520152946133e4, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Earth",
        mass=5.9e24
    )
    
    Mars = Particle(
        position=np.array([-7.816400366646364e10, 7.443698280209219e10, 0]),
        velocity=np.array([-2.453487660910571e4, -2.530241055411627e4, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Mars",
        mass=6.39e23
    )
    
    Venus = Particle(
        position=np.array([-1.083732613923766e11, -2.011037351357945e11, 0]),
        velocity=np.array([2.229340842795413e4, -9.349070226191618e3, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Venus",
        mass =4.9e24
    )
    
    #bodies = [Sol, Earth, Mars, Venus]
    fname = ['C:/Users/rafeh/Desktop/Physics/Programming/PHYS281/Project/test/Sol.txt', 'C:/Users/rafeh/Desktop/Physics/Programming/PHYS281/Project/test/Earth.txt']
    masses = [2e30, 5.9e24]
    window = SystemAnimation(fname, 5000, masses)
    window.show()
    
    sys.exit(app.exec_())
    '''

        
    
