#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import json
import time
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

	def getEpisode(self,serie_id,season,episode,lang='en'):
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "getEpisode" , "--arg" , "{\"id\":" + str(serie_id) + ",\"season\":" + str(season) + ",\"episode\":" + str(episode) + "}"]
		return self.__exec_cmd(cmd,"getEpisode")

	def setSerie(self,id,param):
		arg = {
				"id":int(id),
				"param":{},
				"status":15
				}
		for (key,value) in param.items():
			if key == "emails" and len(value) > 0:
				arg['param']['emails'] = value
			elif key == "emails" and len(value) < 1:
				arg['param']['emails'] = []
			elif key == "keywords" and len(value) > 0:
				arg['param']['keywords'] = value
			elif key == "keywords" and len(value) < 1:
				arg['param']['keywords'] = []
			else:
				arg['param'][str(key)] = str(value)
		cmd = PYTHON_EXEC + self.cmd + ["--action" , "update" , "--arg" , json.dumps(arg)]
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
			return self.__exec_cmd(cmd,"testRunning",json_rtn=False).replace('tvShowWatch is ','')
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

action = form.getvalue('action')
debug = form.getvalue('debug')
if action != "streamGetSeries":
	print("Content-type:text/html\r\n"),
	print('Cache-Control: no-cache\r\n\r\n'),

if action is not None:
	if debug is not None:
		debug = True
	else:
		debug = False
		
	if action == "run":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]},ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		TSW.run()
		sys.exit()
		
	elif action == 'save_conf':
		result = {
			"tracker": tracker_api_conf(form),
			"transmission":transmission_api_conf(form),
			"smtp": email_api_conf(form)
			}
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		if os.path.isfile(CONF_FILE):
			conf = TSW.setConf(json.dumps(result, ensure_ascii=False))
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
		
		print json.dumps({"rtn":conf['rtn'],"error":msg}, ensure_ascii=False)
		sys.exit()
		
	elif action == 'get_conf':
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({'rtn':e.args[0],'error':e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print json.dumps(TSW.getConf())
		sys.exit()
		
	elif action == 'save_keywords':
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		keywords = form.getlist('keywords[]')
		if form.getvalue('serie_id') is not None and int(form.getvalue('serie_id'))>0:
			res = TSW.setSerie(int(form.getvalue('serie_id')),{"keywords":keywords})
			if res['rtn']!='200':
				print json.dumps({"rtn":res['rtn'],"error":res['error']}, ensure_ascii=False)
				sys.exit()
			print json.dumps({"rtn":200,"error":"Keywords updated"}, ensure_ascii=False)
		else:
			res = TSW.setConf(json.dumps({"keywords":keywords}, ensure_ascii=False))
			if res['rtn']!='200':
				print json.dumps({"rtn":res['rtn'],"error":res['error']}, ensure_ascii=False)
				sys.exit()
			print json.dumps({"rtn":200,"error":"Keywords updated"}, ensure_ascii=False)
		sys.exit()
		
	elif action == "getSeries":
		load_tvdb = (form.getvalue('load_tvdb')=='1')
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print json.dumps(TSW.getSeries(load_tvdb))
		sys.exit()

	elif action == "streamGetSeries":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print('Content-Type: text/event-stream\r\n'),
		print('Cache-Control: no-cache\r\n\r\n'),
		while True:
			print "Event: server-time"
			print("data:" + time.ctime(os.path.getmtime(SERIES_FILE)) + "\n\n"),
			sys.stdout.flush()
			time.sleep(5)
		
	elif action == "getSerie":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print json.dumps(TSW.getSerie(int(form.getvalue('id'))))
		sys.exit()
		
	elif action == "delSerie":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print json.dumps(TSW.delSerie(int(form.getvalue('serie_id'))))
		sys.exit()

	elif action == "addSerie":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print json.dumps(TSW.addSerie(int(form.getvalue('serie_id'))))
		sys.exit()
		
	elif action == "getEpisode":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print json.dumps(TSW.getEpisode(int(form.getvalue('serie_id')),int(form.getvalue('season')),int(form.getvalue('episode'))))
		sys.exit()
		
	elif action == "setSerie":
		if form.getvalue('season') is not None and form.getvalue('episode') is not None and form.getvalue('serie_id') is not None:
			serie_id = int(form.getvalue('serie_id'))
			season = int(form.getvalue('season'))
			episode = int(form.getvalue('episode'))
			pattern = form.getvalue('pattern')
			if season * episode != 0:
				try:
					TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
				except Exception as e:
					print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
					sys.exit()
				TSW.setAuth()
				try:
					val_episode = TSW.getEpisode(serie_id, season, episode, 'en')
				except Exception as e:
					print json.dumps({'rtn' : 419, 'error' : 'Episode S' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ' does not exist'})
					sys.exit()
			else:
				print json.dumps({'rtn' : 499, 'error' : 'You must indicate both of Season and Episode numbers'})
				sys.exit()
		else:
			print json.dumps({'rtn' : 499, 'error' : 'You must indicate both of Season and Episode numbers'})
			sys.exit()

		update = TSW.setSerie(serie_id,{'season':season,'episode':episode,'pattern':pattern,'expected':val_episode['result']['firstaired'],'status':15})
		if update['rtn'] != '200':
			print json.dumps({'rtn' : update['rtn'], 'error' : 'Error during TV Show update<br />'+update['error']})
			sys.exit()
		else:
			print json.dumps({'rtn' : 200, 'error' : 'TV Show updated'})
			sys.exit()
	
	elif action == "addemail":
		if form.getvalue('serie_id') == None or int(form.getvalue('serie_id')) == 0:
			print json.dumps({'rtn' : 499, 'error' : 'TV Show unfound'})
			sys.exit()
		if form.getvalue('email') == None or form.getvalue('email') == '':
			print json.dumps({'rtn' : 499, 'error' : 'Email blank'})
			sys.exit()

		id = int(form.getvalue('serie_id'))
		email = str(form.getvalue('email'))

		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		update = TSW.addemail(id,email)
		if update['rtn'] != '200':
			print json.dumps(update)
			sys.exit()
		else:
			print json.dumps({'rtn':200,'error':'Tv Show updated'})
		sys.exit()

	elif action == "delemail":
		if form.getvalue('serie_id') == None or int(form.getvalue('serie_id')) == 0:
			json.dumps({'rtn' : 499, 'error' : 'TV Show unfound'})
			sys.exit()
		if form.getvalue('email') == None or form.getvalue('email') == '':
			json.dumps({'rtn' : 499, 'error' : 'Email blank'})
			sys.exit()

		id = int(form.getvalue('serie_id'))
		email = str(form.getvalue('email'))

		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		update = TSW.delemail(id,email)
		if update['rtn'] != '200':
			print json.dumps(update)
			sys.exit()
		else:
			print json.dumps({'rtn':200,'error':'Tv Show updated'})
		sys.exit()
		
	elif action == "reset_serie_keywords":
		if form.getvalue('serie_id') == None or int(form.getvalue('serie_id')) == 0:
			json.dumps({'rtn' : 499, 'error' : 'TV Show unfound'})
			sys.exit()
		id = int(form.getvalue('serie_id'))
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		update = TSW.resetSerieKeywords(id)
		if update['rtn'] != '200':
			print json.dumps(update)
			sys.exit()
		else:
			print json.dumps({'rtn':200,'error':'Keywords updated'})
		sys.exit()

	elif action == "reset_all_keywords":
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		update = TSW.resetAllKeywords()
		if update['rtn'] != '200':
			print json.dumps(update)
			sys.exit()
		else:
			print json.dumps({'rtn':200,'error':'Keywords updated for all TV Shows'})
		sys.exit()

	elif action == "search":
		if form.getvalue('pattern') is not None:
			pattern = form.getvalue('pattern')
		if form.getvalue('pattern') is None or pattern=='':
			print json.dumps({'rtn':499,'error':'TV Show unfound'})
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		result = TSW.search(pattern)
		print json.dumps(result)
		sys.exit()
		
	elif action == "pushTorrent":
		if form.getvalue('serie_id') != None:
			serie_id = form.getvalue('serie_id')
		else:
			print json.dumps({"rtn":499,"error":'TV Show unfound'}, ensure_ascii=False)
			sys.exit()
		if form['torrent'].filename:
			fn = os.path.basename(form['torrent'].filename)
			destination = '../' + TMP_DIR + '/' + fn
			open(destination, 'wb').write(form['torrent'].file.read())
			try:
				TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
			except Exception as e:
				print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
				sys.exit()
			TSW.setAuth()
			print json.dumps(TSW.push(serie_id,destination), ensure_ascii=False)
		else:
			print json.dumps({"rtn":499,"error":'Enable to upload file'}, ensure_ascii=False)
		sys.exit()
		
	elif action == 'logs':
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print json.dumps(TSW.logs(), ensure_ascii=False)
		sys.exit()
	
	elif action == 'get_arch':
		print ARCH
		sys.exit()

	elif action == 'testRunning':
		try:
			TSW = TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,debug)
		except Exception as e:
			print json.dumps({"rtn":e.args[0],"error":e.args[1]}, ensure_ascii=False)
			sys.exit()
		TSW.setAuth()
		print TSW.testRunning()
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


