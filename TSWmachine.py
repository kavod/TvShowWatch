#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import messages
import logging
import json
import copy
from datetime import date
import transmissionrpc
import tracker
import jsonConfigParser
import requests
from myDate import *
from ConfFileJSON import ConfFile
from serieListJSON import SerieList
from functions import *
from myTvDB import *
from logger import *
import myConstants
import myExceptions


class TSWmachine:
	def __init__(self,admin=False,log=False):
		if log:
			logging.basicConfig(level=logging.DEBUG)
		self.admin = admin
		self.confFilename = None
		self.confData = None
		
		self.seriefile = SerieList()
		self.verbosity = log
		try:
			self.confschema = jsonConfigParser.loadParserFromFile(myConstants.CONFIG_SCHEMA)
		except:
			raise Exception(messages.returnCode['423'].format(myConstants.CONFIG_SCHEMA))
	
	def getVerbosity(self):
		return self.verbosity

	def getAuth(self):
		logging.info('Get Auth :'+ str(self.admin))
		return self.admin

	def openFiles(self,conffile=myConstants.CONFIG_FILE,seriefile=myConstants.SERIES_FILE):
		# conf file opening
		logging.info('OpenFile ' + str(conffile) + ' and '+ str(seriefile))
		try:
			self.confData = jsonConfigParser.jsonConfigValue(self.confschema,value=None,filename=conffile)
		except Exception as e:
			logging.info('Fail to open file:'+ str(conffile))
			logging.debug(str(e))
			return {'rtn':'401','tracker_conf':self.get_tracker_conf(),'error':messages.returnCode['401'].format(conffile)}
		self.confFilename = conffile
		
		# conf file parsing
		try:
			self.confData.load()
		except Exception as e:
			logging.info('Fail to parse file:'+ str(conffile))
			logging.debug(str(e))
			return {'rtn':'423','tracker_conf':self.get_tracker_conf(),'error':messages.returnCode['423'].format(conffile)}
		
		logging.info('Conf file OK, opening Serie List')
		return self.seriefile.openFile(seriefile)

	def openedFiles(self,files=['conf','serie']):
		logging.info('OpenedFile')
		if 'conf' in files and self.confData is None:
			logging.info('Conf file not opened')
			return {'rtn':'403','error':messages.returnCode['403'].format("Configuration file")}
		if 'serie' in files and self.seriefile.openedFile()['rtn']!='200':
			logging.info('Serie file not opened')
			return self.seriefile.openedFile()
		return {'rtn':'200','error':messages.returnCode['200']}

	def createConf(self,filename,conf={}):
		logging.info('CreateConf ' + str(filename) + ' with '+ str(conf))
		if (not self.getAuth()):
			return {'rtn':'406','error':messages.returnCode['406']}
		confData = {"version":myConstants.CONFIG_VERSION}
		confData.update(conf)
		self.confFilename = filename
		try:
			self.confData = jsonConfigParser.jsonConfigValue(self.confschema,value=None,filename=filename)
		except:
			return {'rtn':'424','error':messages.returnCode['424'].format(filename)}
		return {'rtn':'200','error':messages.returnCode['200']}

	def getConf(self,conf='all'):
		if (not self.openedFiles(['conf'])['rtn']=='200'):
			result = self.openedFiles(['conf'])
			result['tracker_conf'] = self.get_tracker_conf()
			return result
		if conf=='all':
			result = self.confData.getValue()
		else:
			result = self.confData.getValue(path=conf.split("_"))
				
		return {'rtn':'200','result':result,'tracker_conf':self.get_tracker_conf()}
		
	def get_tracker_conf(self):
		return tracker.TRACKER_CONF

	def setConf(self,conf={},save=True):
		if (not self.getAuth()):
			return {'rtn':'406','error':messages.returnCode['406']}
		if (not self.openedFiles(['conf'])['rtn']=='200'):
			return {'rtn':'403','error':messages.returnCode['403'].format('Configuration')}

		self.confData.update(conf)
		send = ('smtp' in conf.keys())
		if save:
			self.confData.save()
			result = self.testConf(send)
			if result['rtn'] == '200':
				if 'keywords' in conf.keys() and len([x for x in conf['keywords'] if x == ''])<1:
					return result
				else:
					return {'rtn':'304','error':messages.returnCode['304'].format(key)}
			return result
		else:	
			return {'rtn':'200','error':messages.returnCode['200']}

	def testTracker(self):
		logging.info('testTracker')
		trackerConf = self.confData['tracker']
		try:
			provider = tracker.check_provider(trackerConf['id'])
			if 'username' in provider['param'] and trackerConf['user'] == '':
				return {'rtn':'422','error':messages.returnCode['422'].format(provider['name'])}
			mytracker = tracker.Tracker(trackerConf['id'],{'username':trackerConf['user'],'password':trackerConf['password']})
		except myExceptions.InputError as e:
			return {'rtn':'404','error':messages.returnCode['404'].format('Tracker',e.expr)}
		except Exception,e:
			return {'rtn':'404','error':messages.returnCode['404'].format('Tracker',e)}
		else:
			return {'rtn':'200','error':messages.returnCode['200']}

	def testTransmission(self):
		tc = self.confData['transmission']
		if tc['server'] == '' or tc['port'] == '':
			 return {'rtn':'405','error':messages.returnCode['405'].format('Transmission')}
		try:
			transmissionrpc.Client(tc['server'], tc['port'], tc['user'], tc['password'])
		except TransmissionError,e:
			return {'rtn':'404','error':messages.returnCode['404'].format('Transmission',e)}
		else:
			return {'rtn':'200','error':messages.returnCode['200']}

	def testEmail(self,send=False):
		email = self.confData['smtp']
		if len(email) < 1:
			 return {'rtn':'405','error':messages.returnCode['405'].format('Email')}
		try:
			msg = MIMEText('This is a test email')
			msg['Subject'] = 'This is a test email'
			msg['From'] = 'TvShowWatch script'
			msg['To'] = email['emailSender']
			s = smtplib.SMTP(email['server'],int(email['port']))
			if email['ssltls']:
				s.starttls() 
			if email['user'] != '':
				s.login(email['user'],email['password']) 
			if send:
				s.sendmail(email['emailSender'],email['emailSender'],msg.as_string())
			s.quit()
		except Exception,e:
			return {'rtn':'404','error':messages.returnCode['404'].format('SMTP server',e)}
		else:
			return {'rtn':'200','error':messages.returnCode['200']}

	def testConf(self,send=False):
		logging.info('testConf ')
		opened = self.openedFiles(['conf'])
		if (opened['rtn'] != '200'):
			return opened

		mytracker = self.testTracker()
		if (mytracker['rtn'] != '200'):
			return mytracker

		transmission = self.testTransmission()
		if (transmission['rtn'] != '200'):
			return transmission

		email = self.testEmail(send)
		if (email['rtn'] != '200' and email['rtn'] != '405'):
			return email

		if email['rtn'] == '405':
			return {'rtn':'302','error':messages.returnCode['302']}
		else:
			return {'rtn':'200','error':messages.returnCode['200']}

	def getSerie(self,s_id,json_c=False,load_tvdb=False):
		logging.info('getSerie ')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		liste = self.seriefile.listSeries(json_c,load_tvdb)
		if liste == False:
			return {'rtn': 404,'error':messages.returnCode['404'].format('TvDB','') }
		if len(liste)>0:
			if isinstance(s_id,int) or (isinstance(s_id,basestring) and s_id.isdigit()):
				result = [x for x in liste if x['id'] == int(s_id)]
				if len(result)>0:
					return {'rtn':'200','result':result[0]}
				else:
					return {'rtn':'408','error':messages.returnCode['408'].format(str(s_id))}
			elif isinstance(s_id,basestring):
				result = [x for x in liste if x['name'] == s_id]
				if len(result)>0:
					return {'rtn':'200','result':result[0]}
				else:
					return {'rtn':'408','error':messages.returnCode['408'].format(str(s_id))}
			else:
				return {'rtn':'407','error':messages.returnCode['407'].format(str(s_id))}
		else:
			return {'rtn':'300','error':messages.returnCode['300']}

	def getSeries(self,s_ids='all',json_c=False,load_tvdb=False):
		logging.info('getSeries ')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		if s_ids == 'all':
			serielist = self.seriefile.listSeries(json_c,load_tvdb)
			if serielist == False:
				return {'rtn': 404,'error':messages.returnCode['404'].format('TvDB','') }
			if len(serielist)>0:
				return {'rtn':'200','result':[x for x in serielist]}
			else:
				return {'rtn':'300','error':messages.returnCode['300']}
		elif isinstance(s_ids,int) or (isinstance(s_ids,basestring) and s_ids.isdigit()):
			return self.getSerie(s_ids,json_c,load_tvdb)
		elif isinstance(s_ids,list):
			result = []
			for s_id in s_ids:
				res_serie = self.getSerie(s_id,json_c,load_tvdb)
				if res_serie['rtn']!='200':
					result.append(res_serie['result'])
				else:
					return res_serie
			return {'rtn':'200','result':result}
		else:
			return {'rtn':'407','error':messages.returnCode['407'].format(str(s_ids))}

	def addSerie(self,s_id,emails=[],season=0,episode=0):		
		logger = Logger(log_file = myConstants.LOG_FILE)
		logging.info('addSerie ' + str(s_id) + '/'+str(emails)+'/'+str(season)+'/'+str(episode))
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		if self.getSerie(s_id)['rtn']=='200':
			return {'rtn':'409','error':messages.returnCode['409']}

		serie = last_aired(int(s_id),int(season),int(episode))
		if len(serie.keys())<1:
			return {'rtn':'408','error':messages.returnCode['408'].format(str(s_id))}
		episode = serie['next']
		if episode is None:
			# If TV show is achieved, just add it without episode scheduled
			episode = None
			infolog = {}
		else:
			infolog = {'season':episode['seasonnumber'],'episode':episode['episodenumber']}
			episode = {'season':episode['seasonnumber'],'episode':episode['episodenumber'],'aired':convert_date(episode['firstaired'])}
		if self.seriefile.addSerie(serie['id'],serie['seriesname'],episode,emails,self.confData['keywords']):
			logger.append(serie['id'],'101',infolog)
			return {'rtn':'200','error':messages.returnCode['200']}
		else:
			return {'rtn':'411','error':messages.returnCode['411'].format(s_id)}

	def addSeries(self,s_ids,emails=[]):
		logging.info('addSeries')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		if isinstance(s_ids,int):
			return self.addSerie(s_ids,emails)
		elif isinstance(s_ids,list):
			result = []
			for s_id in s_ids:
				res_serie = self.addSerie(s_id,emails)
				res_serie.update({'id':s_id})
				result.append(res_serie)
				if res_serie['rtn'] != '200':
					return {'rtn':'412','error':messages.returnCode['412'],'result':result}
			return {'rtn':'200','result':result}
		else:
			return {'rtn':'411','error':messages.returnCode['411'].format(s_id)}

	def _setSerie(self,s_id,result,emails,keywords,param={}):
		logger = Logger(log_file = myConstants.LOG_FILE)
		error = False
		if len(result)>0:
			serie = self.seriefile.updateSerie(result['id'],param)
			if (serie['id'] == result['id']):
				if emails is not None:
					if(not self.seriefile.changeEmails(result['id'],emails)):
						error = True
				if keywords is not None:
					if(not self.seriefile.changeKeywords(result['id'],keywords)):
						error = True
				if error:
					return {'rtn':'417','error':messages.returnCode['417'].format(result['name'])} #Error during update
				else:
					logger.append(s_id,'100',{})
					return {'rtn':'200','error':messages.returnCode['200']}
			else:
				return {'rtn':'417','error':messages.returnCode['417'].format(result['name'])} #Error during update
		else:
			return {'rtn':'408','error':messages.returnCode['408'].format(str(s_id))} #Not found

	def setSerie(self,s_id,param={},json_c=False):
		logging.info('getSerie ')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		if not all(y in ['emails','season','episode','expected','status','keywords','pattern'] for y in param.keys()):
			return {'rtn':'400','error':messages.returnCode['400'].format(str(param.keys()))}
		if 'emails' in param.keys():
			emails = param.pop('emails')
		else:
			emails = None
		if 'keywords' in param.keys():
			keywords = param.pop('keywords')
		else:
			keywords = None
		liste = self.seriefile.listSeries(json_c)
		if liste == False:
			return {'rtn': 404,'error':messages.returnCode['404'].format('TvDB','') }
		if len(liste)>0:
			if isinstance(s_id,int) or (isinstance(s_id,basestring) and s_id.isdigit()):
				result = [x for x in liste if x['id'] == int(s_id)]
				return self._setSerie(s_id,result[0],emails,keywords,param)
			elif isinstance(s_id,basestring):
				result = [x for x in liste if x['name'] == s_id]
				return self._setSerie(s_id,result[0],emails,keywords,param)
			else:
				return {'rtn':'407','error':messages.returnCode['407'].format(str(s_id))}
		else:
			return {'rtn':'300','error':messages.returnCode['300']}

	def resetKeywords(self,s_id):
		logger = Logger(log_file = myConstants.LOG_FILE)
		logging.info('resetKeywords ' + str(s_id))
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		keywords = self.confData['keywords']
		logger.append(s_id,'102',{})
		return self.setSerie(s_id,{'keywords':keywords},False)

	def resetAllKeywords(self):
		logging.info('resetAllKeywords ')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		keywords = self.confData['keywords']
		series = self.getSeries('all',False,False)
		if len(series)<1:
			return {'rtn':'300','error':messages.returnCode['300']}
		for serie in series['result']:
			result = self.resetKeywords(serie['id'])
			if result['rtn'] != '200':
				break
		return result

	def delSerie(self,s_id):
		logger = Logger(log_file = myConstants.LOG_FILE)
		logging.info('delSerie ')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		serie = self.getSerie(s_id)
		if serie['rtn'] != '200':
			return serie
		result = self.seriefile.delSerie(s_id)
		if result:
			logger.append(s_id,'103',{})
			return {'rtn':'200','error':messages.returnCode['200']}
		else:
			return {'rtn':'413','error':messages.returnCode['413'].format(s_id)}
	
	def delSeries(self,s_ids=''):
		logging.info('delSeries ')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		if s_ids == '':
			return {'rtn':'416','error':messages.returnCode['416']}
		if s_ids == 'all':
			series = self.getSeries()
			if series['rtn'] != '200':
				return series
			else:
				s_ids = [x['id'] for x in series['result']]
		if isinstance(s_ids,int):
			return self.delSerie(s_ids)
		elif isinstance(s_ids,list):
			result = []
			for s_id in s_ids:
				res_serie = self.delSerie(s_id)
				res_serie.update({'id':s_id})
				result.append(res_serie)
				if res_serie['rtn'] != '200':
					return {'rtn':'414','error':messages.returnCode['412'],'result':result}
			return {'rtn':'200','result':result}
		else:
			return {'rtn':'411','error':messages.returnCode['411'].format(s_id)}

	def pushTorrent(self,serieID,filepath):
		logger = Logger(log_file = myConstants.LOG_FILE)
		logging.info('pushTorrent ')
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			return opened
		if int(serieID) == 0:
			return {'rtn':'416','error':messages.returnCode['416']}
		result = self.getSerie(serieID,json_c=False,load_tvdb=True)
		if (result['rtn'] != '200'):
			return result
		serie = result['result']
		if (not os.path.isfile(filepath)):
			return {'rtn':'422','error':messages.returnCode['422'].format(filepath)}
		if (serie['status'] in [10,15,20,21]): # Status waiting for broadcast / waiting for run / searching torrent / No tracker configured
			season = int(serie['season'])
			episode = int(serie['episode'])
			result = self.getEpisode(serieID,season,episode)
			if (season * episode > 0 and result['rtn']=='200'):
				confTransmission = self.confData['transmission']
				tc = transmissionrpc.Client(
						confTransmission['server'],
						confTransmission['port'],
						confTransmission['user'],
						confTransmission['password']
					)
				new_torrent = add_torrent('file://' +filepath, tc, confTransmission['slotNumber'],confTransmission['folder'] is not None)
				self.seriefile.updateSerie(serie['id'],{'status':30, 'slot_id':new_torrent.id})
				logger.append(serieID,'104',{"season":season,"episode":episode})
				return {'rtn':'230','error':messages.returnCode['230']}
		return {'rtn':'421','error':messages.returnCode['421']}
		
		
	def run(self):
		logging.info('Run !!! ')
		logger = Logger(log_file = myConstants.LOG_FILE)
		opened = self.openedFiles()
		if opened['rtn'] != '200':
			print("{0}|{1}".format(opened['rtn'],opened['error']))
			return
		testconf = self.testConf()
		if testconf['rtn'] != '200' and testconf['rtn'] != '302':
			print("{0}|{1}".format(testconf['rtn'],testconf['error']))
			return
		conf = self.confData['tracker']
		try:
			mytracker = tracker.Tracker(conf['id'],{'username':conf['user'],'password':conf['password']},myConstants.TMP_PATH)
		except InputError as e:
			print(e.msg)
			return
		series = self.seriefile

		str_search = '{0} S{1:02}E{2:02} {3}'
		str_result = "{0}|{1}|{2}"
		
		liste = series.listSeries()
		if liste == False:
			return {'rtn': 404,'error':messages.returnCode['404'].format('TvDB','') }

		if (len(liste)<1):
			print("{0}|{1}".format('300',messages.returnCode['300']))
			return

		for serie in liste:
			if serie['status'] == 90 or serie['episode'] == 0: # If last episode reached
				print(str_result.format('303',str(serie['id']),messages.returnCode['303']))
				continue

			
			str_search_list = []
			for keyword in serie['keywords']:
				str_search_list.append(str_search.format(
						serie['pattern'],
						int(serie['season']),
						int(serie['episode']),
						keyword
							))
			if (len(str_search_list)<1):
				str_search_list.append(str_search.format(
                                                serie['name'],
                                                int(serie['season']),
                                                int(serie['episode']),
                                                ''
                                                        ))
			confTransmission = self.confData['transmission']
			if int(serie['status']) == 30: # Torrent already active
				if 'tc' not in locals():
					tc = transmissionrpc.Client(
						confTransmission['server'],
						confTransmission['port'],
						confTransmission['user'],
						confTransmission['password']
					)
				else:
					logging.info('connection saved')

				tor_found = False
				for tor in tc.get_torrents(): # Check if torrent still there!
					if tor.id == serie['slot_id']:
						tor_found = True
						break
				if not tor_found:
					logger.append(serie['id'],'105',{"season":serie['season'],"episode":serie['episode']})
					serie = self.seriefile.updateSerie(serie['id'],{'status':15,'slot_id':0})
				else:
					torrent = tc.get_torrent(serie['slot_id'])
					if torrent.status == 'seeding':
						if(confTransmission['folder'] is not None):
							if (transferFile(torrent.files(),serie,confTransmission)):
								content = str_search_list[0] + ' broadcasted on ' + print_date(convert_date(serie['expected'])) + ' download completed'
								sendEmail(content,serie,self.confData['smtp'])
							else:
								print(str_result.format('418',str(serie['id']),messages.returnCode['418']))
								continue
						next = next_aired(serie['id'],serie['season'],serie['episode'])
						self.seriefile.updateSerie(serie['id'],next)
						if next['status'] == 90:
							logger.append(serie['id'],'260',{"season":serie['season'],"episode":serie['episode']})
							print(str_result.format('260',str(serie['id']),messages.returnCode['260']))
						else:
							logger.append(serie['id'],'250',{"season":serie['season'],"episode":serie['episode']})
							print(str_result.format('250',str(serie['id']),messages.returnCode['250']))
					else:
						print(str_result.format('240',str(serie['id']),messages.returnCode['240']))
					continue

			if int(serie['status']) in [10,15,20,21] and convert_date(serie['expected']) < date.today(): # If episode broadcast is in the past
				if conf['id'] == 'none':
					self.seriefile.updateSerie(serie['id'],{'status':21})
					logger.append(serie['id'],'221',{"season":serie['season'],"episode":serie['episode']})
					print(str_result.format('221',str(serie['id']),messages.returnCode['221']))
				else:
					if 'tc' not in locals():
						tc = transmissionrpc.Client(
							confTransmission['server'],
							confTransmission['port'],
							confTransmission['user'],
							confTransmission['password']
						)
					else:
						logging.info('connection saved')

					self.seriefile.updateSerie(serie['id'],{'status':20})
					for search in str_search_list:
						try:
							result = mytracker.search(search)
						except requests.exceptions.ConnectionError as e:
							print(e)
							sys.exit()
						nb_result = len(result)
						logging.debug(search + ":" + str(nb_result) + ' result(s)')

						if nb_result > 0: # If at least 1 relevant torrent is found
							result = mytracker.select_torrent(result)
							logging.debug("selected torrent:")
							logging.debug(result)
							torrent = mytracker.download(result['id'])
							new_torrent = add_torrent(torrent, tc, confTransmission['slotNumber'],confTransmission['folder'] is not None)
							self.seriefile.updateSerie(serie['id'],{'status':30, 'slot_id':new_torrent.id})
							break
					if nb_result > 0:
						logger.append(serie['id'],'230',{"season":serie['season'],"episode":serie['episode']})
						print(str_result.format('230',str(serie['id']),messages.returnCode['230']))
					else:
						logger.append(serie['id'],'220',{"season":serie['season'],"episode":serie['episode']})
						print(str_result.format('220',str(serie['id']),messages.returnCode['220']))
			else:
				self.seriefile.updateSerie(serie['id'],{'status':10})
				print(str_result.format('210',str(serie['id']),messages.returnCode['210']))

	def getEpisode(self,serieID,season,episode):
		global t
		t = myTvDB()
		try:
			result = t[serieID][season][episode]
			return {'rtn':'200','result':result}
		except Exception,e:
			return {'rtn':'419','error':messages.returnCode['419']}

	def search(self,pattern):
		global t
		t = myTvDB()
		try:
			result = t.search(pattern)
			if len(result)>0:
				return {'rtn':'200','result':result}
			else:
				return {'rtn':'408','error':messages.returnCode['408'].format(pattern)}
		except Exception,e:
			return {'rtn':'404','error':messages.returnCode['404'].format('TvDB')}

	def logs(self,json_c=False):
		global t
		t = myTvDB()
		logger = Logger(log_file = myConstants.LOG_FILE)
		if json_c:
			result = [ convert_dt2str(i) for i in logger.filter_log()]
		else:
			result = logger.filter_log()
		for i in result:
			i['msg'] = messages.returnCode[i['rtn']]
			if 'args' in i.keys():
				i['msg'] = i['msg'].format(i['args'])
			i['seriesname'] = t[i['serieID']]['seriesname']


		return {'rtn':'200','result': result}

