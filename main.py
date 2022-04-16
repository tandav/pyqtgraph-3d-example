import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QSlider
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import sys
import pickle
import json
import itertools
from pathlib import Path


with open('graph.pkl', 'rb') as f:
    graph = pickle.load(f)


class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        # pg.setConfigOption('background', 'w')
        # pg.setConfigOption('foreground', 'k')
        
        self.setWindowTitle('Earth Cities')

        # self.data_file = Path('X.csv')
        self.data_file = Path('tiers.json')
        self.data_file_mtime = None


        self.w = gl.GLViewWidget()

        # self.sp = QSlider()

        self.layout = QHBoxLayout()
        # self.right_layout = QVBoxLayout()
        # self.left_layout = QVBoxLayout()
        #
        # self.left_layout.addWidget(self.w)
        # self.right_layout.addWidget(self.sp)
        #
        # self.layout.addLayout(self.left_layout)
        # self.layout.addLayout(self.right_layout)

        # layout = QVBoxLayout()
        self.layout.addWidget(self.w)

        self.setLayout(self.layout)
        self.setGeometry(0, 0, 1920, 1080)
        self.update()
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def make_axes_grids(self, grid_shift = 50, grid_spacing = 1):
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

    def update(self) -> None:
        mtime = self.data_file.stat().st_mtime
        if mtime == self.data_file_mtime:
            print('no update, return')
            return
        self.data_file_mtime = mtime
        print('update')

        # X = pd.read_csv(self.data_file, index_col=0)

        with open(self.data_file) as f:
            tiers = json.load(f)

        data, index = [], []

        for tier in tiers:
            points_names = tier['points']
            index += points_names
            n = len(points_names)

            points = []
            for i in range(n):
                points.append(tier['radius'] * np.exp(2j * np.pi * i / n))
            points = np.array(points)
            points = points * np.exp(2j * tier['rotation'])

            data += zip(points.real, points.imag, itertools.repeat(tier['z']))

        X = pd.DataFrame(data, index, columns=list('xyz'))

        # self.w.opts['viewport'] = (0, 0, 200, 300)
        # self.w.opts['distance'] = 150
        self.w.clear()
        self.make_axes_grids()

        self.main_scatter_plot = gl.GLScatterPlotItem()
        self.color = (1, 0.7, 0.4, 1)
        self.w.addItem(self.main_scatter_plot)


        self.main_scatter_plot.setData(pos=X.values, size=0.05, color=self.color, pxMode=False)

        for row in X.itertuples():
            t = gl.GLTextItem()
            t.setData(pos=(row.x, row.y, row.z), color=(127, 255, 127, 255), text=row.Index)
            self.w.addItem(t)

        for k, v in graph.items():
            for vv in v:
                pts = np.linspace(X.loc[k].values, X.loc[vv].values)
                p = gl.GLLinePlotItem(pos=pts, color=(1, 1, 1, 0.3), width=2., antialias=True)
                self.w.addItem(p)

        # for k, v in graph.items():
        # for vv in v:



app = QtGui.QApplication(sys.argv)
gui = Window()
gui.show()
app.exec()
