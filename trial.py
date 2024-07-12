import os
import sys

import pandas as pd
import numpy as np

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QPointF
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QAbstractItemView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from random import randint

from automation import Ui_MainWindow

class MyPlotWidget(pg.PlotWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ref_point = QPointF()
        self.start_point = QPointF()
        self.end_point = QPointF()

        self.ref_line = pg.InfiniteLine(pen = 'r')
        self.ref_line.setMovable(False)

        self.end_line = pg.InfiniteLine(pen = 'b')
        self.end_line.setMovable(False)

        self.radio_status = 1

        # self.scene() is a pyqtgraph.GraphicsScene.GraphicsScene.GraphicsScene
        self.scene().sigMouseClicked.connect(self.mouse_clicked)

    def mouse_clicked(self, mouseClickEvent):
        vb = self.plotItem.vb
        scene_coords = mouseClickEvent.scenePos()

        #if self.graphWidget.sceneBoundingRect().contains(scene_coords):
        mouse_point = vb.mapSceneToView(scene_coords)
        print(f'clicked plot X: {mouse_point.x()}, Y: {mouse_point.y()}, event: {mouseClickEvent}')

        if mouseClickEvent.double() :
            print("Double clicked!!!")
            print(self.end_line.value())
            if (self.end_line.value() != None) :
                if(self.radio_status !=3) :
                    self.ref_point = mouse_point
                    self.removeItem(self.ref_line)
                    self.removeItem(self.end_line)
                    self.ref_line.setPos(mouse_point.x())
                    self.addItem(self.ref_line)
                else :
                    self.end_point = mouse_point
                    self.end_line.setPos(mouse_point.x())
                    self.addItem(self.end_line)
            else :
                pass

class MainWindow(QMainWindow, Ui_MainWindow) :
    
    def __init__(self, *args, obj = None, **kwargs) :
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #self.graphWidget.end_line = pg.InfiniteLine(pen = 'b')
        self.avg_period = np.float64(600)

        ## Raw data file explore
        self.pushButton_11.pressed.connect(self.load_files)
        self.pushButton.pressed.connect(self.import_file)

        ## Select channels to be plotted
        self.listView.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.pushButton_2.pressed.connect(self.plotting)

        ## Set the averaging period
        self.Forward.pressed.connect(self.averaging_forward)

        # Select the averaging period
        self.radioButton.clicked.connect(self.radio_check)
        self.radioButton_2.clicked.connect(self.radio_check)
        self.radioButton_3.clicked.connect(self.radio_check)
        

    def load_files(self) :
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', filter = "Comma Separated files(*.csv)")
        self.lineEdit.setText(self.fname[0])

    def import_file(self) :
        print(self.fname[0])
        self.df = pd.read_csv(self.fname[0], sep=',', encoding = 'CP949',  low_memory=False)
        self.df = self.df.apply(pd.to_numeric)

        self.model = QStandardItemModel()
        for column in self.df.columns :
            self.model.appendRow(QStandardItem(column))
        self.listView.setModel(self.model)

    def plotting(self) :

        if self.verticalLayout.isEmpty() :
            self.graphWidget = MyPlotWidget()
            self.verticalLayout.addWidget(self.graphWidget)
        else :
            self.verticalLayout.removeWidget(self.graphWidget)

        indexes = self.listView.selectedIndexes()
        for item in indexes :
            print(item.row())
            i = item.row()
            x = self.df.iloc[:, 0]
            y = self.df.iloc[:, i]
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            rand_color = (r, g, b) 

            self.plot(x, y, item.column, rand_color)

    def plot(self, x, y, plotname, color) :
        pen = pg.mkPen(color = color)
        self.graphWidget.plot(
            x,
            y,
            name = plotname,
            pen = pen
        )
    
    def radio_check(self) :
        if (self.radioButton.isChecked()) :
            self.graphWidget.radio_status = 1
            self.avg_period = np.float64(600)
        elif (self.radioButton_2.isChecked()) :
            self.graphWidget.radio_status = 2
            self.avg_period = np.float64(300)
            print("300 is checked!")
        elif (self.radioButton_3.isChecked()) :
            self.graphWidget.radio_status = 3
            self.avg_period = np.float64(0)

    def averaging_forward(self) :
        self.graphWidget.start_point = self.graphWidget.ref_point
        self.graphWidget.end_point = self.graphWidget.start_point
        if (self.avg_period != np.float64(0)) :
            print(self.avg_period)
            self.graphWidget.end_point.setX(self.graphWidget.start_point.x() + self.avg_period)
            self.graphWidget.end_line.setPos(self.graphWidget.end_point.x())
            self.graphWidget.addItem(self.graphWidget.end_line)
        else :
            print(self.avg_period)

              
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()