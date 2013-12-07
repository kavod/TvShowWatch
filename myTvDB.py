#!/usr/bin/env python
#encoding:utf-8

import sys
import os
from myDate import *
import tvdb_api

class myTvDB(tvdb_api.Tvdb):
	def __init__(self):
		tvdb_api.Tvdb.__init__(self)

	def _setItem(self, sid, seas, ep, attrib, value):
		if sid not in self.shows:
            		self.shows[sid] = myShow()
		return tvdb_api.Tvdb._setItem(self, sid, seas, ep, attrib, value)

	def _setShowData(self, sid, key, value):
		"""Sets self.shows[sid] to a new Show instance, or sets the data
		"""
		if sid not in self.shows:
			self.shows[sid] = myShow()
		return tvdb_api.Tvdb._setShowData(self, sid, key, value)

class myShow(tvdb_api.Show):
	def lastAired(self):
		today = myToday()
		current = tvdb_api.Episode()
		current['firstaired'] = '1900-01-01'

		for key,season in self.items():
			if str(key)=="0":
				continue
			for episode in season.values():
				if convert_date(episode['firstaired'])==None:
					continue
				if convert_date(episode['firstaired']) < today:
					if convert_date(current['firstaired']) < convert_date(episode['firstaired']):
						current = episode
		if current['firstaired'] == '1900-01-01':
			return None
		return current

	def nextAired(self):
		today = myToday()
		current = tvdb_api.Episode()
		current['firstaired'] = '2100-12-31'

		for key,season in self.items():
			if str(key)=="0":
				continue
			for episode in season.values():
				if convert_date(episode['firstaired'])==None:
					continue
				if convert_date(episode['firstaired']) >= today:
					if convert_date(current['firstaired']) > convert_date(episode['firstaired']):
						current = episode
		if current['firstaired'] == '2100-12-31':
			return None
		return current

def main():
	t = myTvDB()
	str_result = '{0} S{1:02}E{2:02}'
	last = t['how i met your mother'].lastAired()
	next = t['how i met your mother'].nextAired()
	print(str_result.format(last['episodename'],int(last['seasonnumber']),int(last['episodenumber'])))
	print(str_result.format(next['episodename'],int(next['seasonnumber']),int(next['episodenumber'])))

if __name__ == '__main__':
    main()
