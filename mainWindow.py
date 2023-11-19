import sys
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog, QApplication, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        #initialise UI
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 800, 600)
        self.fname = None
        
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        #Create menu bar with name "File" and sub menu "Add File" 
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("&File")
        self.Browse_action = self.file_menu.addAction("Add File")
        self.Browse_action.triggered.connect(self.Browseapp)
        
        #Label to show chosen file
        self.Label = QLabel("File Name: ")
        layout.addWidget(self.Label)
        
        
    def Browseapp(self):
        #Opens file browser and saves chosen files name
        fname  = QFileDialog.getOpenFileName(self, 'Open file')
        self.Label.setText("File Name: " + str(fname[0]))
        
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())