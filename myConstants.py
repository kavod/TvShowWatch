#!/usr/bin/env python
#encoding:utf-8
import os
import sys
import json

class myConstants(object):
	CONFIG_FILE = sys.path[0] + '/config.xml' if sys.path[0] != '' else 'config.xml'
	LIST_FILE = sys.path[0] + '/series.xml' if sys.path[0] != '' else 'series.xml'
	SCRIPT_PATH = sys.path[0] if sys.path[0] != '' else './'
	TMP_PATH = "/tmp"
	LOG_PATH = "/tmp"
	PATH = {'configpath':CONFIG_FILE,'seriepath':LIST_FILE,'tmppath':TMP_PATH, 'logpath':LOG_PATH}

def load_directories():
	# Load directories paths
	try:
		dir_file_folder = sys.path[0] + 'directory.json'
		json_data = open(dir_file_folder)
		myConstants.PATH = dict(json.load(json_data))
		myConstants.CONFIG_FILE = myConstants.PATH['configpath'] + '/config.xml'
		myConstants.LIST_FILE = myConstants.PATH['seriepath'] + '/series.xml'
		myConstants.TMP_PATH = myConstants.PATH['tmppath']
		myConstants.LOG_PATH = myConstants.PATH['logpath']
		myConstants.SCRIPT_PATH = myConstants.PATH['scriptpath']
	except: # If directory file reading failed
		print("Fail to open directory file:" + dir_file_folder)
		sys.exit()
