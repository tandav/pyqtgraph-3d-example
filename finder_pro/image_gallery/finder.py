from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

THUMBNAIL_SIZE = 128
SPACING = 10
IMAGES_PER_ROW = 5

class TableWidget(QTableWidget):
    def init(self, parent=None, **kwargs):
        QTableWidget.init(self, parent, **kwargs)
        self.setIconSize(QSize(128,128))
        self.setColumnCount(IMAGES_PER_ROW)
        self.setGridStyle(Qt.NoPen)

        # Set the default column width and hide the header
        self.verticalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.verticalHeader().hide()

        # Set the default row height and hide the header
        self.horizontalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.horizontalHeader().hide()

        # Set the table width to show all images without horizontal scrolling
        self.setMinimumWidth((THUMBNAIL_SIZE+SPACING)*IMAGES_PER_ROW+(SPACING*2))

    def addPicture(self, row, col, picturePath):
        item=QTableWidgetItem()

        # Scale the image by either height or width and then 'crop' it to the
        # desired size, this prevents distortion of the image.
        p=QPixmap(picturePath)
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        item.setIcon(QIcon(p))

        self.setItem(row,col,item)

class MainWindow(QMainWindow):
    def init(self, parent=None, **kwargs):
        QMainWindow.init(self, parent, **kwargs)
        centralWidget=QWidget(self)
        l=QVBoxLayout(centralWidget)

        self.tableWidget=TableWidget(self)
        l.addWidget(self.tableWidget)

        self.setCentralWidget(centralWidget)

        picturesPath=QDesktopServices.storageLocation(QDesktopServices.PicturesLocation)
        pictureDir=QDir(picturesPath)
        pictures=pictureDir.entryList(['*.jpg','*.png','*.gif'])

        rowCount=len(pictures)//IMAGES_PER_ROW
        if len(pictures)%IMAGES_PER_ROW: rowCount+=1
        self.tableWidget.setRowCount(rowCount)

        row=-1
        for i,picture in enumerate(pictures):
            col=i%IMAGES_PER_ROW
            if not col: row+=1
            self.tableWidget.addPicture(row, col, pictureDir.absoluteFilePath(picture))

if __name__ == '__main__':
    from sys import argv, exit

    a=QApplication(argv)
    m=MainWindow()
    m.show()
    m.raise_()
    exit(a.exec_())
