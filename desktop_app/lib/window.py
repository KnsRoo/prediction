import os, sys, numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QFileDialog, QGraphicsPixmapItem, QTableWidgetItem, QGraphicsView, QGraphicsScene, QDialogButtonBox,
							 QLabel, QMainWindow, QPushButton, QDialog)
from PyQt5.uic import loadUi
from io import BytesIO

#For debug only, delete later
DEBUG = False

class Window(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)
		loadUi('interface/ui.ui', self)

	@pyqtSlot()
	def open_file(self):
		QF = QFileDialog()
		temp = QF.getOpenFileName(self, 'Open file', '', 'CSV Files (*.csv)')[0]
		if not temp: return