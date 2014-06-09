#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import logging
import transmissionrpc
import smtplib
from email.mime.text import MIMEText
from datetime import date
from myDate import *
from myTvDB import *
from ConfFile import ConfFile
from ftplib import FTP


"""CONFIG_FILE = sys.path[0] + '/config.xml' if sys.path[0] != '' else 'config.xml'
LIST_FILE = sys.path[0] + '/series.xml' if sys.path[0] != '' else 'series.xml'
TMP_PATH = "/tmp"
LOG_PATH = "/tmp"
PATH = {'configpath':CONFIG_FILE,'seriepath':LIST_FILE,'tmppath':TMP_PATH, 'logpath':LOG_PATH}

def load_directories():
	# Load directories paths
	global PATH, CONFIG_FILE, LIST_FILE, TMP_PATH, LOG_PATH
	#print("Start of load_directories : " + CONFIG_FILE)
	try:
		dir_file_folder = sys.path[0] + '/directory.json' if sys.path[0] != '' else 'directory.json'
		json_data = open(dir_file_folder)
		PATH = dict(json.load(json_data))
		CONFIG_FILE = PATH['configpath'] + '/config.xml'
		LIST_FILE = PATH['seriepath'] + '/series.xml'
		TMP_PATH = PATH['tmppath']
		LOG_PATH = PATH['logpath']
	except: # If directory file reading failed
		print("Fail to open directory file:" + dir_file_folder)
		sys.exit()
	print("End of load_directories : " + CONFIG_FILE)"""

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
'''
	The ``next_aired`` function
	=============================
	
	Retrieve the next step for TV Show schedule.

	:param serie_id: TV Show identifier (from theTVDB)
	:type serie_id: integer
	:param s_season: Season number of the last downloaded episode. If blank or 0 => get the last aired season
	:type s_season: integer
	:param s_season: Episode number in the season of the last downloaded episode. If blank or 0 => get the last aired episode
	:type s_episode: integer

	:return: data for the next episode to be downloaded {'status','season','episode','slot_id','expected'}. Season, episode and expected are 0 if no next episode
	:rtype: dict

'''
def next_aired(serie_id,s_season=0,s_episode=0):
	global t
	if 't' not in globals():
		t = myTvDB()
	else:
		logging.info('Connection saved')

	logging.debug('API initiator: %s', t)

	try:
		#for serie_id in series:
		if not isinstance(serie_id,int):
			serie_id = serie_id.find('id').text
		serie = t[int(serie_id)]
	except Exception,e:
		return {}

	# If season & episode specified
	if int(s_season)*int(s_episode)>0: 

		# Check if next episode exists in season
		if s_episode+1 in serie[s_season].keys():
			status = 10 if convert_date(serie[s_season][s_episode+1]['firstaired']) >= date.today() else 15
			return {
				'status':	status,
				'season':	s_season,
				'episode':	s_episode+1,
				'slot_id':	0,
				'expected':	serie[s_season][s_episode+1]['firstaired']
				}
		else:
			# Check if next season exists
			if s_season+1 in serie.keys() and not serie[s_season+1][1]['firstaired'] is None:
				status = 10 if convert_date(serie[s_season+1][1]['firstaired']) >= date.today() else 15
				return {
					'status':	status,
					'season':	s_season+1,
					'episode':	1,
					'slot_id':	0,
					'expected':	serie[s_season+1][1]['firstaired']
					}
			else:
				# TV show achieved
				return {
						'status':	90,
						'season':	0,
						'episode':	0,
						'slot_id':	0,
						'expected':	'2100-12-31'
					}
	# If no episode specified
	else:
		# Retrieve last aired episode
		if serie.nextAired() is not None:
			return {
					'status':	10,
					'season':	result['next']['seasonnumber'],
					'episode':	result['next']['episodenumber'],
					'slot_id':	0,
					'expected':	result['next']['firstaired']
					}
		return	{
					'status':	90,
					'season':	0,
					'episode':	0,
					'slot_id':	0,
					'expected':	'2100-12-31'
				}

def last_aired(serie_id,s_season=0,s_episode=0):
	global t
	if 't' not in globals():
		t = myTvDB()
	else:
		logging.info('Connection saved')

	logging.debug('API initiator: %s', t)

	try:
		#for serie_id in series:
		if not isinstance(serie_id,int):
			serie_id = serie_id.find('id').text
		serie = t[int(serie_id)]
	except Exception,e:
		return {}

	if int(s_season)*int(s_episode)>0:
		return	{
			'id':		int(serie_id),
			'seriesname':	serie.data['seriesname'],
			'next':	t[int(serie_id)][int(s_season)][int(s_episode)]
			}

	return	{
			'id':		int(serie_id),
			'seriesname':	serie.data['seriesname'],
			'last':	t[int(serie_id)].lastAired(),
			'next': t[int(serie_id)].nextAired()
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
		logging.debug('FTP connection: %s',conf['server'])
		ftp = FTP(conf['server'])
		ftp.login(conf['user'],conf['password']) 
		for fichier in fichiers.values():
			logging.debug('FTP transfer: %s',fichier['name'].encode('UTF-8'))
			pattern = '{0}/season {1}/{2}'
			chemin_cible = pattern.format(
					str(serie['name']),
					str(serie['season']),
					"/".join(fichier['name'].encode('UTF-8').split('/')[0:-1])
							)
			chemin = conf['folder'] + '/'
			for folder in chemin_cible.split('/'):
				if not os.path.isdir(chemin + folder):
					os.mkdir(chemin + folder)
				chemin += folder + '/'
			ftp_cmd = 'RETR ' + fichier['name'].encode('UTF-8')
			logging.debug(ftp_cmd)
			ftp.retrbinary(
				ftp_cmd, 
				open(conf['folder'] + '/' + chemin_cible + '/' + fichier['name'].encode('UTF-8').split('/')[-1], 'wb').write)
		ftp.quit()
		# File download is completed!
		return True
	except:
		#Error during transfer
		return False

def add_torrent(filepath, tc, slotNumber,delete_data):
	# fileuri = 'file.torrent'
	torrents = tc.get_torrents()
	torrents = filter(ignore_stopped,torrents)

	while len(torrents) >= int(slotNumber):
		# If there is not slot available, close the older one
		torrents = filter(keep_in_progress,torrents)
		torrent = sorted(torrents, key=lambda tor: tor.date_added)[0]
		tc.remove_torrent(torrent.id, delete_data= delete_data)
		logging.info("Maximum slot number reached, deletion of the oldest torrent : {0}".format(torrent.name))
		torrents = tc.stop_torrent(torrent.id)
		torrents = tc.get_torrents()
	
	new_torrent = tc.add_torrent(filepath)
	if (filepath[:7] == 'file://'):
		os.remove(filepath[7:])
	tc.start_torrent(new_torrent.id)
	return new_torrent

def keep_in_progress(tor):
	return tor.status == 'seeding'

def ignore_stopped(tor):
	return tor.status != 'stopped'


