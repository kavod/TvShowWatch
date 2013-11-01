#!/usr/bin/env python
#encoding:utf-8

import sys
import os
import tvdb_api
import time
import string
import argparse
import xml.etree.ElementTree as ET
from myDate import *
from types import *
from Prompt import *
from ConfFile import ConfFile

CONFIG_FILE = 'series.xml'

def last_aired(t,series):
	
	result = []
	last_episode = {'seasonnumber': 0, 'episodenumber': 0, 'firstaired': datetime.date(1900,1,1) }
	next_episode = {'seasonnumber': 0, 'episodenumber': 0, 'firstaired': datetime.date(1900,1,1) }

	for serie_id in series:
		if type(serie_id) is not IntType:
			serie_id = serie_id.find('id').text
		serie = t[int(serie_id)]
		# Delete of Special season
		if 0 in serie.keys():
			del serie[0]

		nb_seasons = len(serie)

		for episode in serie[nb_seasons].values():
		 
		 if episode['firstaired'] is not None:
		  date_firstaired = convert_date(episode['firstaired'])
		  if date_firstaired > datetime.date.today():
			next_episode = episode
		  	next_episode['firstaired'] = date_firstaired
		  	break
		  else:
		   last_episode = episode
		   last_episode['firstaired'] = date_firstaired

		result.append(
			[serie.data['seriesname'],
			last_episode['seasonnumber'],
			last_episode['episodenumber'],
			last_episode['firstaired'],
			next_episode['seasonnumber'],
			next_episode['episodenumber'],
			next_episode['firstaired']])
	return result

def do_run(conffile,t):
	series = last_aired(t,conffile.listSeries())
	for serie in series:
		print(serie[0] + " - Season " + serie[1] + " Episode " + serie[2] + " broadcasted on " + print_date(serie[3]))

def do_list(conffile,t):
	series = conffile.listSeries()
	if len(series)>0:	
		for serie in series:
			print t[serie].data['seriesname']
	else:
		print "No TV Show scheduled"
		sys.exit()

def do_add(conffile,t):
	result = []
	while len(result) < 1:
		serie = promptSimple("Please type your TV Show ")
		result = t.search(serie)

		if len(result) == 0:
			print "Unknowned TV Show"
		elif len(result) > 1:
			choices = []
			for val in result:
				choices.append([val['id'],val['seriesname']+' (' + val['firstaired'][0:4] + ')'])
			result = promptChoice("Did you mean...",choices)
			result = t[result]

		elif len(result) == 1:
			result = t[result[0]['id']]

	if conffile.testSerieExists(int(result.data['id'])):
		print(u'Already scheduled TV Show')
		sys.exit()

	serie = last_aired(t,[int(result.data['id'])])
	serie = serie[0]

	if (serie[1] == 0):
		if promptYN("Last season not yet started. Do you want to schedule the Season pilot on " + print_date(serie[6]),'y'):
			next_s = serie[4]
			next_e = serie[5]
		else:
			sys.exit()
	elif (serie[4] == 0):
		if promptYN("Last season achieved. Do you want to download the Season final on " + print_date(serie[3]),'n'):
			next_s = serie[4]
			next_e = serie[5]
		else:
			sys.exit()	
	else:		
		if promptYN("Next episode download scheduled on " + print_date(serie[6]) + "\nDo you want also download the last aired : S" + serie[1] + "E" + serie[2] + " - " + print_date(serie[3]) + " ?",'N'):
			next_s = serie[1]
			next_e = serie[2]
		else:
			next_s = serie[4]
			next_e = serie[5]

	conffile.addSerie(result.data['id'],next_s,next_e)

	print(result.data['seriesname'] + u" added")

def main():
	conffile = ConfFile(CONFIG_FILE)
	t = tvdb_api.Tvdb()

	parser = argparse.ArgumentParser()
	parser.add_argument("--action",default='run')
	args = parser.parse_args()
	if args.action == 'run':
		do_run(conffile,t)

	elif args.action == 'list':
		do_list(conffile,t)

	elif args.action == 'reset':
		conffile.reset()

	elif args.action == 'add':
		do_add(conffile,t)

if __name__ == '__main__':
    main()

