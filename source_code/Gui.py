from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication,QWidget,QTableWidget,QVBoxLayout,QLabel,QPushButton,QTableWidgetItem,QMessageBox
import get_passwords as gp
import sys
import clipboard


class Aplicacion(QWidget):
    def __init__(self):
        super(Aplicacion,self).__init__()
        self.window_configuration()

    def window_configuration(self):
        self.setWindowTitle("Passwords Getter")
        self.resize(400,200)
        self.setWindowIcon(QIcon("lock-unlock-fill.ico"))
        self.setStyleSheet("""
        background-color: white;
        color: black;""")
        self.show_widgets()
        

    def show_widgets(self):
        self.label = QLabel()
        self.label.setText("press refresh to see the saved passwords, make click to copy")
        self.label.move(50,50)
        self.label.setStyleSheet("border:6px solid black;")
        self.label.setFont(QFont("Consolas",10))

        self.table = QTableWidget()
        self.table.itemSelectionChanged.connect(self.item_selected)
        self.table.setStyleSheet("""background-color: black;
        color: grey;
        border-style: double;
        border-width: 2px;
        border-radius: 2px;
        font: 20px "Consolas";""")
        
        self.button = QPushButton("Refresh")
        self.button.move(50,150)   
        self.button.clicked.connect(self.refresh)    
        self.button.setFont(QFont("Consolas",10)) 
        self.button.setStyleSheet("QPushButton{border: 2px solid black;}QPushButton:pressed{background-color: black;color: white;border:2px solid black}")
        
        lay1 = QVBoxLayout()
        lay2 = QVBoxLayout()
        lay3 = QVBoxLayout()
        lay1.addWidget(self.label)
        lay2.addWidget(self.table)
        lay1.addWidget(self.button)
        lay3.addLayout(lay1)
        lay3.addLayout(lay2)
        self.setLayout(lay3)


    def item_selected(self):
        try:
            item = self.table.selectedItems()
            clipboard.copy(str(item[0].text()))
        except IndexError:
            clipboard.copy("Nothing Selected")

    def refresh(self):
        profiles = gp.obtenerPerfiles()
        if gp.verificarPerfiles(profiles):
            profileList = gp.obtenerSSID(profiles)
            passwordsList = gp.obtenerPassword(profileList)
            self.show_passwords(profileList,passwordsList)
        else:
            message = QMessageBox(self)
            message.setWindowTitle("Warning")
            message.setText("There is no passwords saved")
            message.setFont(QFont("Consolas",10))
            message.show()

    def show_passwords(self,profileList,passwordsList):   
        self.table.setColumnCount(2)       
        self.table.setRowCount(len(profileList))
        x = 0
        for profile,password in zip(profileList,passwordsList):
            self.table.setItem(x,0, QTableWidgetItem(profile))
            self.table.setItem(x,1, QTableWidgetItem(password))
            x+=1
        self.table.setHorizontalHeaderLabels(["NETWORK","PASS"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.resizeColumnsToContents()

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Aplicacion()
    win.show()
    sys.exit(app.exec_())