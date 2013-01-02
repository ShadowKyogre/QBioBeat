from PyQt4 import QtCore,QtGui

class QColorButton(QtGui.QPushButton):

	colorChanged = QtCore.pyqtSignal('QColor')

	def __init__(self, color=None, parent=None):
		super().__init__(parent)
		self.clicked.connect(lambda x: self.adjustColor())

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
			self.setText(color.name())
			px=QtGui.QPixmap(128,128)
			px.fill(self._color)
			self.setIcon(QtGui.QIcon(px))
			self.colorChanged.emit(self.color)
		else:
			raise ValueError("That isn't a QColor!")
	
	color = QtCore.pyqtProperty('QColor',fget=color,fset=setColor)
