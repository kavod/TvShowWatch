#!/usr/bin/env python
#encoding:utf-8
import os
import sys
import json

try:
	dir_file_folder = os.path.dirname(os.path.abspath(__file__)) + '/directory.json'
	json_data = open(dir_file_folder)
	PATH = dict(json.load(json_data))
except: # If directory file reading failed
	sys.exit("Fail to open directory file:" + dir_file_folder)
try:
	TMP_PATH = PATH['tmp_path']
	LOG_PATH = PATH['log_path']
	TSW_PATH = PATH['tsw_path']
	ETC_PATH = PATH['etc_path']
	APP_PATH = PATH['app_path']
	PYTHON_PATH = PATH['python_path']
	SCRIPT_PATH = PATH['script_path']
	
	CONFIG_FILE = ETC_PATH + '/config.json'
	SERIES_FILE = ETC_PATH + '/series.json'
	PID_FILE = TMP_PATH + '/TSW.pid'
	START_STOP_FILE = SCRIPT_PATH + '/start-stop-status'
	LOG_FILE = LOG_PATH + '/TSW.log.json'
	
	ARCH = PATH['arch']
except Exception as e:
	print "Cannot read " + e[0]
	sys.exit()
	
def load_path(path, filename):
	if filename != "":
		filename = "/" + filename
	if path not in PATH.keys():
		raise Exception(path)
	return PATH[path] + filename
