#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import logging
import transmissionrpc
import smtplib
from email.mime.text import MIMEText
from datetime import date
from tracker import *
from myDate import *
from myTvDB import *
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

def add_torrent(filepath, tc, slotNumber):
	# fileuri = 'file.torrent'
	torrents = tc.get_torrents()
	torrents = filter(ignore_stopped,torrents)

	while len(torrents) >= int(slotNumber):
		# If there is not slot available, close the older one
		torrents = filter(keep_in_progress,torrents)
		torrent = sorted(torrents, key=lambda tor: tor.date_added)[0]
		tc.remove_torrent(torrent.id, delete_data=True)
		logging.info("Maximum slot number reached, deletion of the oldest torrent : {0}".format(torrent.name))
		torrents = tc.stop_torrent(torrent.id)
		torrents = tc.get_torrents()
	
	new_torrent = tc.add_torrent('file://'+filepath)
	os.remove(filepath)
	tc.start_torrent(new_torrent.id)
	return new_torrent

def keep_in_progress(tor):
	return tor.status == 'seeding'

def ignore_stopped(tor):
	return tor.status != 'stopped'


