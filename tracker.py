#!/usr/bin/env python
#encoding:utf-8

from __future__ import absolute_import
import os
import sys
import inspect
import json
import requests
import logging
import re
import unicodedata
import string
import imp
from myExceptions import *

TMPPATH = "/tmp"

TRACKER_CONF = [
	{'id':'t411','name':'T411','url':'https://api.t411.io','param':['username','password']},
	{'id':'kickass','name':'KickAss','url':"https://kickass.to",'param':[]},
	{'id':'none','name':'No tracker, only manual push','url':"",'param':[]}
	]

def check_provider(trackerID):
	# Selecting requested provider
	provider = [x for x in TRACKER_CONF if x['id'] == trackerID]
	if len(provider) < 1:
		raise InputError('trackerID','tracker ' + str(trackerID) + ' not recognized')
		return False
	else:
		return provider[0]

class Tracker:
	def __init__(self,trackerID,param_data,tmppath = TMPPATH ):
		self.provider = {} 		# Provider data
		self.token = ''			# If required by provider, authentification token
		self.param = {}			# If required by provider, extra parameters (like username / password)
		self.tmppath = tmppath

		# Selecting requested provider
		try:
			self.provider = check_provider(trackerID)
		except InputError as e:
			raise InputError(e.expr,e.msg)

		# Populating paramerters
		for param in self.provider['param']:
			if param in param_data.keys():
				self.param[param] = param_data[param]
			else:
				print("Missing parameter: "+param)

	def connect_t411(self):
		if not self.token: #If no token, let's connect
			req = requests.post(self.provider['url']+"/auth", {'username': self.param['username'], 'password': self.param['password']}, verify=False)
			if 'code' not in req.json().keys():
				self.token = req.json()['token']
				self.uid = req.json()['uid']
				return True
			else:
				raise requests.exceptions.ConnectionError('Unable to login on T411. Please check username/password')
		else: #If token exist, let's test connection
			if test_t411():
				return True
			else:#If error code returned, token is expired. So let's erase it and reconnect
				self.token = ''
				return self.connect_t411()

	def connect_kickass(self):
		return self.test_kickass()
			
	def connect_none(self):
		self.token = 'ok'
		return True

	def connect_tpb(self):
		self.token = tpb.TPB(self.provider['url'])
		return True

	def connect(self):
		return getattr(self, "connect_"+self.provider['id'])()

	def test_t411(self):
		if not self.token: 
			return False
		else: 
			req = requests.post(self.provider['url']+"/users/profile/" + self.uid,headers={"Authorization": self.token}, verify=False)
			if 'code' not in req.json().keys():
				return True
			else:
				return False

	def test_kickass(self):
		req = requests.post(self.provider['url']+"/json.php", verify=False)
		if 'title' not in req.json().keys():
			return True
		else:
			return False

	def test_none(self):
		return True

	def test_tpb(self):
		if not self.token: 
			return False
		else: 
			return True

	def test(self):
		return getattr(self, "test_"+self.provider['id'])()

	def search_t411(self, search):
		if not self.test():
			self.connect()
		result = requests.post(self.provider['url']+"/torrents/search/" + search,headers={"Authorization": self.token}, verify=False).json()
		logging.debug('%s', result)
                if 'torrents' in result.keys():
                        result = result['torrents']
                        logging.debug('%s torrents found', int(len(result)))
                        result = filter(self.filter_t411,result)
                        return result
                else:
                        return []
						
	def search_kickass(self, search):
		if not self.test():
			self.connect()
		params = {'q':search}
		result = requests.post(self.provider['url']+"/json.php",params=params, verify=False).json()
		logging.debug('%s', result)
                if 'list' in result.keys():
                        result = result['list']
                        logging.debug('%s torrents found', int(len(result)))
                        result = filter(self.filter_kickass,result)
                        return result
                else:
                        return []

	def search_none(self,search):
		return []

	def search_tpb(self,search):
		if not self.test():
			self.connect()
		result = []
		for tor in self.token.search(search):
			result.append({
				'seeders': int(tor.seeders),
				'leechers': int(tor.leechers),
				'name':		str(tor.title),
				'isVerified': '1',
				'magnet_link': str(tor.magnet_link)
						})
		return result
				

	def search(self,search):
		search = str(''.join(c for c in unicodedata.normalize('NFKD', unicode(search, 'utf-8')) if unicodedata.category(c) != 'Mn'))
		search = re.sub('[%s]' % re.escape(string.punctuation), '', search)
		return getattr(self, "search_" + self.provider['id'] )(search)

	def download_t411(self,torrent_id):
		logging.debug("/torrents/download/"+str(torrent_id))
		stream = requests.post(self.provider['url']+"/torrents/download/"+str(torrent_id),headers={"Authorization": self.token}, stream=True, verify=False)
		with open(TMPPATH + '/file.torrent', 'wb') as f:
			for chunk in stream.iter_content(chunk_size=1024): 
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
			     		f.flush()
		return 'file://' + TMPPATH + '/file.torrent'
		
	def download_kickass(self,torrent_id):
		logging.debug(str(torrent_id))
		stream = requests.post(str(torrent_id), stream=True, verify=False)
		with open(TMPPATH + '/file.torrent', 'wb') as f:
			for chunk in stream.iter_content(chunk_size=1024): 
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
			     		f.flush()
		return 'file://' + TMPPATH + '/file.torrent'

	def download_none(self,torrent_id):
		return False

	def download_tpb(self,torrent_id):
		return torrent_id

	def download(self,torrent_id):
		return getattr(self, "download_" + self.provider['id'] )(torrent_id)

	# Deletion of useless torrent (no seeder, not verified and dl never completed
	def filter_torrent(self,tor): 
		return getattr(self, "filter_" + self.provider['id'] )(tor)

	def filter_t411(self,tor):
		return int(tor['seeders']) > 0 and tor['isVerified'] == '1' and int(tor['times_completed']) > 0

	def filter_tpb(self,tor):
		return int(tor['seeders']) > 0 and tor['isVerified'] == '1' > 0

	def filter_kickass(self,tor):
		return int(tor['seeds']) > 0 and tor['verified'] == 1 and int(tor['votes']) > 0
		
	def filter_none(self,tor):
		return True

	# Selection of the most downloaded completed time torrent
	def select_torrent(self,result):
		return getattr(self, "select_" + self.provider['id'] )(result)

	def select_t411(self,result):
		logging.debug(result)
		#filter(self.filter_torrent,result)
		return sorted(result, key=lambda tor: int(tor[u'times_completed']), reverse=True)[0]

	def select_tpb(self,result):
		logging.debug(result)
		#filter(self.filter_torrent,result)
		return {'id':sorted(result, key=lambda tor: int(tor['seeders']), reverse=True)[0]['magnet_link']}

	def select_kickass(self,result):
		logging.debug(result)
		#filter(self.filter_torrent,result)
		return {'id':sorted(result, key=lambda tor: int(tor[u'votes']), reverse=True)[0]['torrentLink']}
		
	def select_none(self,result):
		logging.debug(result)
		return result[0]





