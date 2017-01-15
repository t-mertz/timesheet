# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:50:15 2015

@author: thoma_000
"""
import sys,os

pyVERSION = float(sys.version[:3])

if pyVERSION >= 3:
	xrange = range

def ixrange(start, stop=None, step=1):
	if stop == None:
		start, stop = 0, start
	
	return xrange(start, stop+1, step)
	
def irange(start, stop=None, step=1):
	if stop == None:
		start, stop = 0, start
	
	return list(range(start, stop+1, step))

def mrange(start, stop=None, step=1):
	""" Takes mathematical indices 1,2,3,... and returns a range in the information
	theoretical format 0,1,2,...
	"""
	if stop == None:
		start, stop = 1, start
	
	return list(range(start-1, stop, step))
	
def assert_dir(path):
	"""
	Make sure the path exists. If not, create it.
	"""
	if not os.access(path, os.F_OK):
		os.mkdir(path)
		
def isfloat(x):
	try:
		temp = float(x)
		return True
	except ValueError:
		return False