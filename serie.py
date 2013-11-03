#!/usr/bin/env python
#encoding:utf-8

import sys
import os
import tvdb_api
import time
from datetime import date
import string
import logging
import argparse
import xml.etree.ElementTree as ET
import transmissionrpc
from myDate import *
from types import *
from Prompt import *
from ConfFile import ConfFile
from tracker import *



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
		  if date_firstaired >= datetime.date.today():
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


def keep_in_progress(tor):
	return tor.status == 'seeding'

def action_run(conffile,t):
	confTracker = conffile.getTracker()
	tracker = Tracker(confTracker[0],confTracker[1],confTracker[2])
	#series = last_aired(t,conffile.listSeries())
	series = conffile.listSeries()	

	for serie in series:
		if serie['episode'] == 0:
			print(t[serie['id']].data['seriesname'])
			print(' => broadcast achieved - No more episode')
			continue

		episode = t[serie['id']][serie['season']][serie['episode']]
		str_search = '{0} S{1:02}E{2:02} {3}'
		print(
			str_search.format(
				t[serie['id']].data['seriesname'],
				int(serie['season']),
				int(serie['episode']),
				confTracker[3])
				 + ' broadcasted on ' + print_date(convert_date(episode['firstaired'])))

		if serie['status'] == 30: # Torrent already active
			confTransmission = conffile.getTransmission()
			tc = transmissionrpc.Client(
					confTransmission['server'],
					confTransmission['port'],
					confTransmission['user'],
					confTransmission['password']
			
			)

			tor_found = False
			for tor in tc.get_torrents(): # Check if torrent still there!
				if tor.id == serie['slot_id']:
					tor_found = True
					break
			if not tor_found:
				print(' => Torrent unfoundable. Relaunch required')
				conffile.updateSerie(serie['id'],{'status':10,'slot_id':0})
			else:
				torrent = tc.get_torrent(serie['slot_id'])
				if torrent.status == 'seeding':
					print(' => Torrent download in completed!')
				else:
					print(' => Torrent download in progress')
				continue

		if convert_date(episode['firstaired']) < date.today():
			conffile.updateSerie(serie['id'],{'status':20})
			
			result = tracker.search(str_search.format(t[serie['id']].data['seriesname'],int(serie['season']),int(serie['episode']),confTracker[3]))
			nb_result = int(result.json()['total'])
			logging.debug(str(nb_result) + ' result(s)')

			if nb_result > 0:
				result = tracker.select_torrent(result.json()['torrents'])
				logging.debug("selected torrent:")
				logging.debug(result)
				print(" => Download torrent!")
				tracker.download(result['id'])
				confTransmission = conffile.getTransmission()
				tc = transmissionrpc.Client(
						confTransmission['server'],
						confTransmission['port'],
						confTransmission['user'],
						confTransmission['password']
				
				)

				torrents = tc.get_torrents()
				#print(str(len(torrents)) + " >= " + str(confTransmission['slotNumber']) + " ?")
				while len(torrents) >= int(confTransmission['slotNumber']):
					# If there is not slot available, close the older one
					torrents = filter(keep_in_progress,torrents)
					torrent = sorted(torrents, key=lambda tor: tor.id, reverse=True)[0]
					tc.remove_torrent(torrent.id, delete_data=True)
					print("Maximum slot number reached, deletion of the oldest torrent : {0}".format(torrent.name))
					torrents = tc.stop_torrent(torrent.id)
					torrents = tc.get_torrents()
					print(torrents)
				
				new_torrent = tc.add_torrent('file://file.torrent')
				tc.start_torrent(new_torrent.id)
				conffile.updateSerie(serie['id'],{'status':30, 'slot_id':new_torrent.id})
			else:
				print(" => No available torrent")
		else:
			str_search = '{0} S{1:02}E{2:02} {3}'
			print(
				str_search.format(
					t[serie['id']].data['seriesname'],
					int(serie['season']),
					int(serie['episode']),
					confTracker[3])
					 + '\n => Next broadcast: ' + print_date(convert_date(episode['firstaired'])))


def action_list(conffile,t):
	series = conffile.listSeries()
	if len(series)>0:	
		for serie in series:
			print t[serie['id']].data['seriesname']
	else:
		print "No TV Show scheduled"
		sys.exit()

def action_add(conffile,t):
	result = []
	while len(result) < 1:
		serie = promptSimple("Please type your TV Show ")
		result = t.search(serie)

		if len(result) == 0:
			print "Unknowned TV Show"
		elif len(result) > 1:
			choices = []
			for val in result:
				if not 'firstaired' in val.keys():
					val['firstaired'] = '????'
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

def action_reset(conffile, t):
    '''Reset the series list'''
    logging.debug('Call function action_reset()')
    conffile.reset()

def action_del(conffile, t):
	'''Delete TV show from configuration file'''
	logging.debug('Call function action_del()')
	choix = []
	series = conffile.listSeries()
	if len(series)>0:	
		for serie in series:
			choix.append([serie['id'],t[serie['id']].data['seriesname']])
	else:
		print "No TV Show scheduled"
		sys.exit()
	s_id = promptChoice("Which TV Show do you want to unschedule?",choix)
	conffile.delSerie(s_id)

def action_config(conffile, t):
    '''Change configuration'''
    logging.debug('Call function action_config()')
    trackerConf = conffile.getTracker()
    configData = promptChoice(
            "Selection value you want modify:",
            [
                ['tracker','Tracker : '+trackerConf[0]],
                ['user','Tracker Username : '+trackerConf[1]],
                ['password','Tracker Password : ******'],
                ['keywords','Tracker default keywords : '+str(trackerConf[3])]
            ])
    conffile.change(configData)

def main():

    # Get input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-a",
            "--action",
            default='run',
            choices=['run', 'list', 'reset', 'add','config','del'],
            help='action triggered by the script'
        )
    parser.add_argument(
            "-v",
            "--verbosity",
            action="store_true",
            help='maximum output verbosity'
        )
    args = parser.parse_args()

    # Manage verbosity level
    if args.verbosity:
        logging.basicConfig(level=logging.DEBUG)
    logging.info('SERIES started in verbosity mode')

    # Initialize more data
    conffile = ConfFile(CONFIG_FILE)
    logging.debug('Conffile: %s', conffile)
    t = tvdb_api.Tvdb()
    logging.debug('API initiator: %s', t)
    action_fct = {
            'list':action_list,
            'run':action_run,
            'add':action_add,
            'reset':action_reset,
            'config':action_config,
            'del':action_del
        }

    # Call for action
    logging.debug('Action from the parameter: %s', args.action)
    fct = action_fct[args.action]
    logging.debug('Action function: %s', fct)

    fct(conffile, t)

if __name__ == '__main__':
    main()

