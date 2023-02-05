import os
import sys

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout


def random_sphere(r: float = 1, n_points: int = 100_000) -> np.ndarray:
    """Generate random points on a sphere surface"""
    theta = np.random.uniform(0, 2 * np.pi, n_points)
    phi = np.random.uniform(0, 2 * np.pi, n_points)
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    return np.c_[x, y, z]


def torus(R: float = 3, r: float = 1, n_points: int = 100_000) -> np.ndarray:
    """Generate points on a torus surface"""
    theta = np.random.uniform(0, 2 * np.pi, n_points)
    phi = np.random.uniform(0, 2 * np.pi, n_points)
    x = (R + r * np.cos(theta)) * np.cos(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    return np.c_[x, y, z]


class Window(QDialog):
    def __init__(self):
        super().__init__()

        # pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.setWindowTitle('3D Plot')

        self.w = gl.GLViewWidget()
        # self.w.opts['distance'] = 100

        grid_shift = 100
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

        # x = random_sphere(r=10)
        x = torus(3, 1)

        self.main_scatter_plot.setData(
            pos=x, size=0.01, color=self.color, pxMode=False,
        )
        self.w.addItem(self.main_scatter_plot)
        layout = QVBoxLayout()
        layout.addWidget(self.w)
        self.setLayout(layout)
        self.setGeometry(0, 0, 1200, 800)

        if 'TEST' in os.environ:
            self.counter = 0
            self.timer = QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(1000)

    def update(self, exit_after: int = 3):
        if self.counter == exit_after:
            raise SystemExit
        self.counter += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Window()
    gui.show()
    app.exec()
