# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Thomas Mertz

Defines classes date, language and several functions that constitute the
timesheet library.
Create your own report card of work hours filled with randomly generated data
in a formatted .txt file or as a .pdf (check dependencies).

Execute with:
import timesheet
times, times_months = timesheet.create_timesheet(begin_date="15/01/01",end_date="15/07/31")
timesheet.print_table(times,times_months)

DEPENDENCIES:
* standard library
* lacommon.py
* reportlab
"""
from __future__ import division, print_function
import sys
from lacommon import *
import random

pyVERSION = float(sys.version[:3])

if pyVERSION >= 3:
	xrange = range

pdf_output = True
DEBUG = True


FORMAT = { 'pdf' : 1, 'txt' : 0}


class language(object):
	"""
	Provides basic multi-language support by translating several expressions.
	For larger vocabulary include dictionary as data stored on disk.
	"""
	HOURS = { 'en' : "Hours", 'de' : "Stunden"}
	BEGIN = { 'en' : "Begin", 'de' : "Beginn"}
	END = { 'en' : "End", 'de' : "Ende"}
	TOTAL = { 'en' : "Total", 'de' : "Gesamt"}
	DATE = { 'en' : "Date", 'de' : "Datum"}
	HEADLINE = { 'en' : "Daily Work Hours for ", 'de' : "Stuendliche Arbeitszeit fuer "}
	WEEKDAY = { 'en' : "Weekday", 'de' : "Wochentag"}
	SIGNATURE = { 'en' : "Signature", 'de' : "Unterschrift" }
	DISCLAIMER = { 'en' : "Signature", 'de' : "Unterschrift" }
	INSTITUTE = { 'en' : "Institute", 'de' : "FB/Institut/Abteilung" }
	NAME = {'en' : "Name employee", 'de' : "Name des Mitarbeiters"}
	EMPLOYEE = {'en' : "employee", 'de' : "Mitarbeiter"}
	EMPLOYER = {'en' : "employer", 'de' : "Vorgesetzter"}
		
	def __init__(self, lang):
		self.lang = lang
	
	def hours(self, lang=None):
		if lang is None:
			return self.HOURS[self.lang]
		else:
			return self.HOURS[lang]
		
	def begin(self, lang=None):
		if lang is None:
			return self.BEGIN[self.lang]
		else:
			return self.BEGIN[lang]
	
	def end(self, lang=None):
		if lang is None:
			return self.END[self.lang]
		else:
			return self.END[lang]
	
	def total(self, lang=None):
		if lang is None:
			return self.TOTAL[self.lang]
		else:
			return self.TOTAL[lang]
	
	def date(self, lang=None):
		if lang is None:
			return self.DATE[self.lang]
		else:
			return self.DATE[lang]
	
	def headline(self, lang=None):
		if lang is None:
			return self.HEADLINE[self.lang]
		else:
			return self.HEADLINE[lang]
			
	def weekday(self, lang=None):
		if lang is None:
			return self.WEEKDAY[self.lang]
		else:
			return self.WEEKDAY[lang]
			
	def signature(self, lang=None):
		if lang is None:
			return self.SIGNATURE[self.lang]
		else:
			return self.SIGNATURE[lang]
	
	def disclaimer(self, lang=None):
		if lang is None:
			return self.DISCLAIMER[self.lang]
		else:
			return self.DISCLAIMER[lang]
			
	def institute(self, lang=None):
		if lang is None:
			return self.INSTITUTE[self.lang]
		else:
			return self.INSTITUTE[lang]
	
	def name(self, lang=None):
		if lang is None:
			return self.NAME[self.lang]
		else:
			return self.NAME[lang]

	def employee(self, lang=None):
		if lang is None:
			return self.EMPLOYEE[self.lang]
		else:
			return self.EMPLOYEE[lang]

	def employer(self, lang=None):
		if lang is None:
			return self.EMPLOYER[self.lang]
		else:
			return self.EMPLOYER[lang]
class date(object):
	def __init__(self, year=None, month=None, day=None, **kwargs):
		if "date" not in kwargs:
			if year is not None and len(str(year)) == 2:
				self.year = int("20"+str(year))
			else:
				self.year = year
			self.month = month
			self.day = day
		else:
			#print(kwargs['date'])
			input_date = kwargs['date'].split("/")
			#print(input_date)
			assert len(input_date) == 3
			year = input_date[0]
			if len(year) == 2:
				year = "20"+year
			
			month = input_date[1]
			day = input_date[2]
			
			self.year = int(year)
			self.month = int(month)
			self.day = int(day)
			
		if "lang" in kwargs:
			self.lang = kwargs['lang']
		else:
			self.lang = 'en'
					
		self.weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
		self.weekdays_de = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
		self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", \
					"Aug", "Sep", "Oct", "Nov", "Dec"]
		self.months_long = ["January", "February", "March", "April", "May", \
						"June", "July", "August", "September",\
						"October", "November", "December"]
		self.months_long_de = ["Januar", "Februar", "Maerz", "April", \
						"Mai", "Juni", "Juli", "August", "September",\
						"Oktober", "November", "Dezember"]
		self.days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.week_day_2015 = 4 # first of January 2015 is Thursday
		
	def get_days_per_month(self, month):
		return self.days_per_month[month-1]
	
	def get_date(self):
		if self.lang == 'en':
			return "{0:04d}/{1:02d}/{2:02d}".format(self.year,self.month,self.day)
		elif self.lang == 'de':
			return "{2:02d}.{1:02d}.{0:04d}".format(self.year,self.month,self.day)
	
	def get_month_name(self, month, long=False):
		if self.lang == 'en':
			if long:
				return self.months_long[month-1]
			else:
				return self.months[month-1]
		else:
			if long:
				return self.months_long_de[month-1]
			else:
				return self.months[month-1]
				
	def week_day_fix(self,year):
		if year in [2015, 15]:
			return self.week_day_2015
		else:
			pass # fix to include other years, too
			y_diff = year - 2016
			if y_diff == 0:
				return 5 # Jan 1st 2016 = Friday
			else:
				# year > 2016
				n_cycles = y_diff // 4
				n_rest = y_diff % 4
				d_cycles = n_cycles * (366 + 3*365)
				d_rest = 366 + (n_rest-1) * 365 if y_diff != 0 else 0
				
				d = d_cycles + d_rest
				
				# Jan 1st 2016 = Friday = 5
				return (d + 5) % 7
				
		
	def get_weekday(self, year=None, month=None, day=None):
		if year is None:
			assert self.year is not None
			year = self.year
			month = self.month
			day = self.day
		year_day = sum(self.days_per_month[:month-1]) + day
		#print(year_day)
		weekday = ( (year_day-1) % 7 + self.week_day_fix(year) ) % 7
		return weekday
		
	def get_weekday_name_from_date(self, year=None, month=None, day=None):
		weekday = self.get_weekday(year,month,day)
		if self.lang == 'en':
			return self.weekdays[weekday-1]
		else:
			return self.weekdays_de[weekday-1]
		
	def get_weekday_name(self, weekday=None, year=None, month=None, day=None):
		if weekday is None:
			#assert year != None and month != None and day != None
			weekday = self.get_weekday(year,month,day)
		assert weekday < 8
		if self.lang == 'en':
			return self.weekdays[weekday-1]
		else:
			return self.weekdays_de[weekday-1]
	
	def find_weekdays(self, weekday, year, month):
		first_of_month = self.get_weekday(year, month, 1)
		weekdays = []
		difference = first_of_month - weekday
		if difference <= 0:
			first_hit = -difference + 1
		else:
			first_hit = 7 - difference + 1
		i = first_hit
		while i <= self.get_days_per_month(month):
			weekdays.append(i)
			i += 7
		return weekdays
		
	
def create_timesheet(usr_input=False,**kwargs):
	
	if usr_input:
		try:
			begin_date = raw_input("Beginning date [format: YY/MM/DD | YY/M/D]: ")
			end_date = raw_input("End date [format: YY/MM/DD | YY/M/D]: ")
			
			begin_date = begin_date.split("/")
			assert len(begin_date) == 3
			begin_date = [int(begin_date[i]) for i in xrange(3)]
			end_date = end_date.split("/")
			assert len(end_date) == 3
			end_date = [int(end_date[i]) for i in xrange(3)]
		except:
			print("Input exception occurred. Please respect the correct input format.")
			return None, None
	elif "begin_date" in kwargs and "end_date" in kwargs:
		begin_date = kwargs['begin_date']
		end_date = kwargs['end_date']
		begin_date = begin_date.split("/")
		assert len(begin_date) == 3
		begin_date = [int(begin_date[i]) for i in xrange(3)]
		end_date = end_date.split("/")
		assert len(end_date) == 3
		end_date = [int(end_date[i]) for i in xrange(3)]
		
		if "target_hours" in kwargs:
			target_hours = kwargs['target_hours']
		else:
			target_hours = 31
		
		if "fixed_target" in kwargs:
			fixed_target = kwargs['fixed_target']
		else:
			fixed_target = True
		
		if "lang" in kwargs:
			lang = kwargs['lang']
		else:
			lang = 'en'
	else:
		print("No input found.")
		return None, None
	
	times = []
	times_months = []
	
	preset = 'MZ'
	
	
	if preset == 'ITP':
		#target_hours = 31
		# ITP
		fixed_hours = 8
		fixed_weekdays = [5]
		fixed_start = [12]
		fixed_end = [15]
		fixed_target = True
	elif preset == 'FRAME':
		# FRAME
		fixed_hours = 0
		fixed_weekdays = [1, 3]
		fixed_start = [10, 13]
		fixed_end = [14, 17]
		fixed_target = True
	elif preset == 'MZ':
		fixed_hours = 24
		fixed_weekdays = [3]
		fixed_start = [13]
		fixed_end = [19]
		fixed_target = True
	
	random.seed()
	dates = date(lang=lang)
	
	for cur_year in ixrange(begin_date[0],end_date[0]):
		# determine which months to include in the current year
		if cur_year == begin_date[0]:
			if end_date[0] == begin_date[0]:
				months_cur_year = irange(begin_date[1],end_date[1])
			else:
				months_cur_year = irange(begin_date[1],12)
		elif	cur_year == end_date[0]:
			months_cur_year = irange(1,end_date[1])
		else:
			months_cur_year = irange(1,12)
			
		for cur_month in months_cur_year:
			hours_cur_month = fixed_hours
			chosen_days = []
			num_days = random.randrange(5,14)
			avg_hours = round((target_hours - fixed_hours) / num_days) #+ 0.5)
			if avg_hours > 5:
				num_days = int(target_hours / 5.)
			if DEBUG:
				print('num_days', num_days)
				print('avg_hours',avg_hours)
			
			if cur_year == begin_date[0] and cur_month == begin_date[1]:
				if cur_year == end_date[0] and cur_month == end_date[1]:
					days_cur_month = irange(begin_date[2], end_date[2])
				else:
					days_cur_month = irange(begin_date[2], dates.get_days_per_month(cur_month))
			elif cur_year == end_date[0] and cur_month == end_date[1]:
				days_cur_month = irange(1,end_date[2])
			else:
				days_cur_month = irange(1,dates.get_days_per_month(cur_month))
			
			if fixed_target:
				#fixed_days = dates.find_weekdays(2,cur_year,cur_month) # find Tuesdays
				fixed_duration = [e - s for e,s in zip(fixed_end, fixed_start)]
				fixed_days = []
				hours_cur_month = 0
				
				# set fixed days
				for i,di in enumerate(fixed_weekdays):
					tmp = dates.find_weekdays(di,cur_year,cur_month)
					fixed_days += tmp
					hours_cur_month += len(tmp) * fixed_duration[i]
					for fixed_day in tmp:
						times.append([date(cur_year,cur_month,fixed_day).get_date(),fixed_start[i],fixed_end[i]])
				
				remaining_days = days_cur_month
				# remove fixed days from remaining list
				for fd in fixed_days:
					remaining_days.remove(fd)
				
				remaining_hours = target_hours - hours_cur_month
				if DEBUG: print('remaining_hours', remaining_hours)
				
				# choose num_days days randomly from the remaining list
				for i in range(num_days):
					chosen_days.append(random.choice(remaining_days))
					remaining_days.remove(chosen_days[-1])
					
				if DEBUG: print('remaining_days', remaining_days)
				#for fixed_day in fixed_days:
				#	start_hour = 8
				#	stop_hour = 10
				#	times.append([date(cur_year,cur_month,fixed_day).get_date(),start_hour,stop_hour])
				duration_inds = []
				#lo = int(avg_hours) - 2
				#lo = lo if lo > 0 else 1
				#hi = int(avg_hours) + 2
				#indices = range(lo, hi+1) if remaining_hours > 0 else 0
				
				
				if remaining_hours > 0:
					# list of time indices. the algorithm will choose random numbers from
					# this list. The difference between two adjacent chosen numbers will be
					# the duration.
					# Simpler: Total duration will be partitioned into random intervals
					indices = list(range(remaining_hours))
					if DEBUG: print('indices', indices)
					for i in range(num_days-1):
						pass
						if len(indices) > 0:
							duration_inds.append(random.choice(indices))
							indices.remove(duration_inds[-1])
						else:
							pass
						#if durations[-1]-1 in indices:
						#	indices.remove(durations[-1]-1)
						#if durations[-1]-2 in indices:
						#	indices.remove(durations[-1]-2)
						#if durations[-1]+1 in indices:
						#	indices.remove(durations[-1]+1)
					if DEBUG: print('duration_inds',duration_inds)
					indices = list(range(remaining_hours))
					indices.append(-1)
					duration_indices = sorted(duration_inds)
					#duration_indices.sort()
					if DEBUG: print('duration_indices',duration_indices)
					duration_indices.append(indices[-2])
					duration_indices.append(-1)
					if DEBUG: print('duration_indices',duration_indices)
					durations = []
					
					assert len(indices) > max(duration_indices)
					
					for i in range(num_days):
						try:
							durations.append(indices[duration_indices[i]] - indices[duration_indices[i-1]])
						except:
							print(i)
							raise
					assert sum(durations) == remaining_hours, str(durations)+" "+str(sum(durations))+" "+str(remaining_hours)
					
					if DEBUG: print('durations:',durations)
					
					for i in xrange(num_days):
						min_hour = 10 if chosen_days[i] in fixed_days else 8
						max_hour = 13
						start_hour = random.randint(min_hour,max_hour)
						stop_hour = start_hour + durations[i]
						new_day = None
						
						# split working days longer than 4h with a break in the middle
						if 8 >= durations[i] > 4:
							start_hours, stop_hours = split_duration(start_hour, durations[i])
						
						#split long days into two
						elif durations[i] > 8:
							# pick one of the remaining days
							new_day = random.choice(remaining_days)
							remaining_days.remove(new_day)
							new_start = random.randint(min_hour, max_hour)
							new_duration = durations[i] // 2
							new_stop = new_start + new_duration
							
							stop_hour = start_hour + durations[i] - new_duration
							
							# check if half day's hours are within bounds
							if durations[i] - new_duration > 4:
								start_hours, stop_hours = split_duration(new_start, new_duration)
							else:
								start_hours = [start_hour]
								stop_hours = [stop_hour]
							
							# check if new day's hours are within bounds
							if new_duration > 4:
								new_start_hours, new_stop_hours = split_duration(new_start, new_duration)
							else:
								new_start_hours = [new_start]
								new_stop_hours = [new_stop]
						else:
							start_hours = [start_hour]
							stop_hours = [stop_hour]
						
						hours_cur_month += durations[i]
						if durations[i] != 0:
							for start, stop in zip(start_hours, stop_hours):
								times.append([date(cur_year,cur_month,chosen_days[i]).get_date(),start,stop])
							if new_day is not None:
								for start, stop in zip(new_start_hours, new_stop_hours):
									times.append([date(cur_year,cur_month,new_day).get_date(),start,stop])
				times.sort()	
					
			
			if False:
				for cur_day in days_cur_month:
					include = False
					remaining_hours = target_hours - hours_cur_month
					if dates.get_weekday(cur_year,cur_month,cur_day) == 2:
						include = True
						start_hour = 8
						duration = 2
						stop_hour = start_hour + duration
					elif random.random() < 0.5:
						include = True
						start_hour = random.randint(8,16)
						duration = random.randint(1,4)
						if remaining_hours < duration:
							duration = remaining_hours
						stop_hour = start_hour + duration
					if include:
						if dates.get_weekday(cur_year,cur_month,cur_day) == 2: duration = 0
						hours_cur_month += duration
						
						cur_date = date(cur_year,cur_month,cur_day)
						times.append([cur_date.get_date(),start_hour,stop_hour])
					pass
			if not fixed_target:
				while True:
					hours_cur_month = fixed_hours
					chosen_days = []
					days_added = 0
					fixed_days = dates.find_weekdays(2,cur_year,cur_month) # find Tuesdays
					remaining_days = days_cur_month[:]
					for i in xrange(num_days):
						chosen_days.append(random.choice(remaining_days))
						remaining_days.remove(chosen_days[-1])
					for fixed_day in fixed_days:
						start_hour = 8
						stop_hour = 10
						times.append([date(cur_year,cur_month,fixed_day).get_date(),start_hour,stop_hour])
					for i in xrange(num_days):
						min_hour = 10 if chosen_days[i] in fixed_days else 8
						max_hour = 16
						start_hour = random.randint(min_hour,max_hour)
						if i < num_days-1:
							duration = random.randint(max(1,avg_hours-1),avg_hours+1)
						#elif target_hours > hours_cur_month:
						#	duration = target_hours - hours_cur_month
						
						if hours_cur_month >= target_hours:
							duration = 0
						stop_hour = start_hour + duration
						hours_cur_month += duration
						if duration != 0:
							days_added += 1
							times.append([date(cur_year,cur_month,chosen_days[i]).get_date(),start_hour,stop_hour])
					if hours_cur_month <= target_hours:
						break
					else:
						for i in range(days_added):
							times.pop()
						for fixed_day in fixed_days:
							times.pop()
					
				times.sort()	
			
			if DEBUG:
				print('hours_cur_month',hours_cur_month)
				print('times', times)
			times_months.append(["{0}/{1}".format(cur_year,cur_month), hours_cur_month])
			
	if 'log' in kwargs:
		log = kwargs['log']
	else:
		log = False
	if log:
		log_str = "Data created for {} months...\n".format(len(times_months))
		return times, times_months, log_str
	else:
		return times, times_months

def split_duration(start_hour, duration):
	"""
	Split the interval [start_hour, start_hour+duration] into two
	equal parts separated by a 1h break and return a list of start and stop hours.
	"""
	pass
	start_hours = []
	stop_hours = []
	
	half = duration // 2
	start_hours += [start_hour]
	stop_hours += [start_hour + half]
	
	start_hours += [stop_hours[-1] + 1]
	stop_hours += [start_hours[-1] + duration - half]
	
	return start_hours, stop_hours
	

def find_months(times):
	lang = 'en'
	delim = "/" if lang == 'en' else "."
	new_month = [0]
	i = 0
	while i<len(times)-1:
		cur_month = times[i][0].split(delim)[1]
		i += 1
		if times[i][0].split(delim)[1] != cur_month:
			new_month.append(i)
	new_month.append(len(times))
	
	return new_month
	
def print_table(times, times_months, name="", institute="", prnt_lang='en', log=False):
	dates = date(lang=prnt_lang)
	lang = language(lang=prnt_lang)
	new_month = find_months(times)
	
	for imonth in xrange(len(times_months)):
		month = times_months[imonth][0].split("/")[1]
		year = times_months[imonth][0].split("/")[0]
		
		cur_month_name = dates.get_month_name(int(month), long=True)
		
		if len(year) == 2:
			year = "20" + year
		#filename = year + dates.get_month_name(int(month))
		filename = './out/' + year + "_" + month + ".txt"
		assert_dir('./out')
		with open(filename,'w') as f:
			#print("Timesheet for {0} {1}\n".format(dates.get_month_name(int(month)),year), file=f)
			print(lang.headline() + cur_month_name + " " + year, file=f)
			print("\n{0:15s}{1:40s}".format("Name:", name), file=f)
			print("{0:15s}{1:40s}\n".format(lang.institute()+":", institute), file=f)
			#print("{0:10s} | {1:12s} | {2:10s} | {3:10s} | {4:10s}".format("Weekday","Date","Begin","End","Hours"), file=f)
			print("{0:10s} | {1:12s} | {2:10s} | {3:10s} | {4:10s}".format(lang.weekday(), \
					lang.date(),lang.begin(),lang.end(),lang.hours()), file=f)
			hline = ("-"*11 + "+") + ("-"*14 + "+") + ("-"*12 + "+") * 3
			#print("-"*64, file=f)
			print(hline, file=f)
			for i in xrange(new_month[imonth],new_month[imonth+1]):
				cur_date = times[i][0]
				cur_weekday = date(date=cur_date, lang=prnt_lang).get_weekday_name_from_date()
				cur_start = "{0:02d}:{1:02d}".format(times[i][1],0)
				cur_stop = "{0:02d}:{1:02d}".format(times[i][2],0)
				cur_hours = "{}".format(times[i][2]-times[i][1])
				print("{0:10s} | {1:12s} | {2:10s} | {3:10s} | {4:10s}".format(cur_weekday,cur_date,cur_start,cur_stop,cur_hours), file=f)
			#print("\n"+"-"*64+"\n", file=f)
			print(hline + "\n", file=f)
			#print("Total hours: {}".format(times_months[imonth][1]), file=f)
			print("{0} {1}".format(lang.total() + ":", times_months[imonth][1]), file=f)
	
	if pdf_output:
		create_pdf(times, times_months, name, institute, prnt_lang)
		
	if log:
		log_str = "txt output created in ./out"
		return log_str
	pass


def create_pdf(times, times_months, name="", institute="", prnt_lang='en', log=False):
	"""
	Print table into pdf file.
	
	Right now this implementation is very dirty.
	
	CHANGE TO PageTemplates!!!
	"""
	
	dates = date(lang=prnt_lang)
	lang = language(prnt_lang)
	new_month = find_months(times)
	
	import reportlab
	from reportlab.lib.units import inch
	from reportlab.platypus import Paragraph
	from reportlab.lib.styles import ParagraphStyle
	from reportlab.lib import colors
	
	styles = stylesheet()
	tableHeadStyle = ParagraphStyle('heading')	
	
	for imonth in xrange(len(times_months)):
		month = times_months[imonth][0].split("/")[1]
		year = times_months[imonth][0].split("/")[0]
		
		cur_month_name = dates.get_month_name(int(month), long=True)
		
		if len(year) == 2:
			year = "20" + year
		#filename = year + dates.get_month_name(int(month))
		filename = year + "_" + month
		data = []
		
		
		#print("Timesheet for {0} {1}\n".format(dates.get_month_name(int(month)),year), file=f)
		#print("{0:10s} | {1:12s} | {2:10s} | {3:10s}".format("Weekday","Date","Begin","End"), file=f)
		#print("-"*51, file=f)
		h0 = Paragraph('''<b>{}</b>'''.format(lang.date()), tableHeadStyle)
		h1 = Paragraph('''<b>{}</b>'''.format(lang.weekday()), tableHeadStyle)
		h2 = Paragraph('''<b>{}</b>'''.format(lang.begin()), tableHeadStyle)
		h3 = Paragraph('''<b>{}</b>'''.format(lang.end()), tableHeadStyle)
		h4 = Paragraph('''<b>{}</b>'''.format(lang.hours()), tableHeadStyle)
		#data.append(['''<b>Date</b>''', '''<b>Weekday</b>''', '''<b>Begin</b>''', '''<b>End</b>'''])
		data.append([h0, h1, h2, h3, h4])
		for i in xrange(new_month[imonth],new_month[imonth+1]):
			cur_date = date(date=times[i][0], lang=prnt_lang).get_date()
			cur_weekday = date(date=times[i][0], lang=prnt_lang).get_weekday_name_from_date()
			cur_start = "{0:02d}:{1:02d}".format(times[i][1],0)
			cur_stop = "{0:02d}:{1:02d}".format(times[i][2],0)
			cur_hours = "{}".format(times[i][2]-times[i][1])
			data.append([cur_date, cur_weekday, cur_start, cur_stop, cur_hours])
			#print("{0:10s} | {1:12s} | {2:10s} | {3:10s}".format(cur_weekday,cur_date,cur_start,cur_stop), file=f)
		#print("\n"+"-"*51+"\n", file=f)
		days_cur_month = new_month[imonth+1]-new_month[imonth]
		for i in xrange(20-1-days_cur_month):
			data.append(['', '', '' ,''])
		data.append(['{}: '.format(lang.total()), '', '', '', times_months[imonth][1]])
		#print("Total hours: {}".format(times_months[imonth][1]), file=f)
		
		assert_dir('./out')
		canvas = reportlab.pdfgen.canvas.Canvas('./out/' + filename + '.pdf')
		headline = Paragraph(
			'''<b>{2} {0} {1}</b>'''.format(cur_month_name, year, 
									lang.headline()), styles['title'])
		w, h = headline.wrapOn(canvas, 7*inch, 10)
		headline.drawOn(canvas, 40, 730)
		
		employee_name = name #"Thomas Mertz"
		institute_name = institute #"Institut fuer theoretische Physik (ITP)"
		
		name1 = Paragraph(
			'''{}: '''.format(lang.name()), styles['small'])
		w, h = name1.wrapOn(canvas, 5*inch, 10)
		name2 = Paragraph(
			'''{}'''.format(employee_name), styles['default'])
		w, h = name2.wrapOn(canvas, 5*inch, 10)
		institute1 = Paragraph(
			'''{}: '''.format(lang.institute()), styles['small'])
		w, h = institute1.wrapOn(canvas, 5*inch, 10)
		institute2 = Paragraph(
			'''{}'''.format(institute_name), styles['default'])
		w, h = institute2.wrapOn(canvas, 5*inch, 10)
		name1.drawOn(canvas, 80, 680)
		name2.drawOn(canvas, 180, 682)
		institute1.drawOn(canvas, 80, 660)
		institute2.drawOn(canvas, 180, 662)
				
		
		table = reportlab.platypus.Table(data, \
				colWidths=[2*inch, 1*inch, 1*inch, 1*inch], \
				hAlign = 'CENTER')
		table.setStyle(reportlab.platypus.TableStyle([('INNERGRID', (0,0), \
						(-1,-1), 1.0, colors.black), \
			('BOX', (0, 0), (-1, -1), 1.0, colors.black), \
			('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), \
			('SPAN', (0,-1), (3,-1))]))
		w, h = table.wrapOn(canvas, 0, 0)
		table.drawOn(canvas, 75, 260)
		
		signatureline = Paragraph('''_'''*40, \
					styles['tiny'])
		w, h = signatureline.wrapOn(canvas, 5*inch, 50)
		signature1 = Paragraph('''{} {}'''.format(lang.signature(), lang.employee()), styles['tiny'])
		w, h = signature1.wrapOn(canvas, 5*inch, 50)
		#signature2 = Paragraph('''{} {}'''.format(lang.signature(), lang.employer()), styles['tiny'])
		#w, h = signature2.wrapOn(canvas, 5*inch, 50)
		
		#signatureline.drawOn(canvas, 250, 70)
		signatureline.drawOn(canvas, -30, 70)
		#signature1.drawOn(canvas, 250, 60)
		#signature2.drawOn(canvas, -30, 60)
		signature1.drawOn(canvas, -30, 60)
		
		
		
		canvas.showPage()
		canvas.save()
	
	if log:
		log_str = "pdf output created in ./out"
		return log_str

def timesheet(begin_date, end_date, name, institute, lang, format, fixed_target, target_hours):
	log_str = ""
	times, times_months, log_tmp = create_timesheet(begin_date=begin_date, end_date=end_date, log=True, \
										fixed_target=fixed_target, target_hours=target_hours, lang=lang)
	log_str += log_tmp
	
	if format == FORMAT['txt']:
		global pdf_output
		pdf_output = False
		log_str += print_table(times, times_months, name, institute, lang, log=True)
	elif format == FORMAT['pdf']:
		log_str += create_pdf(times, times_months, name, institute, lang, log=True)
		
	return log_str
		
		
		
		
def stylesheet():
    from reportlab.platypus import (
        BaseDocTemplate, 
        PageTemplate, 
        Frame, 
        Paragraph
    )
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.colors import (
        black,
        purple,
        white,
        yellow
    )
    styles= {
        'default': ParagraphStyle(
            'default',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
        ),
    }
    styles['small'] = ParagraphStyle(
        'default',
        fontName='Helvetica',
        fontSize=8,
        leading=12,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName='Times-Roman',
        bulletFontSize=10,
        bulletIndent=0,
        textColor= black,
        backColor=None,
        wordWrap=None,
        borderWidth= 0,
        borderPadding= 0,
        borderColor= None,
        borderRadius= None,
        allowWidows= 1,
        allowOrphans= 0,
        textTransform=None,  # 'uppercase' | 'lowercase' | None
        endDots=None,         
        splitLongWords=1,
    )
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica',
        fontSize=18,
        leading=42,
        alignment=TA_CENTER,
        textColor=black,
    )
    styles['tiny'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica',
        fontSize=7,
        leading=42,
        alignment=TA_CENTER,
        textColor=black,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        leading=14,
        backColor=yellow,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    return styles

def guimain():
	"""
	Playing around with pyQt...
	For the real deal use the MainForm class defined in ui.py.
	"""
	
	a = gui.QApplication(sys.argv)
	a.aboutToQuit.connect(a.deleteLater)
	
	# window
	w = gui.QWidget()
	w.resize(600, 400)
	w.setWindowTitle("TimeSheet")
	
	# textboxes
	name_box = gui.QLineEdit(w)
	name_box.move(100, 40)
	name_box.resize(100, 24)
	name_box.setText("Enter Name")
	
	# labels
	wlcm = gui.QLabel(w)
	wlcm.move(10, 20)
	wlcm.resize(550, 30)
	wlcm.setText("Welcome to TimeSheet. This application allows you to create\
	your very own table of work hours as simply as possible.\nJust enter your\
	information below and get started. Have fun spending your time on \
	something useful!")
	
	name_label = gui.QLabel(w)
	name_label.move(10, 40)
	name_label.resize(130,24)
	name_label.setText("Enter your name:")
	
	cal_label = gui.QLabel(w)
	cal_label.move(10, 100)
	cal_label.resize(150,24)
	cal_label.setText("Choose date to begin with:")
	
	
	#sl = gui.QAbstractSlider(w)
	#sl.move(20, 20)
	
	# checkboxes
	chbx_tot = gui.QCheckBox(w)
	chbx_tot.move(10, 60)
	chbx_tot.setText("Fix target hours")

	chbx_mean = gui.QCheckBox(w)
	chbx_mean.move(10, 80)
	chbx_mean.setText("Fix mean target hours only")
	
	grp = gui.QButtonGroup(w)
	grp.addButton(chbx_tot)
	grp.addButton(chbx_mean)
	grp.exclusive = True
	
	# calendar
	cal = gui.QCalendarWidget(w)
	cal.setGridVisible(True)
	cal.move(10, 130)
	cal.resize(320, 200)
	
	# buttons
	start_button = gui.QPushButton("Create Timesheet", w)
	start_button.move(450, 350)
	start_button.resize(100, 24)
	
	
	w.show()	
	#times, times_months = create_timesheet(begin_date="15/01/01",end_date="15/01/31")
	#print_table(times,times_months)
	
	sys.exit(a.exec_())

if __name__ == "__main__":
	
	#guimain()
	
	times, times_months = create_timesheet(begin_date="15/01/01",end_date="15/01/31")
	create_pdf(times, times_months, name="usrname", institute="usrinstitute", prnt_lang='de', log=False)
	#print_table(times, times_months, name="usrname", institute="usrinstitute")
	
	