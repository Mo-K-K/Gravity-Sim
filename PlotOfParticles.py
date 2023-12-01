import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

class SystemAnimation(QMainWindow):
    def __init__(self, nbodies):
        super().__init__()
        #
        nbodies = nbodies+1
        self.particles = np.random.rand(nbodies, 2)
        #
        self.nbodies = nbodies #number of bodies in the system
        self.colours = self.randomisecolours(exclude='navy')
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('System Animation')
        self.setGeometry(100, 100, 800, 600)
        
        #main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        #Matplotlib figure and the canvas
        self.fig, self.ax = plt.subplots(facecolor='navy')
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        
        #create animation
        self.ani = animation.FuncAnimation(self.fig, self.updatePlot, frames = 100, interval=50, blit = False)
        
        
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
        
        #send updated positions to graph class

        #
        self.particles += 0.01 * np.random.rand(self.nbodies, 2)
        #
        
        # clear plot
        self.ax.clear()
        
        self.ax.set_facecolor('navy')
        self.ax.axis('off')

        #plot particle with updated position
        self.ax.scatter(self.particles[:, 0], self.particles[:, 1], c=self.colours)

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = SystemAnimation()
    window.show()
    sys.exit(app.exec_())