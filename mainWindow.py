import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog, QApplication, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.app = app
        self.setWindowTitle("Main Window")
        
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        Browse_action = file_menu.addAction("Add File")
        Browse_action.triggered.connect(self.Browseapp)
        
    def Browseapp(self):
        fname  = QFileDialog.getOpenFileName(self, 'Open file')
        print("name of file", fname[0])
        
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())