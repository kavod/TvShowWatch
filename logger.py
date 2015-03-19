#!/usr/bin/env python
#encoding:utf-8

import os
import json
import copy
from myDate import *
from datetime import datetime, date, time
import myConstants

node = {}

class Logger:
	'''
		The ``Logger`` constructor
		=============================
		
		Initialize a Logger instance with filename TSW.log.json file.
		If file exists, file content is loaded.
		Else, empty file is created

		:param log_file: filepath of log file

	'''
	def __init__(self,log_file = myConstants.LOG_FILE):
		self.filename = log_file
		if os.path.isfile(self.filename):
			self.load()
		else:
			self.content = []
			self.save()

	def load(self):
		if os.path.isfile(self.filename):
			fd = open(self.filename)
			try:
				data = json.load(fd)
			except ValueError:
				data = []
			fd.close
			self.content = [ convert_str2dt(log) for log in data]

	def save(self):	
		result = copy.deepcopy(self.content)
		json.dump(
					[ convert_dt2str(log) for log in result ],
					open(self.filename,"w")
				)

	def append(self,serieID,returnCode,args):
		node = {
				'serieID':	serieID,
				'datetime':	datetime.now(),
				'rtn':		returnCode
				}
		for key,value in args.items():
			node[str(key)] = value
		self.content.append(node)
		self.save()

	def filter_log(self,serieID=0,datefrom=None,dateto=None):
		result = self.content
		serieID = int(serieID)
		if serieID > 0:
			f = make_filter_serieID(serieID)
			result = filter(f,result)
		if datefrom is None:
			datefrom = datetime(1900,01,01)
		f = make_filter_period(datefrom,dateto)
		result = filter(f,result)
		return result

	def print_log(self,serieID=0,datefrom=None,dateto=None):
		print(self.filter_log(serieID,datefrom,dateto))

def make_filter_serieID(serieID):
	return lambda x: x['serieID'] == serieID

def make_filter_period(fromdate,todate=None):
	if todate is None:
		todate = datetime.now()
	return lambda x: x['datetime'] <= todate and x['datetime'] >= fromdate

def convert_dt2str(log):
	log['datetime'] = log['datetime'].strftime("%Y-%m-%dT%H:%M:%S")
	return log

def convert_str2dt(log):
	log['datetime'] = isoparse(log['datetime'])
	return log

def main():
	l = Logger()
	l.append(5436,'210',{})
	l.print_log(5436,datetime(2014,5,30,12),datetime(2014,5,30,12,5))

if __name__ == '__main__':
    main()
