import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QAction, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MainWindow(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)

        self.title = 'test'
        self.left = 10
        self.top = 10
        self.width = 1920
        self.height = 1080

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=10, height=8)
        m.move(0,100)

        self.statusBar().showMessage('Ready')

        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)


        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)

        self.nameLabel2 = QLabel(self)
        self.nameLabel2.setText('Result')
        #self.line2 = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        #self.line2.move(500, 20)
        #self.line2.resize(500, 32)
        self.nameLabel2.move(500, 20)

        pybutton = QPushButton('Click me', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50)

    def clickMethod(self):
        print('Clicked Pyqt button.')
        if((self.line.text() == '')):
            self.statusBar().showMessage('Not a Number')
        else:
            print('Number: ' + str(float(self.line.text())*2))
            self.statusBar().showMessage('Introduction of a number')
            self.nameLabel2.setText(str(float(self.line.text())*2))


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        #self.addWidget(toolbar)


        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(250)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-', linewidth = 0.5)
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_())
#The code has a button, a statusbar, a matplotlib plot and a QlineEdit.