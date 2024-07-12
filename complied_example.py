import os
import sys

import pandas as pd
import numpy as np

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

from automation import Ui_MainWindow

class TableModel(QtCore.QAbstractTableModel) :
    def __init__(self, data) :
        super().__init__()
        self._data = data

    def data(self, index, role) :
        if role == Qt.ItemDataRole.DisplayRole :
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        
    def rowCount(self, index) :
        return self._data.shape[0]
    
    def columnCount(self, index) :
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role) :
        if role == Qt.ItemDataRole.DisplayRole :
            if orientation == Qt.Orientation.Horizontal :
                return str(self._data.columns[section])
            
            if orientation == Qt.Orientation.Vertical :
                return str(self._data.index[section])
    
class HeaderProxyModel(QtCore.QIdentityProxyModel):

    checked = QtCore.pyqtSignal(int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.checks = {}

    def columnCount(self, index=QtCore.QModelIndex()):
        return 1
    """
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.headerData(index.row(), Qt.Orientation.Vertical, role)
        elif role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            return self.checks.get(
                QtCore.QPersistentModelIndex(index), Qt.Unchecked
            )
    """
            
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):

        if not index.isValid():
            return False
        if role == Qt.ItemDataRole.CheckStateRole:
            self.checks[QtCore.QPersistentModelIndex(index)] = value
            self.checked.emit(index.row(), bool(value))
            return True
        return False
    """
    def flags(self, index):
        fl = super().flags(index)
        if index.column() == 0:
            fl |= Qt.ItemIsEditable | Qt.ItemIsUserCheckable
        return fl
    """

class MainWindow(QMainWindow, Ui_MainWindow) :
    def __init__(self, *args, obj = None, **kwargs) :
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        ## Raw data file explore
        self.pushButton_11.pressed.connect(self.load_files)
        self.pushButton.pressed.connect(self.import_file)

    def load_files(self) :
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', filter = "Comma Separated files(*.csv)")

    def import_file(self) :
        print(self.fname[0])
        self.df = pd.read_csv(self.fname[0], sep=',')
        # TableModel 만들때, 왜 첫행(column 행)을 날리고 시작하지?
        self.model = TableModel(self.df.T)

        ##headers = HeaderProxyModel()
        ##headers.setSourceModel(self.model)
        
        transpose = QtCore.QTransposeProxyModel()
        transpose.setSourceModel(self.model)
        
        self.listView.setModel(transpose)

        #nColumn = self.model.columnCount(0)
        #ColumnList = self.model.headerData(section = range(0, nColumn), orientation = Qt.Orientation.Horizontal, role = Qt.ItemDataRole.DisplayRole)
        #self.listView.setModel(self.model.headerData(section = range(0, nColumn), orientation = Qt.Orientation.Horizontal, role = Qt.ItemDataRole.DisplayRole))
              
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()