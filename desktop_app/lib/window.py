import os, sys, numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPen, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QFileDialog, QGraphicsPixmapItem, QTableWidgetItem, QGraphicsView, QGraphicsScene, QDialogButtonBox,
							 QLabel, QMainWindow, QPushButton, QDialog)
from PyQt5.uic import loadUi
from io import BytesIO
from lib.model import Model

#For debug only, delete later
DEBUG = False

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.iloc[index.row()][index.column()]))
        return QtCore.QVariant()

class Window(QMainWindow):
	filepath = ''

	def __init__(self):
		QMainWindow.__init__(self)
		loadUi('interface/ui.ui', self)
		with open('interface/main.css') as f:
			ss = f.read()
			self.setStyleSheet(ss)


	@pyqtSlot()
	def on_pushButton_clicked(self):
		date1, date2 = self.lineEdit_3.text(), self.lineEdit_2.text()
		self.progressBar.setValue(4)
		model = Model(self.filepath, date1, date2)
		self.progressBar.setValue(8)
		pix = QPixmap("temp/corr.png")
		self.progressBar.setValue(12)
		item = QGraphicsPixmapItem(pix)
		self.progressBar.setValue(16)
		scene = QGraphicsScene(self)
		self.progressBar.setValue(20)
		scene.addItem(item)
		self.progressBar.setValue(24)
		self.graphicsView.setScene(scene)
		self.progressBar.setValue(28)
		self.graphicsView.fitInView(item, QtCore.Qt.KeepAspectRatio);
		self.progressBar.setValue(32)
		tableModel = PandasModel(model.get_itog_table())
		self.progressBar.setValue(36)
		self.tableView.setModel(tableModel)
		self.progressBar.setValue(40)
		self.textEdit.setText(model.get_summary())
		self.progressBar.setValue(44)
		self.lineEdit_4.setText(model.get_V())
		self.progressBar.setValue(48)
		pix = QPixmap("temp/arima.png")
		self.progressBar.setValue(52)
		item = QGraphicsPixmapItem(pix)
		self.progressBar.setValue(56)
		scene = QGraphicsScene(self)
		self.progressBar.setValue(60)
		scene.addItem(item)
		self.progressBar.setValue(64)
		self.graphicsView_2.setScene(scene)
		self.progressBar.setValue(68)
		self.graphicsView_2.fitInView(item, QtCore.Qt.KeepAspectRatio);
		self.progressBar.setValue(72)
		self.lineEdit_5.setText(model.get_rsq())
		self.progressBar.setValue(76)
		pix = QPixmap("temp/regr.png")
		self.progressBar.setValue(80)
		item = QGraphicsPixmapItem(pix)
		self.progressBar.setValue(84)
		scene = QGraphicsScene(self)
		self.progressBar.setValue(88)
		scene.addItem(item)
		self.progressBar.setValue(92)
		self.graphicsView_3.setScene(scene)
		self.progressBar.setValue(96)
		self.graphicsView_3.fitInView(item, QtCore.Qt.KeepAspectRatio);
		self.progressBar.setValue(100)


	@pyqtSlot()
	def on_pushButton_3_clicked(self):
		QF = QFileDialog()
		self.filepath = QF.getOpenFileName(self, 'Open file', '', 'CSV Files (*.csv)')[0]
		self.lineEdit.setText(self.filepath)