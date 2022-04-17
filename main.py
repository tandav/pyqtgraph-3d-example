"""
TODO: rewrite some strings eg CA,B, CAB, here CAB should be renamed to CBA
"""

import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from  PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import sys
import pickle
import json
import itertools
from functools import partial
from pathlib import Path

'''
[
    {"points": ["C", "D", "E", "F", "G", "A", "B"], "radius": 7, "rotation": 0, "z": 0},
    {"points": ["CD", "CB", "DE", "EF", "FG", "GA", "AB"], "radius": 6, "rotation": 0.7, "z": 3},
    {"points": ["CE", "CA", "DF", "DB", "EG", "FA", "GB"], "radius": 4, "rotation": 0.2, "z": 6},
    {"points": ["CF", "CG", "DG", "DA", "EA", "EB", "FB"], "radius": 2, "rotation": 7, "z": 9}
]
'''

with open('graph.pkl', 'rb') as f:
    graph = pickle.load(f)


def fit(v, oldmin, oldmax, newmin=0.0, newmax=1.0):
    return (v - oldmin) * (newmax - newmin) / (oldmax - oldmin) + newmin


def update_tier(
    R: pd.DataFrame,  # in polar form
    tier: int,
    radius: float | None = None,
    angle_offset: float | None = None,
    z: float | None = None,
):
    R = R.copy()
    if radius is not None:
        R.loc[R.tier == tier, 'radius'] = radius
    if angle_offset is not None:
        R.loc[R.tier == tier, 'angle'] = R.loc[R.tier == tier, 'angle'] + angle_offset
    if z is not None:
        R.loc[R.tier == tier, 'z'] = z
    C = R['radius'] * (np.cos(R['angle']) + 1j * np.sin(R['angle']))
    R['x'] = C.values.real
    R['y'] = C.values.imag

    return R


class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        # pg.setConfigOption('background', 'w')
        # pg.setConfigOption('foreground', 'k')
        
        self.setWindowTitle('Earth Cities')

        # self.data_file = Path('X.csv')
        self.data_file = Path('X3.csv')
        self.X = pd.read_csv(self.data_file, index_col=0)
        self.tiers = self.X['tier'].unique().tolist()
        # self.data_file = Path('tiers.json')
        self.data_file_mtime = None
        self.n_range = 1000

        self.w = gl.GLViewWidget()


        # self.sp = QSlider(orientation=Qt.Orientation.Horizontal)
        # sliders_width = 300
        # self.sp.setFixedWidth(sliders_width)

        self.values = dict()
        self.sliders = dict()
        self.labels = dict()
        self.ranges = {
            'z': (0, 50),
            'radius': (0, 50),
            'angle': (-np.pi, + np.pi),
        }

        self.layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.addWidget(self.w)
        # self.right_layout.addWidget(self.sp)
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

        # layout = QVBoxLayout()
        # self.layout.addWidget(self.w)

        self.setLayout(self.layout)
        self.setGeometry(0, 0, 2500, 1600)

        self.make_sliders()
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


    def slider_changed(self, tier: int, slider: str):
        v = self.sliders[tier, slider].value()
        self.values[tier, slider] = fit(v, 0, self.n_range, *self.ranges[slider])

        print('slider_changed', tier, slider, v)
        self.X = update_tier(self.X, tier, **{slider: self.values[tier, slider]})

        self.update(read_file=False)
        # self.s = fit(self.s_slider.value(), 0, self.sliders_positions, self.s_min, self.s_max)
        # self.y_slice = self.y_slice_slider.value()
        # self.y_slice_label.setText(f'Y axis [{self.y_axis_name[0]} - {self.y_axis_name[1]}] Slice: {self.y_slice + 1}/{self.data.shape[1]}')
        # self.y_slice_img.setImage(self.data[:, self.y_slice, :])
        # self.print_mean()
        # self.update_observ_slice_plot()
        # self.update_slice_helpers_lines()

    def make_sliders(self):
        # tier_chords = X.reset_index().groupby('tier')['index'].aggregate(list).tolist()
        for tier in self.tiers:
            tier_layout = QVBoxLayout()
            slider_layout = QHBoxLayout()

            self.sliders[tier, 'z'] = QSlider(orientation=Qt.Orientation.Horizontal)
            self.sliders[tier, 'radius'] = QSlider(orientation=Qt.Orientation.Horizontal)
            self.sliders[tier, 'angle'] = QSlider(orientation=Qt.Orientation.Horizontal)

            # self.sliders[tier, 'z'].setObjectName(f'{tier} z')

            # z_slider.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')
            # radius_slider.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')
            # angle_slider.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')

            self.sliders[tier, 'z'].setRange(0, self.n_range)
            self.sliders[tier, 'radius'].setRange(0, self.n_range)
            self.sliders[tier, 'angle'].setRange(0, self.n_range)

            self.values[tier, 'z'] = self.X[self.X.tier == tier].z.mean()
            self.values[tier, 'radius'] = self.X[self.X.tier == tier].radius.mean()
            self.values[tier, 'angle'] = 0

            self.sliders[tier, 'z'].setValue(int(fit(self.values[tier, 'z'], *self.ranges['z'], 0, self.n_range)))
            self.sliders[tier, 'radius'].setValue(int(fit(self.values[tier, 'radius'], *self.ranges['radius'], 0, self.n_range)))
            self.sliders[tier, 'angle'].setValue(int(fit(self.values[tier, 'angle'], *self.ranges['angle'], 0, self.n_range)))

            self.sliders[tier, 'z'].setTickPosition(QSlider.TickPosition.TicksBelow)
            self.sliders[tier, 'radius'].setTickPosition(QSlider.TickPosition.TicksBelow)
            self.sliders[tier, 'angle'].setTickPosition(QSlider.TickPosition.TicksBelow)

            self.sliders[tier, 'z'].setTickInterval(25)
            self.sliders[tier, 'radius'].setTickInterval(25)
            self.sliders[tier, 'angle'].setTickInterval(25)

            # z_slider.setRange(0, 100)
            # radius_slider.setRange(0, 50)
            # angle_slider.setRange(-np.pi, +np.pi)

            # self.z_slice_slider = QtGui.QSlider()
            # self.z_slice_slider.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')
            # self.z_slice_slider.setRange(0, self.data.shape[0] - 1)
            # self.z_slice_slider.setValue(self.z_slice)
            # self.z_slice_slider.setTickPosition(QtGui.QSlider.TicksBelow)
            # self.z_slice_slider.setTickInterval(1)

            # self.b_slider.setRange(0, self.sliders_positions)
            # self.b_slider.setValue(util.fit(self.b, self.b_min, self.b_max, 0, self.sliders_positions))
            # self.b_slider.setTickInterval(0.01)

            self.sliders[tier, 'z'].setFixedWidth(200)
            self.sliders[tier, 'radius'].setFixedWidth(200)
            self.sliders[tier, 'angle'].setFixedWidth(200)

            self.sliders[tier, 'z'].valueChanged.connect(partial(self.slider_changed, tier, 'z'))
            self.sliders[tier, 'radius'].valueChanged.connect(partial(self.slider_changed, tier, 'radius'))
            self.sliders[tier, 'angle'].valueChanged.connect(partial(self.slider_changed, tier, 'angle'))

            # self.sliders[tier, 'z'].valueChanged.connect(lambda: self.slider_changed(tier, 'z'))
            # self.sliders[tier, 'radius'].valueChanged.connect(lambda: self.slider_changed(tier, 'radius'))
            # self.sliders[tier, 'angle'].valueChanged.connect(lambda: self.slider_changed(tier, 'angle'))

            self.labels[tier, 'z'] = QLabel(text=f"z {self.values[tier, 'z']:.2f}")
            self.labels[tier, 'radius'] = QLabel(text=f"radius {self.values[tier, 'radius']:.2f}")
            self.labels[tier, 'angle'] = QLabel(text=f"angle {self.values[tier, 'angle']:.2f}")

            self.labels[tier, 'z'].setFixedWidth(50)
            self.labels[tier, 'radius'].setFixedWidth(80)
            self.labels[tier, 'angle'].setFixedWidth(80)

            slider_layout.addWidget(self.labels[tier, 'z'])
            slider_layout.addWidget(self.sliders[tier, 'z'])
            slider_layout.addWidget(self.labels[tier, 'radius'])
            slider_layout.addWidget(self.sliders[tier, 'radius'])
            slider_layout.addWidget(self.labels[tier, 'angle'])
            slider_layout.addWidget(self.sliders[tier, 'angle'])

            label = QLabel(text=' '.join(self.X[self.X.tier == tier].index))

            label.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')

            tier_layout.addWidget(label)
            tier_layout.addLayout(slider_layout)

            self.right_layout.addLayout(tier_layout)

            # TODO: add save csv button

    def update_sliders(self):
        for tier in self.tiers:
            self.labels[tier, 'z'].setText(f"z {self.values[tier, 'z']:.2f}")
            self.labels[tier, 'radius'].setText(f"radius {self.values[tier, 'radius']:.2f}")
            self.labels[tier, 'angle'].setText(f"angle {self.values[tier, 'angle']:.2f}")

    def update_plot(self):
        # data, index = [], []
        #
        # for tier in tiers:
        #     points_names = tier['points']
        #     index += points_names
        #     n = len(points_names)
        #
        #     points = []
        #     for i in range(n):
        #         points.append(tier['radius'] * np.exp(2j * np.pi * i / n))
        #     points = np.array(points)
        #     # rot = 2 * np.pi / tier['rotation'] if tier['rotation'] else 0
        #     rot = 2 * np.pi * tier['rotation']
        #     points = points * np.exp(1j * rot)
        #
        #     data += zip(points.real, points.imag, itertools.repeat(tier['z']))
        #
        # X = pd.DataFrame(data, index, columns=list('xyz'))

        # self.w.opts['viewport'] = (0, 0, 200, 300)
        # self.w.opts['distance'] = 150
        self.w.clear()
        # self.make_axes_grids()

        self.main_scatter_plot = gl.GLScatterPlotItem()
        self.color = (1, 0.7, 0.4, 1)
        self.w.addItem(self.main_scatter_plot)


        self.main_scatter_plot.setData(pos=self.X[list('xyz')].values, size=0.05, color=self.color, pxMode=False)

        for row in self.X.itertuples():
            t = gl.GLTextItem()
            t.setData(pos=(row.x, row.y, row.z), color=(127, 255, 127, 255), text=row.Index)
            self.w.addItem(t)

        for k, v in graph.items():
            for vv in v:
                pts = np.linspace(self.X.loc[k, list('xyz')].values, self.X.loc[vv, list('xyz')].values)
                p = gl.GLLinePlotItem(pos=pts, color=(1, 1, 1, 0.3), width=2., antialias=True)
                self.w.addItem(p)

        # for k, v in graph.items():
        # for vv in v:
    def update(self, read_file: bool = True) -> None:
        if read_file:
            mtime = self.data_file.stat().st_mtime
            if mtime == self.data_file_mtime:
                print('no update, return')
                return
            self.data_file_mtime = mtime
            print('update')
            self.X = pd.read_csv(self.data_file, index_col=0)

        self.update_sliders()
        self.update_plot()
        # with open(self.data_file) as f:
        #     tiers = json.load(f)





app = QtGui.QApplication(sys.argv)
gui = Window()
gui.show()
app.exec()
