#!/usr/bin/env python
#encoding:utf-8

import sys
import json
import requests
#from t411 import *

TRACKER_CONF = [
	['t411','T411']
	]

class Tracker:
	def __init__(self,trackerID,username, password):
		self.token = ''
		tracker_found = False
		for i in TRACKER_CONF:
			if i[0] == trackerID:
				print("tracker : " + str(trackerID))
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
		return getattr(self, "search_" + self.trackerID )(search)

