#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import json
import subprocess
import cgi, cgitb 

from constants import *
from functions import *

form = cgi.FieldStorage() 

class TvShowWatch():
	def __init__(self,py_file = API_FILE, conffile = CONF_FILE, serielist = SERIES_FILE, debug = False, run_file = RUN_FILE):
		self.debug = debug != False
		self.auth = False
		if not os.path.isfile(conffile):
			raise Exception("Configuration file " + conffile + " does not exist",401)
		self.conffile = conffile
		self.serielist = serielist
		if not os.path.isfile(py_file):
			raise Exception("Configuration file " + py_file + " does not exist",401)
		self.py_file = py_file
		if not os.path.isfile(run_file):
			raise Exception("Configuration file " + run_file + " does not exist",401)
		self.run_file = run_file
		self.cmd = [self.py_file ,'-c',self.conffile.replace('"','\"') , '-s',self.serielist.replace('"','\"')]
		self.run_cmd = [self.run_file,'-c',self.conffile.replace('"','\"'),'-s',self.serielist.replace('"','\"')]

	def setAuth(self,auth=True):
		if self.auth != auth:
			self.auth = auth
			if self.auth:
				self.cmd.append('--admin')
			else:
				self.cmd.remove('--admin')

	def isAuth(self):
		return self.auth

	def __exec_cmd(self,cmd,method="unknown",json_rtn=True):
		try:
			result = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as e:
			raise e
		except:
			if self.debug:
				print cmd
			raise Exception(method)
		if self.debug:
			print cmd
			print result
		if json_rtn:
			return json.loads(result)
		else:
			return result
		
	def getConf(self):
		cmd = PYTHON_EXEC + self.cmd + ['--action','getconf']
		return self.__exec_cmd(cmd,"getConf")

	def setConf(self,conf):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "config" , "--arg" , "{\"conf\":" + str(conf) + "}"]
		return self.__exec_cmd(cmd,"setConf")

	def createConf(self,conf):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "init" , "--arg" , "{\"conf\":" + str(conf) + "}"]
		return self.__exec_cmd(cmd,"createConf")

	def getSeries(self,load_tvdb=False):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "list" , "--arg" , "{\"load_tvdb\":" + str(load_tvdb).lower() + "}"]
		return self.__exec_cmd(cmd,"getSeries")

	def getSerie(self,id):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "list" , "--arg" , "{\"ids\":[" + str(id) + "]}"]
		return self.__exec_cmd(cmd,"getSerie")

	def getEpisode(self,serie_id,season,episode):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "getEpisode" , "--arg" , "{\"id\":" + str(serie_id) + ",\"season\":" + str(season) + ",\"episode\":" + str(episode) + "}"]
		return self.__exec_cmd(cmd,"getEpisode")

	def setSerie(self,id,param):
		arg = "{\"id\":" + str(id) + ",\"param\":{"
		for (key,value) in param.items():
			if key == "emails" and len(value) > 0:
				arg += '"emails":[\"' + "\",\"".join(value) + '\"],'
			elif key == "emails" and len(value) < 1:
				arg += '"emails":[],'
			elif key == "keywords" and len(value) > 0:
				arg += '"keywords":[\"' + "\",\"".join(value) + '\"],'
			elif key == "keywords" and len(value) < 1:
				arg += '"keywords":[],'
			else:
				arg += '"' + str(key) + '":"' + str(value) + '",'
		arg += '"status":15'
		arg += "}}"
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "update" , "--arg" , arg]
		return self.__exec_cmd(cmd,"setSerie")
	
	def addemail(self,id,email):
		serie = self.getSerie(id)
		emails = serie['result']['emails']
		if email not in emails:
			emails.append(email)
		return self.setSerie(id,{"emails":emails})

	def delemail(self,id,email):
		serie = self.getSerie(id)
		emails = serie['result']['emails']
		if email in emails:
			emails.remove(email)
		return self.setSerie(id,{"emails":emails})

	def delSerie(self,id):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "del" , "--arg" , "{\"id\":" + str(id) + "}"]
		return self.__exec_cmd(cmd,"delSerie")

	def addSerie(self,id):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "add" , "--arg" , "{\"id\":" + str(id) + "}"]
		return self.__exec_cmd(cmd,"addSerie")

	def resetSerieKeywords(self,id):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "resetKeywords" , "--arg" , "{\"id\":" + str(id) + "}"]
		return self.__exec_cmd(cmd,"resetSerieKeywords")

	def resetAllKeywords(self):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "resetAllKeywords"]
		return self.__exec_cmd(cmd,"resetAllKeywords")


	def search(self,pattern):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "search" , "--arg" , "{\"pattern\":\"" + str(pattern) + "\"}"]
		return self.__exec_cmd(cmd,"search")

	def testRunning(self):
		cmd = ['/var/packages/TvShowWatch/scripts/start-stop-status','status']
		try:
			return self.__exec_cmd(cmd,"testRunning").replace('tvShowWatch is ','')
		except subprocess.CalledProcessError as e:
			return "Not running..."

	def push(self,serie_id,destination):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "push" , "--arg" , "{\"id\":" + str(serie_id) + ",\"filepath\":\"" + destination + "\"}"]
		return self.__exec_cmd(cmd,"push")

	def run(self):
		#myfile = open(LOGFILE, "a"):
		cmd = ["date"]
		print self.__exec_cmd(cmd,"date",json_rtn=False)
		cmd = PYTHON_EXEC + self.run_cmd + ["--action" , "run"]
		print self.__exec_cmd(self.run_cmd,"run",json_rtn=False)
		return True

	def logs(self):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "logs"]
		return self.__exec_cmd(cmd,"logs")


for name, value in {
    "action" : "get_conf",
    "keywords" : "niouf"
}.items():
    form.list.append(cgi.MiniFieldStorage(name, value))
form.list.append(cgi.MiniFieldStorage('keywords', "4015"))
action = form.getvalue('action')
debug = form.getvalue('debug')

if action is not None:
	if form.getvalue('debug') is not None:
		debug = True
	else:
		debug = False
		
	if action == "run":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]})
			sys.exit()
		TSW.setAuth()
		TSW.run()
		sys.exit()
		
	elif action == 'save_conf':
		result = '{"tracker":' + tracker_api_conf(form)
		result += ',"transmission":' + transmission_api_conf(form)
		result += ',"smtp":' + email_api_conf(form)
		result += '}'
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]})
			sys.exit()
		TSW.setAuth()
		if os.path.isfile(CONF_FILE):
			conf = TSW.setConf(result)
			if conf['rtn']=='200' or conf['rtn']=='302':
				msg = "Configuration file saved"
			else:
				msg = "Error during configuration save: " + conf['error']
		else:
			conf = TSW.createConf(result)
			if conf['rtn']=='200':
				msg = 'Configuration file created'
			else:
				msg = 'Error during configuration creation: ' + conf['error']
		
		print json.dumps({"rtn":conf['rtn'],"error":msg})
		sys.exit()
		
	elif action == 'get_conf':
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]})
			sys.exit()
		TSW.setAuth()
		print TSW.getConf()
		sys.exit()
		
	elif action == 'save_keywords':
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]})
			sys.exit()
		TSW.setAuth()
		keywords = form.getlist('keywords')
		if form.getvalue('serie_id') is not None and int(form.getvalue('serie_id'))>0:
			res = TSW.setSerie(int(form.getvalue('serie_id')),json.dumps({"keywords":keywords}))
			if res['rtn']!='200':
				print json.dumps({"rtn":res['rtn'],"error":res['error']})
				sys.exit()
			print json.dumps({"rtn":200,"error":"Keywords updated"})
		else:
			res = TSW.setConf(json.dumps({"keywords":keywords}))
			if res['rtn']!='200':
				print json.dumps({"rtn":res['rtn'],"error":res['error']})
				sys.exit()
			print json.dumps({"rtn":200,"error":"Keywords updated"})
		sys.exit()
		

'''TSW = TvShowWatch()
TSW.setAuth()
TSW.setConf('{"keywords":["niouf"]}')
TSW.getConf()
TSW.getSeries()
TSW.getSerie("264586")
#TSW.getEpisode("264586","1","1")
TSW.setSerie("264586",{"episode":2,"emails":[]})
TSW.getSerie("264586")
TSW.setSerie("264586",{"episode":1})
TSW.addemail("264586","niouf@niouf.fr")
TSW.getSerie("264586")
TSW.addemail("264586","niorf@niouf.fr")
TSW.delemail("264586","niouf@niouf.fr")
TSW.getSerie("264586")
TSW.getSeries()
TSW.delSerie("264586")
TSW.getSeries()
TSW.addSerie("264586")
TSW.setSerie("264586",{"keywords":["niouf","niorf"]})
TSW.getSerie(264586)
TSW.resetSerieKeywords(264586)
TSW.getSerie(264586)
TSW.setSerie("264586",{"keywords":["plouf","niorf"]})
TSW.resetAllKeywords()
TSW.getSerie(264586)
#TSW.search("X files")
#TSW.testRunning()
#TSW.run()
#TSW.logs()'''



