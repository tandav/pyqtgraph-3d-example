import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import sys



class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        self.setWindowTitle('Earth Cities')

        self.w = gl.GLViewWidget()
        # self.w.opts['distance'] = 100

        # grid_shift = 100
        grid_shift = 40
        grid_spacing = 4

        gx = gl.GLGridItem()
        gx.setSize(grid_shift, grid_shift, grid_shift)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-grid_shift/2, 0, grid_shift/2)
        gx.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.setSize(grid_shift, grid_shift, grid_shift)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -grid_shift/2, grid_shift/2)
        gy.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.setSize(grid_shift, grid_shift, grid_shift)
        gz.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        # gz.translate(0, 0, -grid_shift/2)
        self.w.addItem(gz)


        self.main_scatter_plot = gl.GLScatterPlotItem()
        self.color = (1, 0.7, 0.4, 1)


        x = np.load('X.npy')
        x = x * 10
        print(x.shape)
        # ind = np.random.choice(x.shape[0], size=40_000, replace=False)
        # x = x[ind]

        self.main_scatter_plot.setData(pos=x, size=0.01, color=self.color, pxMode=False)

        self.w.addItem(self.main_scatter_plot)

        # self.a = np.random.randint(0, 100, (400, 200))
        # self.glayout = pg.GraphicsLayoutWidget()

        # self.pplot = self.glayout.addPlot()

        # self.pplot.setYRange(0, 500)
        # self.pplot.setXRange(0, 500)

        # self.pplot.setAspectLocked()
        # self.pplot.setMouseEnabled(x=False, y=False)
        # self.pplot.setMenuEnabled(False)
        # self.pplot.setLogMode(y=True, x=False)

        # self.pplot.setXRange(0, 200, padding=0)
        # self.pplot.setYRange(0, 400, padding=0)

        # self.pplot.invertY(True)
        # self.img.setRect(pg.QtCore.QRectF(0, 0, self.a.shape[0] - 1, self.a.shape[1] - 1))
        # self.img.setRect(pg.QtCore.QRectF(0, config.min_hz, self.a.shape[0] - 1, config.max_hz))
        # self.pplot.addItem(self.img)
        # print(self.pplot.viewGeometry())
        # self.plot()

        # self.pcurve = self.pplot.plot()

        # set the layout
        layout = QVBoxLayout()
        # layout.addWidget(self.plot)
        # layout.addWidget(self.glayout)
        layout.addWidget(self.w)

        self.setLayout(layout)


        self.setGeometry(0, 0, 1200, 800)




app = QtGui.QApplication(sys.argv)
# QtGui.QApplication.instance().exec()
gui = Window()
gui.show()
app.exec()
