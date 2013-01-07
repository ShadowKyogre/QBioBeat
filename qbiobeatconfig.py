from PyQt4 import QtGui,QtCore
from collections import OrderedDict as od
from datetime import datetime

class QBioBeatConfig:

	APPNAME="QBioBeat"
	APPVERSION="0.1.2"
	AUTHOR="ShadowKyogre"
	DESCRIPTION="A small biorhythm application based on PyQt4."
	YEAR="2012"
	PAGE="http://shadowkyogre.github.com/QBioBeat/"

	def __init__(self):
		self.settings=QtCore.QSettings(QtCore.QSettings.IniFormat,
						QtCore.QSettings.UserScope,
						QBioBeatConfig.AUTHOR,
						QBioBeatConfig.APPNAME)
		self.colors=od([("physical",QtGui.QColor("pink")),
			("emotional",QtGui.QColor("green")),
			("intellectual",QtGui.QColor("cyan")),
			("spiritual",QtGui.QColor("white")),
			("awareness",QtGui.QColor("yellow")),
			("aesthetic",QtGui.QColor("magenta")),
			("intuition",QtGui.QColor("orange")),
			("grid",QtGui.QColor("black")),
			("baseline",QtGui.QColor("red")),
			("background",QtGui.QColor("white")),
			("(mini)critical",QtGui.QColor("gray"))])
		self.enabled=od([("physical",False),
			("emotional",False),
			("intellectual",False),
			("spiritual",False),
			("awareness",False),
			("aesthetic",False),
			("intuition",False),])
		self.sys_icotheme=QtGui.QIcon.themeName()
		self.reset_settings()
	
	def reset_settings(self):
		self.current_icon_override=self.settings.value("stIconTheme", "")
		if self.current_icon_override > "":
			QtGui.QIcon.setThemeName(self.current_icon_override)
		else:
			QtGui.QIcon.setThemeName(self.sys_icotheme)

		self.settings.beginGroup("LastReportSettings")
		self.bdt=datetime.strptime(self.settings.value('birthday','01/01/2000 - 00:00:00'),"%m/%d/%Y - %H:%M:%S")
		self.sdt=datetime.strptime(self.settings.value('startTime','01/01/2000 - 00:00:00'),"%m/%d/%Y - %H:%M:%S")
		self.edt=datetime.strptime(self.settings.value('endTime','01/01/2000 - 00:00:00'),"%m/%d/%Y - %H:%M:%S")
		self.samples_taken=self.settings.value('samplesTaken',100,type=int)
		self.settings.beginGroup("patternsEnabled")
		for k in self.enabled.keys():
				self.enabled[k]=self.settings.value(k,self.enabled[k],type=bool)
		self.settings.endGroup()
		self.settings.endGroup()

		self.settings.beginGroup("LastChartAppearance")
		self.bgop=self.settings.value('backgroundOpacity',0,type=int)
		self.mcop=self.settings.value('miniCriticalOpacity',0,type=int)
		self.height=self.settings.value('height',400,type=int)
		self.width=self.settings.value('width',1000,type=int)
		self.font=QtGui.QFont(self.settings.value('font',''))
		self.show_panel=self.settings.value('showPanel',False,type=bool)
		self.settings.beginGroup("colors")
		for k in self.colors.keys():
				if self.settings.contains(k):
					self.colors[k]=QtGui.QColor(self.settings.value(k))
		self.settings.endGroup()
		self.settings.endGroup()

	def save_settings(self):
		self.settings.setValue("stIconTheme",self.current_icon_override)
		self.settings.beginGroup("LastReportSettings")
		print(self.bdt,self.sdt,self.edt)
		self.settings.setValue('birthday',self.bdt.strftime("%m/%d/%Y - %H:%M:%S"))
		self.settings.setValue('startTime',self.sdt.strftime("%m/%d/%Y - %H:%M:%S"))
		self.settings.setValue('endTime',self.edt.strftime("%m/%d/%Y - %H:%M:%S"))
		self.settings.setValue('samplesTaken',self.samples_taken)
		self.settings.beginGroup("patternsEnabled")
		for k in self.enabled.keys():
				self.settings.setValue(k,self.enabled[k])
		self.settings.endGroup()
		self.settings.endGroup()

		self.settings.beginGroup("LastChartAppearance")
		self.settings.setValue('backgroundOpacity',self.bgop)
		self.settings.setValue('miniCriticalOpacity',self.mcop)
		self.settings.setValue('height',self.height)
		self.settings.setValue('width',self.width)
		self.settings.setValue('font',self.font.family())
		self.settings.setValue('showPanel',self.show_panel)
		self.settings.beginGroup("colors")
		for k in self.colors.keys():
				self.settings.setValue(k,self.colors[k].name())
		self.settings.endGroup()
		self.settings.endGroup()
		self.settings.sync()	

