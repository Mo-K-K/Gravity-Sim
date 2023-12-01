import sys
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog, QApplication, QFileDialog
from Secondwindow import *
from Bodies import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        '''initialises the UI'''
        
        #initialise UI
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 800, 600)
        
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        self.Window = None
        self.filenames = []
        self.bodies = []
        self.nbuttons = 5
        
        #Create menu bar with name "File" and sub menu "Add File" 
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("&File")
        self.Browse_action = self.file_menu.addAction("Add File")
        self.Browse_action.triggered.connect(self.Browseapp)
        
        #Label to show chosen file
        self.Label = QLabel("File Name: ")
        layout.addWidget(self.Label)
        
        #Label to show number of files selected and names
        self.Label2 = QLabel("files selected: ")
        layout.addWidget(self.Label2)
        
        #Create button to create second window
        self.Button = QPushButton("launch")
        layout.addWidget(self.Button)
        
        self.Button.clicked.connect(self.launch)
        
    def launch(self):
        self.GetInfoFromFile()
        self.show_second()
        
    def show_second(self):
        '''Opens the second window when the launch button is pressed'''
        if self.Window is None:
            self.Window = secondWindow(name=self.bodies, num_buttons=self.nbuttons)
        self.Window.show()
           
    
    def Browseapp(self) -> str:
        '''
        Uses QFileDialog so user can select files containing ephemerides
        '''
        #Opens file browser and saves chosen files name
        fname  = QFileDialog.getOpenFileName(self, 'Open file')
        self.Label.setText("File Name: " + fname[0])
        self.filenames.append(fname[0])
        names = ""
        for name in self.filenames:
            names = name[64:-4] + " " + names
        self.Label2.setText("Files selected: " + names)
        
    def GetInfoFromFile(self):
        '''gets information from the selected file and produces an object.
        This is done by calling the class Bodies'''
        #pos is the initial positions of the body and vec are the initial velocites
        for x in range(len(self.filenames)):
            pos=[]
            vec=[]
            names = self.filenames[x]
            name = names[5:-4]
            with open("test/Mars.txt") as file:
                for line in file:
                    if line[:4] == " X =":
                        pos.append(float(line[4:26]))
                        pos.append(float(line[30:52]))
                        pos.append(float(line[56:78]))
                    if line[:4] == " VX=":
                        vec.append(float(line[4:26]))
                        vec.append(float(line[30:52]))
                        vec.append(float(line[56:78]))
                        break
                    
            self.bodies.append(Bodies(
                position=np.array(pos),
                velocity=np.array(vec),
                acceleration=np.array([0, 0, 0]),
                name = name,
                mass = 100
            ))
        
            

        
        
        
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    
    sys.exit(app.exec_())
        