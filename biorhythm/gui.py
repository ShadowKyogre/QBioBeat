from PyQt4 import QtGui,QtCore
from collections import OrderedDict as od
import os
import datetime

from . import APPNAME,APPVERSION
from . import core
from . import colorbutton
from . import fontbutton
from .guiconfig import QBioBeatConfig

class QBioBeat(QtGui.QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__()
		self.setWindowTitle(APPNAME)
		self.scene=QtGui.QGraphicsScene(self)
		self.view=QtGui.QGraphicsView(self.scene,self)
		self.setCentralWidget(self.view)
		self.reportparams=None
		self.chartappearance=None
		self.browseRhythm()
		self.tweakAppearance()
		self.updateBG(qtrcfg.bgop)

		exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('application-exit'), 'Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.close)

		saveAction = QtGui.QAction(QtGui.QIcon.fromTheme('document-save'), 'Save', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip('Save')
		saveAction.triggered.connect(self.saveData)

		#saveIMGAction = QtGui.QAction(QtGui.QIcon.fromTheme('document-save'), 'Save as image', self)
		#saveIMGAction.setShortcut('Ctrl+Shift+S')
		#saveIMGAction.setStatusTip('Save')
		#saveIMGAction.triggered.connect(self.saveDataAsImage)

		toolbar = self.addToolBar('Exit')
		toolbar.addAction(exitAction)
		toolbar.addAction(saveAction)
		#toolbar.addAction(saveIMGAction)

	def closeEvent(self,event):
		print("Saving configuration...")
		qtrcfg.save_settings()
		super().closeEvent(event)

	def saveDataAsTXT(self, filename):
		f=open(filename,'w')

		bdate=self.bdt.dateTime().toPyDateTime()
		sdate=self.startdt.dateTime().toPyDateTime()
		edate=self.enddt.dateTime().toPyDateTime()

		qtrcfg.bdt=bdate
		qtrcfg.sdt=sdate
		qtrcfg.edt=edate

		lines=['Birth date: {}'.format(bdate.strftime("%m/%d/%Y - %H:%M:%S")),
			'Start time: {}'.format(sdate.strftime("%m/%d/%Y - %H:%M:%S")),
			'End time: {}'.format(edate.strftime("%m/%d/%Y - %H:%M:%S")),]
		data_to_get=[button.text().lower() for button in self.qbg.buttons() if button.isChecked()]
		header='date                  {}'.format('|'.join(['{:12s}'.format(s) for s in data_to_get]))
		separator='---------------------{}'.format('|------------'*len(data_to_get))
		lines.append(header)
		lines.append(separator)
		delta=edate-sdate
		
		for d in range(delta.days+1):
			ndt=sdate+datetime.timedelta(d)
			row=[ndt.strftime("%m/%d/%Y - %H:%M:%S")]
			for cv in data_to_get:
				result=core.core_val(bdate,ndt,cv)
				row.append('{:12.2f}'.format(result*100))
			lines.append('|'.join(row))
		f.write('\n'.join(lines))
		f.close()

	def saveDataAsIMG(self,filename,fmt):
		pixMap = QtGui.QPixmap(self.scene.sceneRect().width(),self.scene.sceneRect().height())

		c = QtGui.QColor(0)
		c.setAlpha(0)
		pixMap.fill(c)

		painter=QtGui.QPainter(pixMap)
		self.scene.render(painter)
		painter.end()
		pixMap.save(filename,format=fmt)

	def saveData(self,filename=None):
		if not filename:
			filename=str(QtGui.QFileDialog.getSaveFileName(self, caption="Save Current Reading",
				filter="Images (%s);;Text (*.txt)" %(' '.join(formats))))
		if filename:
			fmt=filename.split(".",1)[-1]
			if fmt == 'txt':
				self.saveDataAsTXT(filename)
			elif "*.{}".format(fmt) in formats:
				self.saveDataAsIMG(filename,fmt)
			else:
				QtGui.QMessageBox.critical(self, "Save Current Reading", \
				"Invalid format ({}) specified for {}!".format(fmt,filename))
	
	def plot(self):
		self.scene.clear()
		self.scene.invalidate()
		bdate=self.bdt.dateTime().toPyDateTime()
		sdate=self.startdt.dateTime().toPyDateTime()
		edate=self.enddt.dateTime().toPyDateTime()
		qtrcfg.bdt=bdate
		qtrcfg.sdt=sdate
		qtrcfg.edt=edate
		days=(edate-sdate).days
		if days <= 0:
			return
		halfheight=qtrcfg.height/2
		daywidth=qtrcfg.width/days
		for i in range(int(-halfheight),int(halfheight),int(halfheight/10)):
				if i == 0:
					key="baseline"
				else:
					key="grid"
				self.scene.addLine(0,i,qtrcfg.width,i,pen=QtGui.QPen(qtrcfg.colors[key]))
		for i in range(days+1):
				j=daywidth*i if i > 0 else 0
				#print(j)
				self.scene.addLine(j,-halfheight,j,halfheight,pen=QtGui.QPen(qtrcfg.colors["grid"]))
		sigdays=set()
		for button in self.qbg.buttons():
			if not button.isChecked():
					continue
			path=QtGui.QPainterPath()
			cv=button.text().lower()
			for result in core.core_intervals(bdate,sdate,edate,cv,qtrcfg.samples_taken):
				if abs(result[1]) <= 1E-3 or abs(result[1]) >= 0.999:
					sigdays.add(int(result[0]))
				path.lineTo(result[0]*daywidth,-result[1]*halfheight)
			#print(qtrcfg.colors[cv].name())
			self.scene.addPath(path,QtGui.QPen(qtrcfg.colors[cv]))
		colorcopy=qtrcfg.colors["(mini)critical"]
		colorcopy.setAlpha(qtrcfg.mcop)
		for day in sigdays:
			if day >= days:
				continue
			recy=self.scene.addRect(day*daywidth, 
							-halfheight,daywidth, 
							qtrcfg.height,
							brush=QtGui.QBrush(colorcopy))
			recy.setZValue(-666)
		if self.show_panel.isChecked():
			qtrcfg.font.setPixelSize(qtrcfg.height/20)
			fm=QtGui.QFontMetrics(qtrcfg.font)
			box_width=fm.maxWidth()*34
			box_height=fm.height()*11

			self.scene.addRect(-box_width-15,-halfheight/2,box_width+10,box_height+10,
								pen=QtGui.QPen(qtrcfg.colors["grid"]))

			txt=self.scene.addText('Birth date: {}'.format(bdate.strftime("%m/%d/%Y - %H:%M:%S")),font=qtrcfg.font)
			txt.setX(-box_width-5)
			txt.setY(-halfheight/2+5)
			txt.setDefaultTextColor(qtrcfg.colors["grid"])

			txt=self.scene.addText('Start time: {}'.format(sdate.strftime("%m/%d/%Y - %H:%M:%S")),font=qtrcfg.font)
			txt.setX(-box_width-5)
			txt.setY(-halfheight/2+5+fm.height())
			txt.setDefaultTextColor(qtrcfg.colors["grid"])

			txt=self.scene.addText('End time: {}'.format(edate.strftime("%m/%d/%Y - %H:%M:%S")),font=qtrcfg.font)
			txt.setX(-box_width-5)
			txt.setY(-halfheight/2+5+2*fm.height())
			txt.setDefaultTextColor(qtrcfg.colors["grid"])

			i=0
			for button in self.qbg.buttons():
				if not button.isChecked():
						continue
				y=-halfheight/2+5+(4+i)*fm.height()
				txt=self.scene.addText(button.text(),font=qtrcfg.font)
				txt.setDefaultTextColor(qtrcfg.colors["grid"])
				rect=self.scene.addRect(-box_width/2-10,y,box_width/2,fm.height(),
						brush=QtGui.QBrush(qtrcfg.colors[button.text().lower()]))
				txt.setX(-box_width-5)
				txt.setY(y)
				i+=1
	
	def updateHeight(self, val):
		qtrcfg.height=val
		self.plot()

	def updateWidth(self, val):
		qtrcfg.width=val
		self.plot()

	def updateSamplesTaken(self, val):
		qtrcfg.samples_taken=val
		self.plot()

	def updateFont(self, font):
		qtrcfg.font=font
		self.plot()

	def updateColors(self, color, coltype):
		qtrcfg.colors[coltype]=color
		self.plot()

	def updateShowPanel(self, checked):
		qtrcfg.show_panel=checked
		self.plot()

	def updateBG(self, val):
		qtrcfg.bgop=val
		colorcopy=QtGui.QColor(qtrcfg.colors["background"])
		colorcopy.setAlpha(val)
		self.scene.setBackgroundBrush(QtGui.QBrush(colorcopy))

	def updateMC(self, val):
		qtrcfg.mcop=val
		self.plot()

	def updateEnabled(self, checked, key):
		qtrcfg.enabled[key]=checked

	def tweakAppearance(self):
		if self.chartappearance is not None:
			self.chartappearance.show()
			return
		self.chartappearance=QtGui.QDockWidget(self)
		self.chartappearance.setWindowTitle("Chart Appearance")

		w=QtGui.QWidget(self.reportparams)
		layout=QtGui.QGridLayout(w)
		i=0
		#The connect wrapper is solely to deal with PyQt's odd behavior of directly
		#connecting in a for loop...
		connectWrapper = lambda b,k: b.colorChanged.connect(lambda x: self.updateColors(x,k))
		for k in qtrcfg.colors.keys():
			layout.addWidget(QtGui.QLabel(k.title()),i,0)
			b=colorbutton.QColorButton(color=qtrcfg.colors[k])
			connectWrapper(b,k)
			layout.addWidget(b,i,1)
			i+=1
		layout.addWidget(QtGui.QLabel("Text"),i,0)
		fb=fontbutton.QFontButton(font=qtrcfg.font)
		fb.fontChanged.connect(self.updateFont)
		layout.addWidget(fb,i,1)

		spinbox=QtGui.QSpinBox(w)
		spinbox.setRange(0,255)
		spinbox.setValue(qtrcfg.bgop)
		spinbox.valueChanged[int].connect(self.updateBG)
		layout.addWidget(QtGui.QLabel("Background Opacity"),i+1,0)
		layout.addWidget(spinbox,i+1,1)

		spinbox=QtGui.QSpinBox(w)
		spinbox.setRange(0,255)
		spinbox.setValue(qtrcfg.mcop)
		spinbox.valueChanged[int].connect(self.updateMC)
		layout.addWidget(QtGui.QLabel("(Mini)Critical Opacity"),i+2,0)
		layout.addWidget(spinbox,i+2,1)

		layout.addWidget(QtGui.QLabel("Grid height"),i+3,0)
		layout.addWidget(QtGui.QLabel("Grid width"),i+4,0)
		spinbox=QtGui.QSpinBox(w)
		spinbox.setRange(0,2000)
		spinbox.setValue(qtrcfg.height)
		spinbox.setSuffix("px")
		spinbox.valueChanged[int].connect(self.updateHeight)
		layout.addWidget(spinbox,i+3,1)

		spinbox=QtGui.QSpinBox(w)
		spinbox.setRange(0,2000)
		spinbox.setValue(qtrcfg.width)
		spinbox.setSuffix("px")
		spinbox.valueChanged[int].connect(self.updateWidth)
		layout.addWidget(spinbox,i+4,1)

		self.show_panel=QtGui.QCheckBox("Show chart making information?",w)
		self.show_panel.setChecked(qtrcfg.show_panel)
		self.show_panel.clicked.connect(self.updateShowPanel)
		layout.addWidget(self.show_panel,i+5,0,1,2)
		
		self.chartappearance.setWidget(w)
		self.chartappearance.show()
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.chartappearance)

	def browseRhythm(self):
		if self.reportparams is not None:
				self.reportparams.show()
				return
		self.reportparams=QtGui.QDockWidget(self)
		self.reportparams.setWindowTitle("Report Parameters")

		w=QtGui.QWidget(self.reportparams)
		layout=QtGui.QGridLayout(w)

		self.startdt=QtGui.QDateTimeEdit(w)
		self.enddt=QtGui.QDateTimeEdit(w)
		self.bdt=QtGui.QDateTimeEdit(w)
		self.startdt.setDateTime(qtrcfg.sdt)
		self.enddt.setDateTime(qtrcfg.edt)
		self.bdt.setDateTime(qtrcfg.bdt)
		self.bdt.dateTimeChanged.connect(self.plot)
		self.startdt.dateTimeChanged.connect(self.plot)
		self.enddt.dateTimeChanged.connect(self.plot)
		rhytypes=QtGui.QGroupBox(w)
		rhytypes.setTitle("Rhythm Types")
		vbox=QtGui.QVBoxLayout(rhytypes)
		self.qbg=QtGui.QButtonGroup(vbox)
		self.qbg.setExclusive(False)
		self.qbg.buttonClicked.connect(self.plot)
		#The connect wrapper is solely to deal with PyQt's odd behavior of directly
		#connecting in a for loop...
		connectWrapper = lambda b,k: b.clicked.connect(lambda x: self.updateEnabled(x,k))
		for k in qtrcfg.enabled.keys():
			b=QtGui.QCheckBox(k.title(),rhytypes)
			b.setChecked(qtrcfg.enabled[k])
			connectWrapper(b,k)
			self.qbg.addButton(b)
			vbox.addWidget(b)

		layout.addWidget(QtGui.QLabel("Birth Date"),0,0)
		layout.addWidget(QtGui.QLabel("Start Date"),1,0)
		layout.addWidget(QtGui.QLabel("End Date"),2,0)
		layout.addWidget(self.bdt,0,1)
		layout.addWidget(self.startdt,1,1)
		layout.addWidget(self.enddt,2,1)
		layout.addWidget(QtGui.QLabel("Samples Taken"),3,0)
		spinbox=QtGui.QSpinBox(w)
		spinbox.setRange(0,1000)
		spinbox.setValue(qtrcfg.samples_taken)
		spinbox.valueChanged[int].connect(self.updateSamplesTaken)
		layout.addWidget(spinbox,3,1)
		layout.addWidget(rhytypes,4,0,1,2)

		self.reportparams.setWidget(w)
		self.reportparams.show()
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.reportparams)

def main():
	global formats
	global app
	global qtrcfg

	formats=set(["*."+''.join(i).lower() for i in \
		QtGui.QImageWriter.supportedImageFormats()])

	formats=sorted(list(formats),key=str.lower)
	try:
		formats.remove('*.bw')
	except ValueError:
		pass
	try:
		formats.remove('*.rgb')
	except ValueError:
		pass
	try:
		formats.remove('*.rgba')
	except ValueError:
		pass
	app = QtGui.QApplication(os.sys.argv)

	app.setWindowIcon(QtGui.QIcon.fromTheme("qbiobeat"))
	app.setApplicationName(APPNAME)
	app.setApplicationVersion(APPVERSION)
	qtrcfg = QBioBeatConfig()

	window = QBioBeat()
	window.show()
	os.sys.exit(app.exec_())

if __name__ == "__main__":
	main()
