# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 19:49:54 2015

@author: thoma_000
"""
from ui import *
import sys

if __name__ == "__main__":
	app = gui.QApplication(sys.argv)
	myapp = MainForm()
	myapp.show()
	sys.exit(app.exec_())