from pyqtgraph.Qt import QtCore, QtGui
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
import sys
import signal
import pydicom


class AppGUI(QDialog):
    def __init__(self):
        super().__init__()

        self.X = pydicom.dcmread('dicom_data/.dcm').pixel_array

        self.z = self.X.shape[0] // 2
        self.y = self.X.shape[1] // 2
        self.x = self.X.shape[2] // 2


        self.init_ui()
        self.qt_connections()

    def init_ui(self):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('imageAxisOrder', 'row-major')

        self.zname = 'Head', 'Feet'
        self.yname = 'Face', 'Back'
        self.xname = 'Left Hand', 'Right Hand'


        self.layout = QVBoxLayout()

        self.setGeometry(0, 0, 1440, 900)
        self.setWindowTitle('DICOM Viewer')


        self.z_slice_label = QLabel(f'Z axis [{self.zname[0]} - {self.zname[1]}] Slice: {self.z + 1}/{self.X.shape[0]}')
        self.y_slice_label = QLabel(f'Y axis [{self.yname[0]} - {self.yname[1]}] Slice: {self.y + 1}/{self.X.shape[1]}')
        self.x_slice_label = QLabel(f'X axis [{self.xname[0]} - {self.xname[1]}] Slice: {self.x + 1}/{self.X.shape[2]}')


        # slices plots ----------------------------------------------------------------
        
        self.autolevels = True
        self.levels = (0, 100)
        self.glayout = pg.GraphicsLayoutWidget()
        self.glayout.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.glayout.ci.layout.setSpacing(0)

        self.zi = pg.ImageItem(self.X[self.z, :     , :     ], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='r', width=3))
        self.yi = pg.ImageItem(self.X[:     , self.y, :     ], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='g', width=3))
        self.xi = pg.ImageItem(self.X[:     , :     , self.x], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='b', width=3))
        self.zp = self.glayout.addPlot()
        self.yp = self.glayout.addPlot()
        self.xp = self.glayout.addPlot()
        # self.z_slice_plot.setTitle(f'Z axis [{self.z_axis_name[0]} - {self.z_axis_name[1]}]')
        # self.y_slice_plot.setTitle(f'Y axis [{self.y_axis_name[0]} - {self.y_axis_name[1]}]')
        # self.x_slice_plot.setTitle(f'X axis [{self.x_axis_name[0]} - {self.x_axis_name[1]}]')
        self.zp.setAspectLocked()
        self.yp.setAspectLocked()
        self.xp.setAspectLocked()

        self.zp.setMouseEnabled(x=False, y=False)
        self.yp.setMouseEnabled(x=False, y=False)
        self.xp.setMouseEnabled(x=False, y=False)

        self.z_slice_plot_y_helper1 = self.zp.plot([0        ,  self.X.shape[2]], [self.y    , self.y         ], pen='g')
        self.z_slice_plot_y_helper2 = self.zp.plot([0        ,  self.X.shape[2]], [self.y + 1, self.y + 1     ], pen='g')
        self.z_slice_plot_x_helper1 = self.zp.plot([self.x   ,  self.x         ], [0         , self.X.shape[1]], pen='b')
        self.z_slice_plot_x_helper2 = self.zp.plot([self.x + 1, self.x + 1     ], [0         , self.X.shape[1]], pen='b')
        self.y_slice_plot_z_helper1 = self.yp.plot([0        ,  self.X.shape[2]], [self.z    , self.z         ], pen='r')
        self.y_slice_plot_z_helper2 = self.yp.plot([0        ,  self.X.shape[2]], [self.z + 1, self.z + 1     ], pen='r')
        self.y_slice_plot_x_helper1 = self.yp.plot([self.x    , self.x         ], [0         , self.X.shape[0]], pen='b')
        self.y_slice_plot_x_helper2 = self.yp.plot([self.x + 1, self.x + 1     ], [0         , self.X.shape[0]], pen='b')
        self.x_slice_plot_z_helper1 = self.xp.plot([0        ,  self.X.shape[1]], [self.z    , self.z         ], pen='r')
        self.x_slice_plot_z_helper2 = self.xp.plot([0        ,  self.X.shape[1]], [self.z + 1, self.z + 1     ], pen='r')
        self.x_slice_plot_y_helper1 = self.xp.plot([self.y    , self.y         ], [0         , self.X.shape[0]], pen='g')
        self.x_slice_plot_y_helper2 = self.xp.plot([self.y + 1, self.y + 1     ], [0         , self.X.shape[0]], pen='g')

        self.zp.invertY(True)
        self.yp.invertY(True)
        self.xp.invertY(True)

        self.zp.setLabel('bottom', f'X axis [{self.xname[0]} - {self.xname[1]}]')
        self.yp.setLabel('bottom', f'X axis [{self.xname[0]} - {self.xname[1]}]')
        self.zp.setLabel('left'  , f'Y axis [{self.yname[1]} - {self.yname[0]}]')
        self.xp.setLabel('bottom', f'Y axis [{self.yname[0]} - {self.yname[1]}]')
        self.yp.setLabel('left'  , f'Z axis [{self.zname[1]} - {self.zname[0]}]')
        self.xp.setLabel('left'  , f'Z axis [{self.zname[1]} - {self.zname[0]}]')

        self.zp.addItem(self.zi)
        self.yp.addItem(self.yi)
        self.xp.addItem(self.xi)

        self.zi.setRect(pg.QtCore.QRectF(0, 0, self.X.shape[2], self.X.shape[1]))
        self.yi.setRect(pg.QtCore.QRectF(0, 0, self.X.shape[2], self.X.shape[0]))
        self.xi.setRect(pg.QtCore.QRectF(0, 0, self.X.shape[1], self.X.shape[0]))

        self.zi.setZValue(-1)
        self.yi.setZValue(-1)
        self.xi.setZValue(-1)


        self.zs = QSlider()
        self.ys = QSlider()
        self.xs = QSlider()
        self.zs.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')
        self.ys.setStyleSheet('background-color: rgba(0, 255, 0, 0.2)')
        self.xs.setStyleSheet('background-color: rgba(0, 0, 255, 0.2)')
        self.zs.setOrientation(Qt.Orientation.Horizontal)
        self.ys.setOrientation(Qt.Orientation.Horizontal)
        self.xs.setOrientation(Qt.Orientation.Horizontal)
        self.zs.setRange(0, self.X.shape[0] - 1)
        self.ys.setRange(0, self.X.shape[1] - 1)
        self.xs.setRange(0, self.X.shape[2] - 1)
        self.zs.setValue(self.z)
        self.ys.setValue(self.y)
        self.xs.setValue(self.x)
        self.zs.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ys.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.xs.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.zs.setTickInterval(1)
        self.ys.setTickInterval(1)
        self.xs.setTickInterval(1)
        self.layout.addWidget(self.zs)
        self.layout.addWidget(self.ys)
        self.layout.addWidget(self.xs)
        self.layout.addWidget(self.z_slice_label)
        self.layout.addWidget(self.y_slice_label)
        self.layout.addWidget(self.x_slice_label)
        self.layout.addWidget(self.glayout)
        self.setLayout(self.layout)

        self.show()


    def qt_connections(self):
        self.zs.valueChanged.connect(self.zs_changed)
        self.ys.valueChanged.connect(self.ys_changed)
        self.xs.valueChanged.connect(self.xs_changed)


    def wheelEvent(self, event):
        if self.zi.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.z = np.clip(self.z + np.sign(event.angleDelta().y()), 0, self.X.shape[0] - 1) # change bounds 0..N-1 => 1..N
            self.zs.setValue(self.z)
        elif self.yi.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.y = np.clip(self.y + np.sign(event.angleDelta().y()), 0, self.X.shape[1] - 1) # change bounds 0..N-1 => 1..N
            self.ys.setValue(self.y)
        elif self.xi.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.x = np.clip(self.x + np.sign(event.angleDelta().y()), 0, self.X.shape[2] - 1) # change bounds 0..N-1 => 1..N
            self.xs.setValue(self.x)


    def update_slice_helpers_lines(self):
        self.z_slice_plot_y_helper1.setData([0               , self.X.shape[2]], [self.y    , self.y         ])
        self.z_slice_plot_y_helper2.setData([0               , self.X.shape[2]], [self.y + 1, self.y + 1     ])
        self.z_slice_plot_x_helper1.setData([self.x          , self.x         ], [0         , self.X.shape[1]])
        self.z_slice_plot_x_helper2.setData([self.x + 1      , self.x + 1     ], [0         , self.X.shape[1]])
        self.y_slice_plot_z_helper1.setData([0               , self.X.shape[2]], [self.z    , self.z         ])
        self.y_slice_plot_z_helper2.setData([0               , self.X.shape[2]], [self.z + 1, self.z + 1     ])
        self.y_slice_plot_x_helper1.setData([self.x          , self.x         ], [0         , self.X.shape[0]])
        self.y_slice_plot_x_helper2.setData([self.x + 1      , self.x + 1     ], [0         , self.X.shape[0]])
        self.x_slice_plot_z_helper1.setData([0               , self.X.shape[1]], [self.z    , self.z         ])
        self.x_slice_plot_z_helper2.setData([0               , self.X.shape[1]], [self.z + 1, self.z + 1     ])
        self.x_slice_plot_y_helper1.setData([self.y          , self.y         ], [0         , self.X.shape[0]])
        self.x_slice_plot_y_helper2.setData([self.y + 1      , self.y + 1     ], [0         , self.X.shape[0]])

    def zs_changed(self):
        self.z = self.zs.value()
        self.z_slice_label.setText(f'Z axis [{self.zname[0]} - {self.zname[1]}] Slice: {self.z + 1}/{self.X.shape[0]}')
        self.zi.setImage(self.X[self.z, :, :])
        self.update_slice_helpers_lines()

    def ys_changed(self):
        self.y = self.ys.value()
        self.y_slice_label.setText(f'Y axis [{self.yname[0]} - {self.yname[1]}] Slice: {self.y + 1}/{self.X.shape[1]}')
        self.yi.setImage(self.X[:, self.y, :])
        self.update_slice_helpers_lines()

    def xs_changed(self):
        self.x = self.xs.value()
        self.x_slice_label.setText(f'X axis [{self.xname[0]} - {self.xname[1]}] Slice: {self.x + 1}/{self.X.shape[2]}')
        self.xi.setImage(self.X[:, :, self.x])
        self.update_slice_helpers_lines()




app = QApplication(sys.argv)
# print(sys.argv[1])
gui = AppGUI()
signal.signal(signal.SIGINT, signal.SIG_DFL)
sys.exit(app.exec())
