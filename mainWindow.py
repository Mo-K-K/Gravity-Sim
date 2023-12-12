import sys
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog, QApplication, QFileDialog, QLineEdit, QFormLayout
from Secondwindow import *


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
        self.nbuttons = 5
        self.bodies = []
        self.masses = []
        
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
        
        self.Label3 = QLabel("Mass: ")
        
        self.Text = QLineEdit()
        layout.addStretch()
        layout.addWidget(self.Label3)
        layout.addWidget(self.Text)
        layout.addStretch()
        
        
        
        #Create button to create second window
        self.Button = QPushButton("launch")
        layout.addWidget(self.Button)
        
        
        self.Button.clicked.connect(self.launch)
        
    def launch(self):
        text = self.Text.text()
        self.masses = text.split(",")
        for x in range(len(self.masses)):
            self.masses[x] = float(self.masses[x])
        self.GetInfoFromFile()
        print(self.masses)
        print(self.bodies)
        if len(self.bodies) == len(self.masses):
            self.show_second()
        else:
            raise Exception("the incorrect number of masses entered")
        
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
            pos=np.array([0, 0, 0])
            vec=np.array([0, 0, 0])
            names = self.filenames[x]
            name = names[64:-4]
            m = self.masses[x]
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
                        break
                    
                    
            self.bodies.append(Bodies(
                position=pos*1000,
                velocity=vec*1000,
                acceleration=np.array([0, 0, 0]),
                name = name,
                mass = m
            ))
            print(self.bodies[0].position)
        

     
if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    
    sys.exit(app.exec_())
        