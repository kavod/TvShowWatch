#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import shutil
import json
import datetime
import getpass
import fileinput
import pip

# Function to check module installation and install if required
def install_module(module,modules_list,isRoot=False):
	if module not in modules_list:
		cmd = ['install',module]
		if not isRoot:
			cmd.insert(1,'--user') 
		pip.main(cmd)

# Set script folder
tsw_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))	

# Check user type
if getpass.getuser() == 'root':
	isRoot = True
	log_path = os.sep + "var" + os.sep + "log"
	etc_path = os.sep + "etc" + os.sep + "tvShowWatch"
	tmp_path = os.sep + "tmp"
else:
	isRoot = False
	log_path = tsw_path + os.sep + "tmp"
	etc_path = tsw_path + os.sep + "etc"
	tmp_path = tsw_path + os.sep + "tmp"
	
# Set folders and files paths
script_path = tsw_path + os.sep + "syno" + os.sep + "scripts"
app_path = tsw_path + os.sep + "application"
tsw_exe = tsw_path + os.sep + 'tvShowWatch.py'
etc_file = etc_path + os.sep + 'config.xml'
serie_file = etc_path + os.sep + 'series.xml'
log_file = tmp_path + os.sep + 'TSW.log'
directories_file = tsw_path + os.sep + 'directory.json'

python_exec = os.path.basename(sys.executable)
python_path = os.path.dirname(sys.executable)
python_full = sys.executable
	
# Install python-crontab module is missing
installed_packages = sorted([i.key for i in pip.get_installed_distributions()])
install_module('python-crontab',installed_packages)
import crontab

cron_command = '%s %s -s"%s" -c"%s" --action run >> %s' % (python_full , tsw_exe , serie_file , etc_file , log_file)

directories = {
	"arch":"linux",
	"log_path":log_path,
	"etc_path":etc_path,
	"tmp_path":tmp_path,
	"tsw_path":tsw_path,
	"python_path" : python_path,
	"script_path":script_path,
	"app_path":app_path,
	"python_exec":python_exec
}
#Write directory.json
with open(directories_file, 'w') as outfile:
	json.dump(directories, outfile)

# If needed, create directories
if not os.path.isdir(tmp_path):
	os.mkdir(tmp_path)
if not os.path.isdir(etc_path):
	os.mkdir(etc_path)

# Install required python modules
install_module('requests',installed_packages)
install_module('tvdb-api',installed_packages)
install_module('transmissionrpc',installed_packages)
install_module('cherrypy',installed_packages)
install_module('python-crontab',installed_packages)

# Schedule task starting from next 2 minutes 
#now = datetime.datetime.now()
#minute = (now.minute +2) % 60
#c=crontab.CronTab(user=(not isRoot))
#c.remove_all(comment='TvShowWatch')
#job = c.new(command=cron_command,comment='TvShowWatch')
#job.minute.on(minute)
#c.write() if isRoot else c.write_to_user(user=True)

print "Installation successed."
