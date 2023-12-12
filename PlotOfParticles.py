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
        #
        self.bodies = bodies
        self.colours = self.randomisecolours(exclude='navy')
        self.initparticlesx = [self.bodies[i].position[0] for i in range(len(self.bodies))]
        self.initparticlesy = [self.bodies[j].position[1] for j in range(len(self.bodies))]
        
        
        self.ylim0 = min(self.initparticlesy)
        self.ylim1 = max(self.initparticlesy)
        self.xlim0 = min(self.initparticlesx)
        self.xlim1 = max(self.initparticlesx)
        
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
        self.ax.set_xlim(-5e11, 5e11)
        self.ax.set_ylim(-5e11,5e11)

        self.canvas.draw()

    def updatenumbers(self):
        '''
        for i in range(len(self.bodies)):
            self.bodies[i].gravacc(self.bodies[:1])
            self.bodies[:i].gravacc(self.bodies[i])
        for j in range(len(self.bodies)):
            self.bodies[j].gravavv(self.bodies[j])
        '''
        
        acc = 0
        for i in range(self.nbodies):
            for j in range(self.nbodies):
                if i != j:
                    self.bodies[i].gravacc(self.bodies[j], False)
                    acc += self.bodies[i].acceleration
            for x in range(200000):
                self.bodies[i].update(6, accelerate = acc)
            acc=0
                    
            
        
        self.particlesx = [self.bodies[i].position[0] for i in range(len(self.bodies))]
        self.particlesy = [self.bodies[j].position[1] for j in range(len(self.bodies))]
        
        #tranforms the axis to set the first body at the origin
        self.particlesx=[0, self.particlesx[1]-self.initparticlesx[0], self.particlesx[2]-self.initparticlesx[0], self.particlesx[3]-self.initparticlesx[0]]
        self.particlesy=[0, self.particlesy[1]-self.initparticlesy[0], self.particlesy[2]-self.initparticlesx[0], self.particlesx[3]-self.initparticlesy[0]]
        

if __name__ == "__main__":
    app=QApplication(sys.argv)
    earthMass = 2.00e30
    earthRadius = 696340
    Sol = Bodies(
        position=np.array([-1.214048065520218e9, -4.013795987957321e8, 0]),
        velocity=np.array([8.012077096627646e-5, -1.271120897662364e-5, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Sol",
        mass=earthMass
        )
    satPosition = earthRadius + 1.49e11
    satVelocity = np.sqrt(Sol.G * Sol.mass / satPosition)

    Earth = Bodies(
        position=np.array([5.361071004514999e10, 1.365682433995717e11, 0]),
        velocity=np.array([-2.813245183269979e4, 1.094520152946133e4, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Earth",
        mass=5.9e24
    )
    
    Mars = Bodies(
        position=np.array([-7.816400366646364e10, 7.443698280209219e10, 0]),
        velocity=np.array([-2.453487660910571e4, -2.530241055411627e4, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Mars",
        mass=6.39e23
    )
    
    Venus = Bodies(
        position=np.array([-1.083732613923766e11, -2.011037351357945e11, 0]),
        velocity=np.array([2.229340842795413e4, -9.349070226191618e3, 0]),
        acceleration=np.array([0, 0, 0]),
        name="Venus",
        mass =4.9e24
    )
    
    bodies = [Sol, Earth, Mars, Venus]
    window = SystemAnimation(bodies)
    window.show()
    
    sys.exit(app.exec_())
    

        
    
