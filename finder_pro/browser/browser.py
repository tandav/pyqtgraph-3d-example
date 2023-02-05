import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QSize    
import signal
import os

class AppGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        # QMainWindow.__init__(self)

        # self.setMinimumSize(QSize(640, 480))    
        # self.setWindowTitle("Hello world") 

        # centralWidget = QWidget(self)          
        # self.setCentralWidget(centralWidget)   

        # gridLayout = QGridLayout(self)     
        # centralWidget.setLayout(gridLayout)  

        # title = QLabel("Hello World from PyQt", self) 
        # title.setAlignment(QtCore.Qt.AlignCenter) 
        # gridLayout.addWidget(title, 0, 0)
    def init_ui(self):
        print('hello')
        
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.webView = QWebEngineView(self)
        html = 'shortcuts.html'
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(os.path.abspath(html)))
        self.layout.addWidget(self.webView)

        # print(QtCore.QUrl.fromLocalFile(os.path.abspath(html)))



        self.setGeometry(0, 0, 1000, 600)
        # self.setGeometry(0, 0, 1200, 900)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = AppGUI()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec())

# import os
# from PyQt5 import QtCore, QtGui, QtWidgets

# class Ui_MainWindow(QWidgets.QWidget):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(800, 600)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
#         self.gridLayout.setObjectName("gridLayout")
#         self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
#         # self.webView.setUrl(QtCore.QUrl("http://www.google.com/"))
        
#         # print(os.path.realpath(__file__))
#         # print(os.path.abspath(__file__))
#         html = 'shortcuts.html'
#         # url = 'file://' + os.path.abspath(html)
#         # self.webView.setUrl(QtCore.QUrl(url))
#         print(QtCore.QUrl.fromLocalFile(os.path.abspath(html)))
#         self.webView.setUrl(QtCore.QUrl.fromLocalFile(os.path.abspath(html)))

#         self.webView.setObjectName("webView")
#         self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)

#         # self.setGeometry(0, 0, 1440, 900)
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

# from PyQt5 import QtWebEngineWidgets

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())



### ALSO WORKS:
# import sys

# from PyQt5.QtCore import QUrl
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWebEngineWidgets import QWebEngineView

# app = QApplication(sys.argv)
# wv = QWebEngineView()
# wv.load(QUrl("https://pypi.python.org/pypi/PyQt5"))
# wv.show()
# app.exec_()

