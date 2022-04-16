import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import sys
import pickle


with open('graph.pkl', 'rb') as f:
    graph = pickle.load(f)


class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        # pg.setConfigOption('background', 'w')
        # pg.setConfigOption('foreground', 'k')
        
        self.setWindowTitle('Earth Cities')

        self.w = gl.GLViewWidget()
        # self.w.opts['distance'] = 100

        grid_shift = 100
        grid_spacing = 4

        gx = gl.GLGridItem(color=(255, 255, 255, 0.1))
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

        X = pd.read_csv('X.csv', index_col=0)
        # tup = tuple(X.index)
        # X = np.load('X.npy')
        # X = np.random.random((1000, 3))
        # X = X * 10
        # print(x.shape)

        # ind = np.random.choice(X.shape[0], size=40_000, replace=False)
        # X = X[ind]
        self.main_scatter_plot.setData(pos=X.values, size=0.05, color=self.color, pxMode=False)
        self.w.addItem(self.main_scatter_plot)

        # txtitem2 = gl.GLTextItem()
        # txtitem2.setData(pos=(1.0, -1.0, 2.0), color=(127, 255, 127, 255), text='text2')
        # self.w.addItem(txtitem2)

        for row in X.itertuples():
            t = gl.GLTextItem()
            t.setData(pos=(row.x, row.y, row.z), color=(127, 255, 127, 255), text=row.Index)
            self.w.addItem(t)


        for k, v in graph.items():
            for vv in v:
                pts = np.linspace(X.loc[k].values, X.loc[vv].values)
                p = gl.GLLinePlotItem(pos=pts, color=(1, 1, 1, 0.3), width=2., antialias=True)
                self.w.addItem(p)

            # i = tup.index(k)
            # js = [tup.index(vv) for vv in v]

            # for j in js:
            #
            #     pts = np.linspace(x.loc[k], [row.x, row.y, row.z])
            #     plt.plot([e[i, 0], e[j, 0]], [e[i, 1], e[j, 1]])


        # pts = np.linspace([0, 0, 0], [row.x, row.y, row.z])
        # p = gl.GLLinePlotItem(pos=pts, width=1., antialias=True)
        # self.w.addItem(p)

        layout = QVBoxLayout()
        layout.addWidget(self.w)
        self.setLayout(layout)
        self.setGeometry(0, 0, 1920, 1080)


app = QtGui.QApplication(sys.argv)
gui = Window()
gui.show()
app.exec()
