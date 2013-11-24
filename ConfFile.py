#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import xml.etree.ElementTree as ET
import transmissionrpc
import smtplib
import logging
from transmissionrpc.error import TransmissionError, HTTPHandlerError
from email.mime.text import MIMEText
from Prompt import *
from myDate import *
from tracker import *
from MyFile import *

CONFIG_FILE = sys.path[0] + 'config.xml' if sys.path[0] != '' else 'config.xml'
CONFIG_VERSION = '1.8'

TORRENT_STATUS = {
			10: 'Waiting Broadcast',
			20: 'Waiting Torrent',
			30: 'Leeching'
		}

class ConfFile(MyFile):
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
		MyFile.__init__(self, 'conf', 'configuration')

	def openFile(self,filename = CONFIG_FILE):
		return MyFile.openFile(self,filename,False)

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
		conf = self.tree.getroot()
		#conf = self._create_root()
                tracker_conf = self.confTracker()
                tc_conf = self.confTransmission()
                email_conf = self.confEmail()
                self.changeKeywords()


		# Transmission conf
		transmission = conf.find('transmission')
		tc_folder = ET.SubElement(transmission, "folder")
		tc_folder.text = str(tc_conf['folder'])

		self._save()
		return True

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
			username = self.change('tracker_user')
			password = self.change('tracker_password')
			
			#tracker = Tracker(tracker_id,username,password)
			#if tracker.test():
			if self.testTracker()['rtn']=='200':
				break
			else:
				print('Invalid authentification')
			
		self._save()
		return {
			'id': 		tracker_id, 
			'username': 	username,
			'password':	password
			}

	def testTracker(self):
		logging.info('testTracker')
		trackerConf = self.getTracker()
		if trackerConf['id'] == '' or trackerConf['user'] == '':
			return {'rtn':'405','error':messages.returnCode['405'].format('Tracker')}
		try:
			tracker = Tracker(trackerConf['id'],trackerConf['user'],trackerConf['password'])
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
			"""try:
				self.tc = transmissionrpc.Client(server, port, user, password)
			except Exception as inst:
				print('Transmission authentification failed')
			else:
				break"""

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

	def confEmail(self):
		if (promptYN("Do you want to activate Email notification?",'N')):
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

				"""
				try:
					msg = MIMEText('This is a test email')
					msg['Subject'] = 'This is a test email'
					msg['From'] = 'TvShowWatch script'
					msg['To'] = emailSender
					s = smtplib.SMTP(server,int(port))
					if ssltls:
						s.starttls() 
					if user != '':
						s.login(user,password) 
					s.sendmail(emailSender,emailSender,msg.as_string())
					s.quit()
				except Exception as inst:
					print('SMTP email sent failed')
				"""
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
		conf = self.tree.getroot().find('tracker')
		"""if conf.find('keywords') is not None:
			keywords = conf.find('keywords').text 
		else:
			keywords = '' """
		if conf is not None and conf.find('id') is not None and conf.find('user') is not None and conf.find('password') is not None:
			return {
				'id':		conf.find('id').text,
				'user':		conf.find('user').text,
				'password':	conf.find('password').text
				}
		else:
			return {
				'id':		'',
				'user':		'',
				'password':	''
				}

	def changeKeywords(self,keywords=[]):
		if len(keywords) < 1:
			keywords = promptList('Enter your keywords [keep blank to save]:')
		conf = self.tree.getroot()
		if conf.find('keywords') is not None:
			keywordsNode = conf.find('keywords')
			for keywordNode in keywordsNode.findall('keyword'):
				keywordsNode.remove(keywordNode)
		else:
			keywordsNode = ET.SubElement(conf, "keywords")
		for keyword in keywords:
			keywordNode = ET.SubElement(keywordsNode, "keyword")
			keywordNode.text = str(keyword)

	def getKeywords(self):
		conf = self.tree.getroot().find('keywords')
		keywords_list = []
		if conf is not None:
			for keyword in conf.findall('keyword'):
				keywords_list.append(keyword.text)
		return keywords_list

	def getTransmission(self):
		transmission = self.tree.getroot().find('transmission')
		if (transmission is not None and (lambda x : all(transmission.find(y) is not None for y in x))(['server','port','user','password','slotNumber'])):
			return {
				'server':	transmission.find('server').text,
				'port':		transmission.find('port').text,
				'user':		transmission.find('user').text,
				'password':	transmission.find('password').text,
				'slotNumber':	transmission.find('slotNumber').text,
				'folder':	transmission.find('folder').text if transmission.find('folder') is not None else ''
				}
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
		smtp = self.tree.getroot().find('smtp')
		if (smtp is not None and (lambda x : all(smtp.find(y) is not None for y in x))(['server','port','ssltls','emailSender'])):
			if smtp is None:
				return {}
			else:
				return {
					'server':	smtp.find('server').text,
					'port':		int(smtp.find('port').text),
					'ssltls':	smtp.find('ssltls').text == 'True',
					'user':		'' if smtp.find('user') is None else smtp.find('user').text,
					'password':	'' if smtp.find('password') is None else smtp.find('password').text,
					'emailSender':	smtp.find('emailSender').text
					}
		else:
			return {}

	def select_tracker_id(self):
		return promptChoice("Please select your tracker:",TRACKER_CONF)

	def select_tracker_user(self):
		return promptSimple('Enter your username:')

	def select_tracker_password(self):
		return promptPass('Enter your password:')


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
		
