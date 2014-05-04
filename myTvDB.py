#!/usr/bin/env python
#encoding:utf-8

import sys
import os
from myDate import *
import tvdb_api
import json
import argparse
import string

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

	def getEpisodes(self):
		result = [];
		for key,season in self.items():
			for episode in season.values():
				result.append(episode)
		return result

	def getSeasons(self):
		result = [];
		for key,season in self.items():
			result.append(str(key))
		return result

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-a",
		"--action",
		default='',
		choices=['getSerie','getEpisodes','getEpisode'],
		help='action triggered by the script'
		)
	parser.add_argument(
		"-n",
		"--serieID",
		default='0',
		help='indicates the series ID'
		)
	args = parser.parse_args()
	if args.serieID.isdigit():
		serieID = int(args.serieID)
	else:
		args_split = args.serieID.split(',')
		if all(x.isdigit() for x in args_split) and len(args_split)>2:
			serieID = int(args_split[0])
			season = int(args_split[1])
			episode = int(args_split[2])
		else:
			serieID = 0
			season = 0
			episode = 0
	t = myTvDB()
	if args.action == 'getSerie':
		serie = t[serieID]
		print(json.dumps(serie.data))
	elif args.action == 'getEpisode':
		episode = t[serieID][season][episode]
		print(json.dumps(episode))
	elif args.action == 'getEpisodes':
		print(json.dumps(t[serieID].getEpisodes()))
	'''str_result = '{0} S{1:02}E{2:02}'
	last = t['how i met your mother'].lastAired()
	next = t['how i met your mother'].nextAired()
	print(str_result.format(last['episodename'],int(last['seasonnumber']),int(last['episodenumber'])))
	print(str_result.format(next['episodename'],int(next['seasonnumber']),int(next['episodenumber'])))'''

if __name__ == '__main__':
    main()
