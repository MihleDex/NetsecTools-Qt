import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from pythonping import ping
import socket
import subprocess
import clipboard
import myport


class HomePage(QtWidgets.QMainWindow):
    def __init__(self):
        super(HomePage, self).__init__() 
        loadUi('homepage.ui', self) #Load Ui FIle
        self.show() #SHow Window
        self.w = None 
        self.pingButton.clicked.connect(self.show_pingPage)
        self.port_btn.clicked.connect(self.show_portPage)

    def get_url(self):
        self.url = self.lineEdit.text()
        self.url = self.url.strip("http://")
        self.url = self.url.strip("https://")
        try:
            self.url = socket.gethostbyname(self.url)
            return self.url
        except socket.error:
            print("error")

    def show_pingPage(self):
        if self.w is None:
            self.w = PingPage()
        self.url = self.get_url()
        
        try:
            self.resp = self.w.ping_url(self.url)
            self.w.label_2.setText(self.resp.decode('UTF-8'))
            self.w.copy_btn.clicked.connect(lambda: clipboard.copy(self.w.label_2.text()))
            self.w.show() #change window
            self.close()
        except Exception as e:
            self.show_popup(e)

    def show_portPage(self):
        if self.w is None:
            self.w = PortScannerPage()
        self.url = self.get_url()
        self.results=myport.Scanner(self.url,1,500,3)
        
        if self.url != None:
            self.results.scan()
            self.w.label_2.setText(str(self.results.open_ports))
            self.w.copy_btn.clicked.connect(lambda: clipboard.copy(self.w.label_2.text()))
            self.w.show() #change window
            self.close()
        else:
            self.show_popup(self.url)


    def show_popup(self,msg):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setText("Error! Please check your internet or your url.")
        x = msg_box.exec_()



class PingPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(PingPage,self).__init__()
        loadUi('pingpage.ui',self)
        self.back_btn.clicked.connect(self.show_homePage)
        

    def show_homePage(self):
        self.w = HomePage()
        self.show()
        self.close()

    def ping_url(self,url):
        try:
            ping_response = subprocess.Popen(["ping", url, "-c", '5'], stdout=subprocess.PIPE).stdout.read()
            return ping_response
        except Exception as e:
            return e

    def copy_to_clipboard(self,results):
        clipboard.copy(results)

class PortScannerPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(PortScannerPage,self).__init__()
        loadUi('portpage.ui',self)
        self.back_btn.clicked.connect(self.show_homePage)

    def show_homePage(self):
        self.w = HomePage()
        self.show()
        self.close()

    def copy_to_clipboard(self,results):
        clipboard.copy(results)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    sys.exit(app.exec_())
