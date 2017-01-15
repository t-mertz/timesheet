# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Thomas Mertz

Graphical user interface for the timesheet program.

DEPENDENCIES:
* standard library
* PyQt4
* timesheet
* lacommon
"""

import PyQt4.QtGui as gui
from PyQt4.QtCore import pyqtSlot
import sys
import lacommon
import timesheet
import os
if os.environ["COMPUTERNAME"] == "SURFACE":
	SCALE_FACTOR = 2 # high resolution scaling fix
else:
	SCALE_FACTOR = 1


class MainForm(gui.QWidget):
	TEXT_POS = (10*SCALE_FACTOR, 10*SCALE_FACTOR)
	BTN_NEXT_POS = (390*SCALE_FACTOR, 280*SCALE_FACTOR)
	BTN_BACK_POS = (300*SCALE_FACTOR, 280*SCALE_FACTOR)
	state = { 'start' : 0,
			  'enter_name' : 1,
			  'enter_date1' : 2,
			  'enter_date2' : 3,
			  'summary' : 4,
			  'done' : 5 }
	
	def __init__(self):
		gui.QWidget.__init__(self)
		self.setWindowTitle("TimeSheet")
		self.resize(480*SCALE_FACTOR, 320*SCALE_FACTOR)
		
		self.head_msg = gui.QLabel("", self)
		self.head_msg.resize(200*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.head_msg.move(*MainForm.TEXT_POS)
		self.head_msg.hide()
		
		self.btn_next = gui.QPushButton("Next", self)
		self.btn_next.move(*MainForm.BTN_NEXT_POS)
		self.btn_next.clicked.connect(self.btn_next_handle)
		
		self.btn_back = gui.QPushButton("Back", self)
		self.btn_back.move(*MainForm.BTN_BACK_POS)
		self.btn_back.clicked.connect(self.btn_back_handle)
		self.btn_back.hide()
		
		self.build_frame_start()



	@pyqtSlot()
	def btn_next_handle(self):
		if self.state == MainForm.state['start']:
			self.del_frame_start()
			self.build_frame_enter_name()
		elif self.state == MainForm.state['enter_name']:
			pass
			self._name = self.name_box.text()
			self._institute = self.inst_box.text()
			self._targethours = self.thours_box.text()
			
			input = [self._name, self._institute, self._targethours]
			
			if all(verify_input(input, ['str', 'str', 'float'])):
				self.del_frame_enter_name()
				self.build_frame_enter_date1()
			else:
				self.warning = gui.QMessageBox.warning(self, "Warning", "Review your input.")
				
		elif self.state == MainForm.state['enter_date1']:
			pass
			self._begin_date_str = self.cal.selectedDate().toString()
			self._begin_date = "{}/{}/{}".format(self.cal.selectedDate().year(),
									self.cal.selectedDate().month(),
									self.cal.selectedDate().day())
						
			self.del_frame_enter_date1()
			self.build_frame_enter_date2()
		elif self.state == MainForm.state['enter_date2']:
			pass
			self._end_date_str = self.cal.selectedDate().toString()
			self._end_date = "{}/{}/{}".format(self.cal.selectedDate().year(),
									self.cal.selectedDate().month(),
									self.cal.selectedDate().day())
			
			if self._end_date == self._begin_date or self._end_date < self._begin_date:
				self.warning = gui.QMessageBox.warning(self, "Warning", "You did not select a valid range.")
				pass
			else:
				self.del_frame_enter_date2()
				self.build_frame_summary()
		elif self.state == MainForm.state['summary']:
			self._format = timesheet.FORMAT['txt'] if self.txt_rbtn.isChecked() else timesheet.FORMAT['pdf']
			self._lang = 'en' if self.en_rbtn.isChecked() else 'de'
			
			try:
				self._log_str = timesheet.timesheet(self._begin_date, self._end_date, \
								self._name, self._institute, self._lang, self._format, False, \
								int(self._targethours))
			except:
				self._log_str = "Unexpected error: " + str(sys.exc_info()[0])
				raise
			self.del_frame_summary()
			self.build_frame_done()
		elif self.state == MainForm.state['done']:
			sys.exit()
		else:
			pass
								
		pass
	
	@pyqtSlot()
	def btn_back_handle(self):
		if self.state == MainForm.state['start']:
			pass
		elif self.state == MainForm.state['enter_name']:
			self.del_frame_enter_name()
			self.build_frame_start()
			self.btn_back.hide()
			self.head_msg.hide()
		elif self.state == MainForm.state['enter_date1']:
			self.del_frame_enter_date1()
			self.build_frame_enter_name()
		elif self.state == MainForm.state['enter_date2']:
			self.del_frame_enter_date2()
			self.build_frame_enter_date1()
		elif self.state == MainForm.state['summary']:
			self.del_frame_summary()
			self.build_frame_enter_date2()
		elif self.state == MainForm.state['done']:
			self.del_frame_done()
			self.build_frame_enter_name()
		else:
			pass
			

	def build_frame_start(self):
		welcome_str = "Welcome to TimeSheet.\n\nThis application " + \
		"allows you to create your very own customized table of work hours"+\
		" as simply\nas possible. Just click on 'next' to enter your "+\
		"information and get started.\n\n"+\
		"Have fun spending your time on something useful!"
		self.welcome_msg = gui.QLabel(welcome_str, self)
		self.welcome_msg.resize(480*SCALE_FACTOR, 100*SCALE_FACTOR)
		self.welcome_msg.move(10*SCALE_FACTOR, 10*SCALE_FACTOR)
		self.welcome_msg.show()
		
		self.state = MainForm.state['start']

	def del_frame_start(self):
		self.welcome_msg.hide()
		del self.welcome_msg

	def build_frame_enter_name(self):
		self.head_msg.setText("Configure your document")
		self.head_msg.show()
		
		std_msg_size = (200*SCALE_FACTOR, 24*SCALE_FACTOR)
		std_box_size = (180*SCALE_FACTOR, 24*SCALE_FACTOR)
		
		self.name_msg = gui.QLabel("Please enter your name:", self)
		self.name_msg.resize(*std_msg_size)
		self.name_msg.move(10*SCALE_FACTOR, 50*SCALE_FACTOR)
		self.name_msg.show()
		
		self.inst_msg = gui.QLabel("Please enter your Institute:", self)
		self.inst_msg.resize(*std_msg_size)
		self.inst_msg.move(10*SCALE_FACTOR, 80*SCALE_FACTOR)
		self.inst_msg.show()
		
		self.thours_msg = gui.QLabel("Number of hours/month targeted:", self)
		self.thours_msg.resize(*std_msg_size)
		self.thours_msg.move(10*SCALE_FACTOR, 110*SCALE_FACTOR)
		self.thours_msg.show()
		
		name = '' if not hasattr(self, '_name') else self._name
		self.name_box = gui.QLineEdit(name, self)
		self.name_box.resize(*std_box_size)
		self.name_box.move(180*SCALE_FACTOR, 50*SCALE_FACTOR)
		self.name_box.show()
		
		institute = '' if not hasattr(self, '_institute') else self._institute
		self.inst_box = gui.QLineEdit(institute, self)
		self.inst_box.resize(*std_box_size)
		self.inst_box.move(180*SCALE_FACTOR, 80*SCALE_FACTOR)
		self.inst_box.show()
		
		targethours = '' if not hasattr(self, '_targethours') else self._targethours
		self.thours_box = gui.QLineEdit(targethours, self)
		self.thours_box.resize(*std_box_size)
		self.thours_box.move(180*SCALE_FACTOR, 110*SCALE_FACTOR)
		self.thours_box.show()
		
		
		
		self.btn_back.show()
		
		self.state = MainForm.state['enter_name']
		
	def del_frame_enter_name(self):
		self.name_msg.hide()
		self.name_box.hide()
		self.inst_msg.hide()
		self.inst_box.hide()
		self.thours_msg.hide()
		self.thours_box.hide()
		
		del self.name_msg
		del self.name_box
		del self.inst_msg
		del self.inst_box
		del self.thours_msg
		del self.thours_box
	pass
	
	def build_frame_enter_date1(self):
		pass
		self.head_msg.setText("Please enter the fist date")
		
		self.cal = gui.QCalendarWidget(self)
		self.cal.setGridVisible(True)
		self.cal.move(80*SCALE_FACTOR, 60*SCALE_FACTOR)
		self.cal.resize(320*SCALE_FACTOR, 200*SCALE_FACTOR)
		self.cal.show()
		
		self.state = MainForm.state['enter_date1']
	
	def del_frame_enter_date1(self):
		pass
		
		self.cal.hide()
		
	def build_frame_enter_date2(self):
		pass
		self.head_msg.setText("Please enter the final date")
		
		self.cal.show()
		
		self.state = MainForm.state['enter_date2']
	
	def del_frame_enter_date2(self):
		pass
		self.cal.hide()
		
	def build_frame_summary(self):
		pass
		self.head_msg.setText("Here is what you have entered")
		
		self.name_msg = gui.QLabel("Name:", self)
		self.name_msg.resize(100*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.name_msg.move(10*SCALE_FACTOR, 50*SCALE_FACTOR)
		self.name_msg.show()
		self.iname_msg = gui.QLabel(self._name, self)
		self.iname_msg.resize(500*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.iname_msg.move(140*SCALE_FACTOR, 50*SCALE_FACTOR)
		self.iname_msg.show()
		
		self.inst_msg = gui.QLabel("Institute:", self)
		self.inst_msg.resize(300*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.inst_msg.move(10*SCALE_FACTOR, 70*SCALE_FACTOR)
		self.inst_msg.show()
		self.iinst_msg = gui.QLabel(self._institute, self)
		self.iinst_msg.resize(500*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.iinst_msg.move(140*SCALE_FACTOR, 70*SCALE_FACTOR)
		self.iinst_msg.show()
		
		self.thours_msg = gui.QLabel("Hours/month targeted:", self)
		self.thours_msg.resize(300*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.thours_msg.move(10*SCALE_FACTOR, 90*SCALE_FACTOR)
		self.thours_msg.show()
		self.ithours_msg = gui.QLabel(self._targethours, self)
		self.ithours_msg.resize(100*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.ithours_msg.move(140*SCALE_FACTOR, 90*SCALE_FACTOR)
		self.ithours_msg.show()
		
		self.date1_msg = gui.QLabel("Begin date:", self)
		self.date1_msg.resize(300*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.date1_msg.move(10*SCALE_FACTOR, 110*SCALE_FACTOR)
		self.date1_msg.show()
		self.idate1_msg = gui.QLabel(self._begin_date_str, self)
		self.idate1_msg.resize(100*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.idate1_msg.move(140*SCALE_FACTOR, 110*SCALE_FACTOR)
		self.idate1_msg.show()
		
		self.date2_msg = gui.QLabel("End date:", self)
		self.date2_msg.resize(300*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.date2_msg.move(10*SCALE_FACTOR, 130*SCALE_FACTOR)
		self.date2_msg.show()
		self.idate2_msg = gui.QLabel(self._end_date_str, self)
		self.idate2_msg.resize(100*SCALE_FACTOR, 24*SCALE_FACTOR)
		self.idate2_msg.move(140*SCALE_FACTOR, 130*SCALE_FACTOR)
		self.idate2_msg.show()
				
		# Radio Button Group Format
		self.format_rbtn = gui.QGroupBox("Output format", self)
		self.format_rbtn.resize(200*SCALE_FACTOR, 100*SCALE_FACTOR)
		self.format_rbtn.move(10*SCALE_FACTOR, 160*SCALE_FACTOR)
		
		self.txt_rbtn = gui.QRadioButton("txt", self)
		self.txt_rbtn.setChecked(True)
		self.pdf_rbtn = gui.QRadioButton("pdf", self)
		
		layout = gui.QVBoxLayout()
		layout.addWidget(self.txt_rbtn)
		layout.addWidget(self.pdf_rbtn)
		
		self.format_rbtn.setLayout(layout)
		self.format_rbtn.show()
		
		# Radio Button Group Language
		self.lang_rbtn = gui.QGroupBox("Output language", self)
		self.lang_rbtn.resize(200*SCALE_FACTOR, 100*SCALE_FACTOR)
		self.lang_rbtn.move(220*SCALE_FACTOR, 160*SCALE_FACTOR)
		
		self.en_rbtn = gui.QRadioButton("English", self)
		self.en_rbtn.setChecked(True)
		self.de_rbtn = gui.QRadioButton("German", self)
		
		layout = gui.QVBoxLayout()
		layout.addWidget(self.en_rbtn)
		layout.addWidget(self.de_rbtn)
		
		self.lang_rbtn.setLayout(layout)
		self.lang_rbtn.show()
		
		self.state = MainForm.state['summary']
	
		
	def del_frame_summary(self):
		pass
		self.name_msg.hide()
		self.inst_msg.hide()
		self.thours_msg.hide()
		self.date1_msg.hide()
		self.date2_msg.hide()
		self.iname_msg.hide()
		self.iinst_msg.hide()
		self.ithours_msg.hide()
		self.idate1_msg.hide()
		self.idate2_msg.hide()
				
		self.format_rbtn.hide()
		self.lang_rbtn.hide()
		
		del self.name_msg
		del self.inst_msg
		del self.thours_msg
		del self.date1_msg
		del self.date2_msg
		del self.iname_msg
		del self.iinst_msg
		del self.ithours_msg
		del self.idate1_msg
		del self.idate2_msg
		del self.format_rbtn
		del self.lang_rbtn
		
		
	def build_frame_done(self):
		pass
		self.head_msg.setText("Your document is being generated")
		
		self.log_box = gui.QTextEdit("", self)
		self.log_box.setPlainText(self._log_str)
		self.log_box.resize(400*SCALE_FACTOR, 200*SCALE_FACTOR)
		self.log_box.move(20*SCALE_FACTOR, 40*SCALE_FACTOR)
		self.log_box.setReadOnly(True)
		self.log_box.show()
		
		
		self.btn_next.setText("Exit")
		self.btn_back.setText("Start over")
				
		self.state = MainForm.state['done']
	
	def del_frame_done(self):
		pass
		self.log_box.hide()
		
		del self.log_box
		
		self.btn_next.setText("Next")
		self.btn_back.setText("Back")

def verify_input(str, type):
	res = []
	for s,t in zip(str, type):
		if t == 'str':
			res += [s != ""]
		if t == 'float':
			res += [lacommon.isfloat(s)]
	return res
	
if __name__ == "__main__":
	app = gui.QApplication(sys.argv)
	myapp = MainForm()
	myapp.show()
	sys.exit(app.exec_())