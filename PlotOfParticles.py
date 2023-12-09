import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from Bodies import Bodies

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class SystemAnimation(QMainWindow):
    def __init__(self, bodies):
        super().__init__()
        #
        self.nbodies = len(bodies)
        self.filenames = bodies
        self.particles = np.random.randn(self.nbodies, 2)
        #
        self.bodies = []
        self.colours = self.randomisecolours(exclude='navy')
        
        self.initUI()
        
    def initUI(self):
        self.GetInfoFromFile()
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
        
    def GetInfoFromFile(self):
        '''gets information from the selected file and produces an object.
        This is done by calling the class Bodies'''
        #pos is the initial positions of the body and vec are the initial velocites
        for x in range(len(self.filenames)):
            pos=np.array([0, 0, 0])
            vec=np.array([0, 0, 0])
            names = self.filenames[x]
            name = names[64:-4]
            with open("test/"+name+".txt") as file:
                for line in file:
                    if line[:4] == " X =":
                        pos[0]=float(line[4:26])
                        pos[1]=float(line[31:52])
                        pos[2]=float(line[57:78])
                    if line[:4] == " VX=":
                        vec[0]=float(line[4:26])
                        vec[1]=float(line[30:52])
                        vec[2]=float(line[57:78])
                        if name == "Mars":
                            m = 6.39e23
                        elif name == "Venus":
                            m = 4.87e24
                        break
                    
                    
            self.bodies.append(Bodies(
                position=pos,
                velocity=vec,
                acceleration=np.array([0, 0, 0]),
                name = name,
                mass = m
            ))
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
        self.ax.axis('off')

        #plot particle with updated position
        self.ax.scatter(self.particlesx, self.particlesy, c='Red')
        ylim = self.bodies[0].position[1]+self.bodies[1].position[1]
        xlim = self.bodies[0].position[0]+self.bodies[1].position[0]
        
        self.ax.set_xlim(-xlim, xlim)
        self.ax.set_ylim(-ylim, ylim)

        self.canvas.draw()

    def updatenumbers(self):
        self.bodies[0].gravacc(self.bodies[1])
        self.bodies[1].gravacc(self.bodies[0])
        self.bodies[0].update(600)
        self.bodies[1].update(600)
        self.particlesx = [self.bodies[i].position[0] for i in range(len(self.bodies))]
        self.particlesy = [self.bodies[j].position[1] for j in range(len(self.bodies))]
        
if __name__ == '__main__':
    app = QApplication(sys.argv)


    window = SystemAnimation(["C:/Users/rafeh/Desktop/Physics/Programming/PHYS281/Project/test/Mars.txt", "C:/Users/rafeh/Desktop/Physics/Programming/PHYS281/Project/test/Venus.txt"])
    window.show()
    sys.exit(app.exec_())
    
