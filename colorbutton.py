from PyQt4 import QtCore,QtGui

class QColorButton(QtGui.QWidget):

	colorChanged = QtCore.pyqtSignal('QColor')

	def __init__(self, color=None, parent=None):
		super().__init__(parent)

		layout=QtGui.QHBoxLayout(self)
		self.label=QtGui.QLabel(self)
		self.label.setAutoFillBackground(True)
		self.button=QtGui.QPushButton(self)
		self.button.clicked.connect(lambda x: self.adjustColor())
		layout.addWidget(self.label)
		layout.addWidget(self.button)

		if isinstance(color,QtGui.QColor):
			self.color=color
		else:
			self.color=QtGui.QColor()
	
	def adjustColor(self):
		self.color=QtGui.QColorDialog.getColor(initial=self.color,parent=self)

	def color(self):
		return self._color
	
	def setColor(self,color):
		if isinstance(color,QtGui.QColor): 
			self._color=color
			self.button.setText(color.name())
			p=self.label.palette()
			p.setColor(QtGui.QPalette.Background, color)
			self.label.setPalette(p)
			self.colorChanged.emit(self.color)
		else:
			raise ValueError("That isn't a QColor!")
	
	color = QtCore.pyqtProperty('QColor',fget=color,fset=setColor)
