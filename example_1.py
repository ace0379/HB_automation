import os
import sys

from PyQt6 import QtWidgets, uic

basedir = os.path.dirname(__file__)

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi(os.path.join(basedir, "automation.ui"))
window.show()

app.exec()