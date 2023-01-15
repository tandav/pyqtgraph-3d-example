import sys
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PyQt6.QtGui import QFont

import time


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel('Test')
        font = QFont("SF Mono", 18) 
        self.label.setFont(font)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setGeometry(0, 0, 600, 400)

    def keyPressEvent(self, event):
        x = f'{event.key()} pressed at {time.time()}'
        self.label.setText(x)
        print(x)

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec())
