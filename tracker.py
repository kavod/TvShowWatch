#!/usr/bin/env python
#encoding:utf-8

import sys
import json
import requests
import logging
import re
import unicodedata
import string


TRACKER_CONF = [
	['t411','T411']
	]

class Tracker:
	def __init__(self,trackerID,username, password):
		self.token = ''
		tracker_found = False
		for i in TRACKER_CONF:
			if i[0] == trackerID:
				logging.info("tracker : " + str(trackerID))
				self.trackerID = trackerID
				tracker_found = True
				break
		if tracker_found != False:
			token = self.connect(username, password)
			self.username = username
			self.password = password
		else:
			print('tracker ' + str(trackerID) + 'not recognized')

	def connect_t411(self,username, password):
		if not self.token: #If no token, let's connect
			req = requests.post("https://api.t411.me/auth", {'username': username, 'password': password})
			if 'code' not in req.json().keys():
				self.token = req.json()['token']
				self.uid = req.json()['uid']
				return True
			else:
				return False
		else: #If token exist, let's test connection
			if test_t411():
				return True
			else:#If error code returned, token is expired. So let's erase it and reconnect
				self.token = ''
				return connect_t411(username, password)

	def connect(self,username,password):
		return getattr(self, "connect_"+self.trackerID)(username, password)

	def test_t411(self):
		if not self.token: 
			return False
		else: 
			req = requests.post("https://api.t411.me/users/profile/" + self.uid,headers={"Authorization": self.token})
			if 'code' not in req.json().keys():
				return True
			else:
				return False

	def test(self):
		return getattr(self, "test_"+self.trackerID)()

	def search_t411(self, search):
		if not self.test():
			self.connect(self.username, self.password)
		return requests.post("https://api.t411.me/torrents/search/" + search,headers={"Authorization": self.token})

	def search(self,search):
		search = str(''.join(c for c in unicodedata.normalize('NFKD', unicode(search, 'utf-8')) if unicodedata.category(c) != 'Mn'))
		search = re.sub('[%s]' % re.escape(string.punctuation), '', search)
		return getattr(self, "search_" + self.trackerID )(search)

	def download_t411(self,torrent_id):
		logging.debug("/torrents/download/"+str(torrent_id))
		stream = requests.post("https://api.t411.me/torrents/download/"+str(torrent_id),headers={"Authorization": self.token}, stream=True)
		with open('file.torrent', 'wb') as f:
			for chunk in stream.iter_content(chunk_size=1024): 
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
			     		f.flush()

	def download(self,torrent_id):
		return getattr(self, "download_" + self.trackerID )(torrent_id)

	# Deletion of useless torrent (no seeder, not verified and dl never completed
	def filter_torrent(self,tor): 
		return getattr(self, "filter_" + self.trackerID )(tor)

	def filter_t411(self,tor):
		return int(tor['seeders']) > 0 and tor['isVerified'] == '1' and int(tor['times_completed']) > 0

	# Selection of the most downloaded completed time torrent
	def select_torrent(self,result):
		return getattr(self, "select_" + self.trackerID )(result)

	def select_t411(self,result):
		logging.debug(result)
		filter(self.filter_torrent,result)
		return sorted(result, key=lambda tor: int(tor[u'times_completed']), reverse=True)[0]







