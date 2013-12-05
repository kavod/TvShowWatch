#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import tvdb_api
import logging
import transmissionrpc
import smtplib
from email.mime.text import MIMEText
from datetime import date
from tracker import *
from myDate import *
from ConfFile import ConfFile
from ftplib import FTP

def convert_conf(conf,root=''):
	if root != '':
		root += '_'
	result = {}
	for key,value in conf.items():
		if (lambda x : any(isinstance(x,y) for y in [int,long,float,str,unicode,basestring,bool,list]))(value):
			result[root+key] = value
		elif (lambda x : any(isinstance(x,y) for y in [dict]))(value):
				result.update(convert_conf(value,root+key))
		else:
			return {}
	return result

def last_aired(serie_id,s_season=0,s_episode=0):
	global t
	if 't' not in globals():
		t = tvdb_api.Tvdb()
	else:#ICI
		logging.info('Connection saved')

	logging.debug('API initiator: %s', t)
	result = []
	last_episode = {'seasonnumber': 0, 'episodenumber': 0, 'firstaired': datetime.date(1900,1,1) }
	next_episode = {'seasonnumber': 0, 'episodenumber': 0, 'firstaired': datetime.date(1900,1,1) }

	try:
		#for serie_id in series:
		if not isinstance(serie_id,int):
			serie_id = serie_id.find('id').text
		serie = t[int(serie_id)]
	except Exception,e:
		return {}
	# Delete of Special season
	if 0 in serie.keys():
		del serie[0]

	nb_seasons = len(serie)
	if int(s_season)*int(s_episode)>0:
		return	{
			'id':		int(serie_id),
			'seriesname':	serie.data['seriesname'],
			'next':	{
				'season':	int(s_season),
				'episode':	int(s_episode),
				'aired':	convert_date(serie[int(s_season)][int(s_episode)]['firstaired'])
				}
			}
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

	return	{
			'id':		int(serie_id),
			'seriesname':	serie.data['seriesname'],
			'last':	{
				'season':	int(last_episode['seasonnumber']),
				'episode':	int(last_episode['episodenumber']),
				'aired':	last_episode['firstaired']
				},
			'next':	{
				'season':	int(next_episode['seasonnumber']),
				'episode':	int(next_episode['episodenumber']),
				'aired':	next_episode['firstaired']
				}
		}

def sendEmail(content,serie,conffile):
	confEmail = conffile.getEmail()
	if len(confEmail)>0:
		msg = MIMEText(content)
		msg['Subject'] = 'File download is completed!'
		msg['From'] = 'TvShowWatch script'
		s = smtplib.SMTP(confEmail['server'],confEmail['port'])
		s.starttls()
		s.login(confEmail['user'],confEmail['password'])
		for email in serie['emails']:
			if msg.has_key('To'):
				msg.replace_header('To', email)
			else:
				msg['To'] = email
			s.sendmail(confEmail['emailSender'],email,msg.as_string())
		s.quit()

def transferFile(fichiers,serie,conf):
	try:
		ftp = FTP(conf['server'])
		ftp.login(conf['user'],conf['password']) 
		for fichier in fichiers.values():
			pattern = '{0}/season {1}/{2}'
			chemin_cible = pattern.format(
					str(serie['name']),
					str(serie['season']),
					"/".join(fichier['name'].split('/')[0:-1])
							)
			chemin = conf['folder'] + '/'
			for folder in chemin_cible.split('/'):
				if not os.path.isdir(chemin + folder):
					os.mkdir(chemin + folder)
				chemin += folder + '/'
			ftp.retrbinary(
				'RETR ' + str(fichier['name']), 
				open(conf['folder'] + '/' + chemin_cible + '/' + str(fichier['name'].split('/')[-1]), 'wb').write)
		ftp.quit()
		print(' => File download is completed!')
		return True
	except:
		print('Error during transfer :'+sys.exc_info()[1].strerror)
		return False

def add_torrent(result, tc, tracker,confTransmission):
	result = tracker.select_torrent(result)
	logging.debug("selected torrent:")
	logging.debug(result)
	tracker.download(result['id'])

	torrents = tc.get_torrents()
	torrents = filter(ignore_stopped,torrents)

	while len(torrents) >= int(confTransmission['slotNumber']):
		# If there is not slot available, close the older one
		torrents = filter(keep_in_progress,torrents)
		torrent = sorted(torrents, key=lambda tor: tor.id, reverse=True)[0]
		tc.remove_torrent(torrent.id, delete_data=True)
		logging.info("Maximum slot number reached, deletion of the oldest torrent : {0}".format(torrent.name))
		torrents = tc.stop_torrent(torrent.id)
		torrents = tc.get_torrents()
	
	new_torrent = tc.add_torrent('file://file.torrent')
	os.remove('file.torrent')
	tc.start_torrent(new_torrent.id)
	return new_torrent

def keep_in_progress(tor):
	return tor.status == 'seeding'

def ignore_stopped(tor):
	return tor.status != 'stopped'

