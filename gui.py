from PyQt4 import QtGui,QtCore
import os
import biorhythm
import datetime

colors={"physical":QtGui.QColor("pink"),
			"emotional":QtGui.QColor("green"),
			"intellectual":QtGui.QColor("cyan"),
			"spiritual":QtGui.QColor("white"),
			"awareness":QtGui.QColor("yellow"),
			"aesthetic":QtGui.QColor("magenta"),
			"intuition":QtGui.QColor("orange"),
			"grid":QtGui.QColor("black")}
interval=100
height=200
xstretch=5
max_width=1000

class QBioBeat(QtGui.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("QBioBeat")
		self.scene=QtGui.QGraphicsScene(self)
		self.view=QtGui.QGraphicsView(self.scene,self)
		self.setCentralWidget(self.view)
		self.dialog=None
		self.browseRhythm()

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

	def saveDataAsTXT(self, filename):
		f=open(filename,'w')

		bdate=self.bdt.dateTime().toPyDateTime()
		sdate=self.startdt.dateTime().toPyDateTime()
		edate=self.enddt.dateTime().toPyDateTime()

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
				result=biorhythm.biorhythm_val(bdate,ndt,cv)
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
		#print(bday)
		days=(edate-sdate).days
		for i in range(int(-height),int(height),int(height/10)):
				self.scene.addLine(0,i,max_width,i,pen=QtGui.QPen(colors["grid"]))
		for i in range(1,days+1):
				j=height/days*i
				#print(j)
				self.scene.addLine(j*xstretch,-height,j*xstretch,height,pen=QtGui.QPen(colors["grid"]))
		for button in self.qbg.buttons():
			if not button.isChecked():
					continue
			path=QtGui.QPainterPath()
			cv=button.text().lower()
			for result in biorhythm.biorhythm_intervals(bdate,sdate,edate,cv,interval):
				path.lineTo(result[0]*max_width/days,-result[1]*height)
				#print(result)
			self.scene.addPath(path,QtGui.QPen(colors[cv]))
		nf=QtGui.QFont()
		nf.setPixelSize(height/3)
		txt=self.scene.addText('Birth date: {}'.format(bdate.strftime("%m/%d/%Y - %H:%M:%S")))
		txt.setY(-height-height)
		txt.setFont(nf)
		txt=self.scene.addText('Start time: {}'.format(sdate.strftime("%m/%d/%Y - %H:%M:%S")))
		txt.setFont(nf)
		txt.setY(-height-height/3*2)
		txt=self.scene.addText('End time: {}'.format(edate.strftime("%m/%d/%Y - %H:%M:%S")))
		txt.setFont(nf)
		txt.setY(-height-height/3)

	def browseRhythm(self):
		if self.dialog is not None:
				self.dialog.show()
				return
		self.dialog=QtGui.QDockWidget(self)
		self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose,True)
		self.dialog.setWindowTitle("Browse Rhythm")

		w=QtGui.QWidget(self.dialog)
		layout=QtGui.QGridLayout(w)

		self.startdt=QtGui.QDateTimeEdit(w)
		self.enddt=QtGui.QDateTimeEdit(w)
		self.bdt=QtGui.QDateTimeEdit(w)
		self.bdt.dateTimeChanged.connect(lambda x: self.plot())
		self.startdt.dateTimeChanged.connect(lambda x: self.plot())
		self.enddt.dateTimeChanged.connect(lambda x: self.plot())
		rhytypes=QtGui.QGroupBox(w)
		rhytypes.setTitle("Rhythm Types")
		vbox=QtGui.QVBoxLayout(rhytypes)
		self.qbg=QtGui.QButtonGroup(vbox)
		self.qbg.setExclusive(False)
		self.qbg.buttonClicked.connect(lambda x: self.plot())
		for k in biorhythm.CYCLE_PERIODS.keys():
			b=QtGui.QCheckBox(k.title(),rhytypes)
			self.qbg.addButton(b)
			vbox.addWidget(b)

		layout.addWidget(QtGui.QLabel("Birth Date"),0,0)
		layout.addWidget(QtGui.QLabel("Start Date"),1,0)
		layout.addWidget(QtGui.QLabel("End Date"),2,0)
		layout.addWidget(self.bdt,0,1)
		layout.addWidget(self.startdt,1,1)
		layout.addWidget(self.enddt,2,1)
		layout.addWidget(rhytypes,3,0,1,2)

		self.dialog.setWidget(w)
		self.dialog.show()
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dialog)

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

	app.setApplicationName("QBioBeat")
	app.setApplicationVersion("0.1")
	#app.setWindowIcon(QtGui.QIcon.fromTheme("qtarot"))
	window = QBioBeat()
	window.show()
	os.sys.exit(app.exec_())

if __name__ == "__main__":
	main()
