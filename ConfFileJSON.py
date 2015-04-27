#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import transmissionrpc
import smtplib
import logging
import myConstants
from transmissionrpc.error import TransmissionError, HTTPHandlerError
from email.mime.text import MIMEText
from Prompt import *
from myDate import *
from myExceptions import *
from tracker import *
import MyFileJSON
import messages

CONFIG_VERSION = '2.0'

TORRENT_STATUS = {
			10: 'Waiting Broadcast',
			20: 'Waiting Torrent',
			30: 'Leeching'
		}

class ConfFile(MyFileJSON.MyFile):
	"""
		The ``ConfFile`` constructor
		============================
		
		Create the ConfFile object
		
		:param filename: Filename
		:type question: string


		:Example:

		>>> f = ConfFile()		
	"""
	def __init__(self):
		MyFileJSON.MyFile.__init__(self, 'conf', 'configuration')

	def openFile(self,filename = myConstants.CONFIG_FILE,createIfNotExist=False):
		return MyFileJSON.MyFile.openFile(self,filename,createIfNotExist)

	def _version(self):
		return CONFIG_VERSION
	"""
		The ``_create`` method
		=============================
		
		Use it for create a blank configuration file.

		.. warnings:: No confirmation required. If file already exists, it will be erase!!!
		.. seealso:: ``reset``

		:return: True if file creation is OK
		:rtype: boolean

		:Example:

		>>> f._create()
		True
		
	"""
	def _create(self,df_tracker={},df_tc={},df_email={}): #Passage en None
		result = MyFileJSON.MyFile._create(self)
		self.tree['version'] = CONFIG_VERSION
		tracker_conf = self.confTracker()
		tc_conf = self.confTransmission()
		email_conf = self.confEmail()
		self.changeKeywords()

		# Transmission conf
		transmission = conf['transmission']['folder'] = str(tc_conf['folder'])

		self._save()
		return result

	"""
		The ``confTracker`` method
		=========================
		
		Create Tracker configuration

		:return: list [tracker ID, username, password]
		:rtype: list of strings

		:Example:
		f.confTracker()
		['t411', 'obiWan', '1324']
		
	"""
	def confTracker(self):
		while True:
			tracker_id = self.change('tracker_id')
			try:
				provider = check_provider(tracker_id)
				for param in provider['param']:
					if param == 'username':
						username = self.change('tracker_user')
					elif param == 'password':
						password = self.change('tracker_password')
					else:
						raise InputError('param','Unknown parameter name: '+param)
			except InputError as e:
				print(e.msg)
				sys.exit()
			
			if self.testTracker()['rtn']=='200':
				break
			else:
				print('Invalid authentification')
			
		self._save()
		return {
			'id': 		tracker_id, 
			'user': 	username,
			'password':	password
			}

	def testTracker(self):
		logging.info('testTracker')
		trackerConf = self.getTracker()
		try:
			provider = check_provider(trackerConf['id'])
			if 'username' in provider['param'] and trackerConf['user'] == '':
				return {'rtn':'422','error':messages.returnCode['422'].format(provider['name'])}
			tracker = Tracker(trackerConf['id'],{'username':trackerConf['user'],'password':trackerConf['password']})
		except InputError as e:
			return {'rtn':'404','error':messages.returnCode['404'].format('Tracker',e.msg)}
		except Exception,e:
			return {'rtn':'404','error':messages.returnCode['404'].format('Tracker',e)}
		else:
			return {'rtn':'200','error':messages.returnCode['200']}

	"""
		The ``confTransmission`` method
		===============================
		
		Create Transmission configuration

		:return: {'server', 'port', 'username', 'password', 'slotNumber'}
		:rtype: dict

		:Example:
		f.confTransmission()
		{
			'server':	'localhost',
			'port':		'9091',
			'username':	'ObiWan',
			'password':	'1234',
			'slotNumber':	6
		}
		
	"""
	def confTransmission(self):
		while True:	
		
			server = self.change('transmission_server')
			port = self.change('transmission_port')
			user = self.change('transmission_user')
			password = self.change('transmission_password')
			slotNumber = self.change('transmission_slotNumber')
			self._save()
			folder = self.change('transmission_folder')
			#folder = self.select_transmission_folder()
			test = self.testTransmission()
			if (test['rtn']=='200'):
				break
			else:
				print(test['error'])

		self._save()

		return {
			'server':	server,
			'port':		port,
			'user':		user,
			'password':	password,
			'slotNumber':	slotNumber,
			'folder':	folder
			}

	def testTransmission(self):
		tc = self.getTransmission()
		if tc['server'] == '' or tc['port'] == '':
			 return {'rtn':'405','error':messages.returnCode['405'].format('Transmission')}
		try:
			transmissionrpc.Client(tc['server'], tc['port'], tc['user'], tc['password'])
		except TransmissionError,e:
			return {'rtn':'404','error':messages.returnCode['404'].format('Transmission',e)}
		else:
			return {'rtn':'200','error':messages.returnCode['200']}

	def confEmail(self,disable=False):
		if (not disable and promptYN("Do you want to activate Email notification?",'N')):
			while True:
				server = self.change('smtp_server')
				port = self.change('smtp_port')
				ssltls = self.change('smtp_ssltls')
				if (promptYN("Authentification required?",'N')):
					user = self.change('smtp_user')
					password = self.change('smtp_password')
				else:
					user = ''
					password = ''
				emailSender = self.change('smtp_emailSender')
				
				if (self.testEmail()['rtn']=='200'):
					break
				else:
					print('Error sending test Email')

			self._save()

			return {
				'server':	server,
				'port':		port,
				'ssltls':	ssltls,
				'user':		user,
				'password':	password,
				'emailSender':	emailSender
				}
		else:
			if 'smtp' in conf.keys() and len(conf['smtp'].key()) > 0:
				del conf['smtp']
			self._save()
			return {}

	def testEmail(self,send=False):
		email = self.getEmail()
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

	def getTracker(self):
		logging.info('getTracker')
		if 'tracker' not in self.tree.keys():
			self.tree['tracker'] = {}
			self._save()
		return {
				'id':		self.tree['tracker']['id'] if 'id' in self.tree['tracker'] else '',
				'user':		self.tree['tracker']['user'] if 'user' in self.tree['tracker'] else '',
				'password':	self.tree['tracker']['password'] if 'password' in self.tree['tracker'] else ''
				}

	def changeKeywords(self,keywords=[]):
		if len(keywords) < 1:
			keywords = promptList('Enter your keywords [keep blank to save]:')
		if keywords == 'None':
			keywords=[]
		conf = self.tree
		conf['keywords'] = keywords

	def getKeywords(self):
		if 'keywords' in self.tree.keys():
			return self.tree['keywords']
		else:
			return []

	def getTransmission(self):
		if 'transmission' in self.tree.keys():
			return self.tree['transmission']
		else:
			return {
				'server':	'',
				'port':		'',
				'user':		'',
				'password':	'',
				'slotNumber':	'',
				'folder':	''
				}

	def getEmail(self):
		if 'smtp' in self.tree.keys():
			return self.tree['smtp']
		else:
			return {}

	def select_tracker_id(self):
		tracker_list = []
		for tracker in TRACKER_CONF:
			tracker_list.append([tracker['id'],tracker['name']])
		return promptChoice("Please select your tracker:",tracker_list)

	def select_tracker_user(self):
		return promptSimple('If required by tracker, enter your username (else, press Enter):')

	def select_tracker_password(self):
		return promptPass('If required by tracker, enter your password (else, press Enter):')

	def select_transmission_server(self):
		return promptSimple('Enter your Transmission server:','localhost')

	def select_transmission_port(self):
		return int(promptSimple('Enter your Transmission port:','9091'))

	def select_transmission_user(self):
		return promptSimple('Enter your Transmission username:')

	def select_transmission_password(self):
		return promptPass('Enter your Transmission password:')

	def select_transmission_slotNumber(self):
		return promptSimple('Enter your maximum slot number:','6')

	def select_transmission_folder(self):
		if (promptYN("Once downloaded, do you need local file transfer?",'N')):
			return promptSimple('Enter the destination folder:','.')
		else:
			return ''

	def select_smtp_server(self):
		return promptSimple('Enter your SMTP server:','localhost')

	def select_smtp_port(self):
		return int(promptSimple('Enter your SMTP port:','25'))

	def select_smtp_ssltls(self):
		return promptYN('Secure connection (SSL/TLS) is required?','N')

	def select_smtp_user(self):
		return promptSimple('Enter your SMTP username:')

	def select_smtp_password(self):
		return promptPass('Enter your SMTP password:')

	def select_smtp_emailSender(self):
		return promptSimple('Enter the sender Email (a test email will be sent to it)')
		
