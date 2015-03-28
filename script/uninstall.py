#!/usr/bin/env python
#encoding:utf-8

import sys
import os
import json
import getpass
import crontab

# Set script folder
tsw_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))	
directories_file = tsw_path + os.sep + 'directory.json'

if not os.path.isfile(directories_file):
	sys.exit("TvShowWatch is not installed on this box for your user")

with open(tsw_path + os.sep + 'directory.json') as data_file:    
	directories = json.load(data_file)

# Check user type
if getpass.getuser() == 'root':
	isRoot = True
else:
	isRoot = False

# Unschedule task
c=crontab.CronTab(user=True)
c.remove_all(comment='TvShowWatch')
c.write() if isRoot else c.write_to_user(user=True)

os.remove(directories_file)

print "Uninstallation successed."
