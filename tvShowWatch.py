#!/usr/bin/env python
#encoding:utf-8

from __future__ import print_function
from select import select
from subprocess import Popen, PIPE

import sys
import os
import tvdb_api
#import time
from datetime import date
import string
import logging
import argparse
#import xml.etree.ElementTree as ET
import transmissionrpc
import smtplib
import unicodedata
from myDate import *
#from types import *
import Prompt
from TSWmachine import *
from ConfFile import ConfFile
from serieList import SerieList
from tracker import *
from ftplib import FTP
from email.mime.text import MIMEText

global t

CONFIG_FILE = sys.path[0] + '/config.xml' if sys.path[0] != '' else 'config.xml'
LIST_FILE = sys.path[0] + '/series.xml' if sys.path[0] != '' else 'series.xml'

def last_aired(serie_id):
	global t
	if 't' not in globals():
		t = tvdb_api.Tvdb()
	else:
		print("connection saved")
	logging.debug('API initiator: %s', t)
	result = []
	last_episode = {'seasonnumber': 0, 'episodenumber': 0, 'firstaired': datetime.date(1900,1,1) }
	next_episode = {'seasonnumber': 0, 'episodenumber': 0, 'firstaired': datetime.date(1900,1,1) }

	#for serie_id in series:
	if not isinstance(serie_id,int):
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

	return	{
			'seriename':	serie.data['seriesname'],
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

def transferFile(fichiers,serie,confTransmission):
	ftp = FTP(confTransmission['server'])
	ftp.login(confTransmission['user'],confTransmission['password']) 
	for fichier in fichiers.values():
		pattern = '{0}/season {1}/{2}'
		chemin_cible = pattern.format(
				str(serie['name']),
				str(serie['season']),
				"/".join(fichier['name'].split('/')[0:-1])
						)
		chemin = confTransmission['folder'] + '/'
		for folder in chemin_cible.split('/'):
			if not os.path.isdir(chemin + folder):
				os.mkdir(chemin + folder)
			chemin += folder + '/'
		ftp.retrbinary(
			'RETR ' + str(fichier['name']), 
			open(confTransmission['folder'] + '/' + chemin_cible + '/' + str(fichier['name'].split('/')[-1]), 'wb').write)
	ftp.quit()
	print(' => File download is completed!')

def add_torrent(result, tracker,confTransmission):
	result = tracker.select_torrent(result)
	logging.debug("selected torrent:")
	logging.debug(result)
	print(" => Download torrent!")
	tracker.download(result['id'])
	tc = transmissionrpc.Client(
			confTransmission['server'],
			confTransmission['port'],
			confTransmission['user'],
			confTransmission['password']
	)

	torrents = tc.get_torrents()
	torrents = filter(ignore_stopped,torrents)

	while len(torrents) >= int(confTransmission['slotNumber']):
		# If there is not slot available, close the older one
		torrents = filter(keep_in_progress,torrents)
		torrent = sorted(torrents, key=lambda tor: tor.id, reverse=True)[0]
		tc.remove_torrent(torrent.id, delete_data=True)
		print("Maximum slot number reached, deletion of the oldest torrent : {0}".format(torrent.name))
		torrents = tc.stop_torrent(torrent.id)
		torrents = tc.get_torrents()
	
	new_torrent = tc.add_torrent('file://file.torrent')
	os.remove('file.torrent')
	tc.start_torrent(new_torrent.id)
	return new_torrent

def input_serie():
	global t
	if 't' not in globals():
		t = tvdb_api.Tvdb()
	else:#ICI
		logging.debug('connection saved')
	logging.debug('API initiator: %s', t)
	result = []
	while len(result) < 1:
		serie = Prompt.promptSimple("Please type your TV Show ")
		serie = str(''.join(c for c in unicodedata.normalize('NFKD', unicode(serie, 'utf-8')) if unicodedata.category(c) != 'Mn'))
		result = t.search(serie)

		if len(result) == 0:
			print("Unknowned TV Show")
		elif len(result) > 1:
			choices = []
			for val in result:
				if not 'firstaired' in val.keys():
					val['firstaired'] = '????'
				choices.append([val['id'],val['seriesname']+' (' + val['firstaired'][0:4] + ')'])
			result = Prompt.promptChoice("Did you mean...",choices)
			result = t[result]

		elif len(result) == 1:
			result = t[result[0]['id']]
	return result

def input_emails():
	emails = []
	email = 'start'
	while email != '':
		email = Prompt.promptSimple("Enter an email [keep blank to finish]")
		if email != '' and not re.match(r'[^@]+@[^@]+\.[^@]+',email):
			print('Incorrect format')
		elif re.match(r'[^@]+@[^@]+\.[^@]+',email):
			emails.append(email)
	return emails

def last_or_next(serie):
	if (serie['last']['season'] == 0):
		if Prompt.promptYN("Last season not yet started. Do you want to schedule the Season pilot on " + print_date(serie['next']['aired']),'y'):
			return serie['next']
		else:
			sys.exit()
	elif (serie['next']['season'] == 0):
		if Prompt.promptYN("Last season achieved. Do you want to download the Season final on " + print_date(serie['last']['aired']),'n'):
			return serie['last']
		else:
			sys.exit()	
	else:	
		print("Next episode download scheduled on " + print_date(serie['next']['aired']))
		str_last = 'Do you want also download the last aired : S{0:02}E{1:02} - {2} ?'
		if Prompt.promptYN(str_last.format(serie['last']['season'],serie['last']['episode'],print_date(serie['last']['aired'])),'N'):
			return serie['last']
		else:
			return serie['next']

def keep_in_progress(tor):
	return tor.status == 'seeding'

def ignore_stopped(tor):
	return tor.status != 'stopped'

def action_run(m):
	processes = [Popen(['./TSW_api.py','--action','run'],stdout=PIPE,bufsize=1, close_fds=True, universal_newlines=True)]
	
	while processes:
	        for p in processes[:]:
	                if p.poll() is not None:
	                        print(p.stdout.read(), end='')
	                        p.stdout.close()
	                        processes.remove(p)
	        rlist = select([p.stdout for p in processes],[],[],0.1)[0]
	        for f in rlist:
        	        print(f.readline(),end='')
	sys.exit()

def action_list(m):
	logging.debug('Call function action_list()')
	result = m.getSeries()
	logging.debug('result => '+str(result))
	if result['rtn']!='200' and result['rtn']!='300':
		print('Error during TV Shows reading: '+result['error'])
		sys.exit()
	if result['rtn'] == '300':
		print("No TV Show scheduled")
		sys.exit()
	pattern = '{0}:{1} - S{2:02}E{3:02} - expected on {4} (status: {5})'
	for serie in result['result']:
		print(pattern.format(serie['id'],serie['name'],serie['season'],serie['episode'],serie['expected'],serie['status']))
	sys.exit()

def action_add(m):

	result = input_serie()
	serie = last_aired(int(result.data['id']))
	next = last_or_next(serie)
	if m.testConf(False)['rtn']=='200' and Prompt.promptYN('Voulez-vous rajouter des emails de notification ?'):
		emails = input_emails()
	else:
		emails = []

	result = m.addSerie(result.data['id'],emails,next['season'],next['episode'])

	if result['rtn']!='200':
		print('Error during TV Show add: '+result['error'])
		sys.exit()
	print(result.data['seriesname'] + u" added")
	sys.exit()

def action_reset(m):
    '''Reset the configuration and/or the series list'''
    logging.debug('Call function action_reset()')
    result = {'rtn': '999'}
    while result['rtn'] != '200' and result['rtn'] != '302':
        conf = [
		'tracker_id', 
		'tracker_user',
		'tracker_password',
		'transmission_server',
		'transmission_port',
		'transmission_user',
		'transmission_password',
		'transmission_slotNumber',
		'transmission_folder'
		]
        for param in conf:
            result = m.setConf({param:'None'},False)
        if result['rtn'] == '200':
            result = m.testConf(False)
        if result['rtn'] != '200' and result['rtn'] != '302':
            print('Error during configuration: '+result['error'])

    if (Prompt.promptYN("Do you want to activate Email notification?",'N')):
        while result['rtn'] != '200':
            conf = [
		'smtp_server',
		'smtp_port',
		'smtp_ssltls',
		'smtp_user',
		'smtp_password',
		'smtp_emailSender',
		]
            for param in conf:
                result = m.setConf({param:'None'},False)
            if result['rtn'] == '200':
                result = m.testConf(True)
            if result['rtn'] != '200':
                print('Error during SMTP configuration: '+result['error'])

    result = m.setConf({},True)
    print('Configuration completed')

def action_del(m):
	'''Delete TV show from configuration file'''
	logging.debug('Call function action_del()')
	series = m.getSeries()
	if series['rtn'] == '300':
		print("No TV Show scheduled")
		sys.exit()
	if series['rtn'] != '200':
		print('Error during TV Show listing'+series['error'])
		sys.exit()
	choix = []
	if len(series['result'])>0:	
		for serie in series['result']:
			choix.append([serie['id'],serie['name']])
	else:
		print("No TV Show scheduled")
		sys.exit()
	s_id = Prompt.promptChoice("Which TV Show do you want to unschedule?",choix)
	result = m.delSerie(s_id)
	if result['rtn'] != '200':
		print('Error during Tv Show deletion'+result['error'])
	else:
		print('TV Show ' + str(s_id) + ' unscheduled')

def action_config(m):
    '''Change configuration'''
    logging.debug('Call function action_config()')
    conf = m.getConf()
    if (conf['rtn']!='200'):
        print("Error during configuration reading")
	sys.exit()
    conf = conf['result']
    if (conf['keywords'] is not None):
        keywords_default = ' / '.join(conf['keywords'])
    else:
        keywords_default = ''
    email_activated = 'Enabled' if len(conf['smtp'])>0 else 'Disabled'
    if ('folder' in conf['transmission'].keys()):
        folder = conf['transmission']['folder']
    else:
        folder = 'No transfer'
    configData = Prompt.promptChoice(
            "Selection value you want modify:",
            [
                ['tracker_id','Tracker : '+conf['tracker']['id']],
                ['tracker_user','Tracker Username : '+conf['tracker']['user']],
                ['tracker_password','Tracker Password : ******'],
                ['keywords','Torrent search keywords : '+keywords_default],
                ['transmission_server','Transmission Server : ' + str(conf['transmission']['server'])],
                ['transmission_port','Transmission Port : ' + str(conf['transmission']['port'])],
                ['transmission_user','Transmission User : ' + str(conf['transmission']['user'])],
                ['transmission_password','Transmission Password : ******'],
                ['transmission_slotNumber','Transmission maximum slots : ' + str(conf['transmission']['slotNumber'])],
                ['transmission_folder','Local folder : ' + str(conf['transmission']['folder'])],
                ['smtp','Email Notification: ' + email_activated]
            ])
    if configData == 'smtp':
        configData = Prompt.promptChoice(
            "Selection value you want modify:",
            [
                ['smtp_server','SMTP Server : ' + str(conf['smtp']['server'])],
                ['smtp_port','SMTP Port : ' + str(conf['smtp']['port'])],
                ['smtp_ssltls','Secure connection : ' + str(conf['smtp']['ssltls'])],
                ['smtp_user','SMTP User : ' + str(conf['smtp']['user'])],
                ['smtp_password','SMTP Password : ******'],
                ['smtp_emailSender','Sender Email : ' + str(conf['smtp']['emailSender'])]
            ])
        result = m.setConf({configData:'None'})
    else:
        result = m.setConf({configData:'None'})
    if result['rtn'] == '200':
        print('Configuration change completed !')
    else:
        print('Error during configuration change: '+result['error'])

def action_getconf(m):
    '''Return configuration'''
    logging.debug('Call function action_getconf()')
    conf = m.getConf()
    if (conf['rtn']!='200'):
        print("Error during configuration reading")
	sys.exit()
    conf = conf['result']
    result = "'tracker_id':"+conf['tracker']['id']
    result += "\n'tracker_user':"+conf['tracker']['user']
    result += "\n'transmission_server':" + str(conf['transmission']['server'])
    result += "\n'transmission_port':" + str(conf['transmission']['port'])
    result += "\n'transmission_user':" + str(conf['transmission']['user'])
    result += "\n'transmission_slotNumber':" + str(conf['transmission']['slotNumber'])
    if 'folder' in conf['transmission'].keys():
        result += "\n'transmission_folder':" + str(conf['transmission']['folder'])
    if len(conf['smtp'])>0:
        result += "\n'smtp_server':" + str(conf['smtp']['server'])
        result += "\n'smtp_port':" + str(conf['smtp']['port'])
        result += "\n'smtp_ssltls':" + str(conf['smtp']['ssltls'])
        result += "\n'smtp_user':" + str(conf['smtp']['user'])
        result += "\n'smtp_emailSender':" + str(conf['smtp']['emailSender'])
    for keyword in conf['keywords']:
        result += "\n'keywords':" + keyword
    print(result)

def main():

    # Get input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-a",
            "--action",
            default='run',
            choices=['run', 'list', 'init', 'add','config','getconf','del'],
            help='action triggered by the script'
        )
    parser.add_argument(
            "-c",
            "--config",
            default=CONFIG_FILE,
            help='indicates the configuration file location. By default:'+CONFIG_FILE
        )
    parser.add_argument(
            "-s",
            "--seriefile",
            default=LIST_FILE,
            help='indicates the series list file location. By default:'+LIST_FILE
        )
    parser.add_argument(
            "-v",
            "--verbosity",
            action="store_true",
            help='maximum output verbosity'
        )
    parser.add_argument(
            "--arg",
            default='',
            help='arguments for bash execution'
        )
    args = parser.parse_args()

    # Manage verbosity level
    if args.verbosity:
        logging.basicConfig(level=logging.DEBUG)
    logging.info('SERIES started in verbosity mode')

    global arg;
    if args.arg != '':
        Prompt.arg = args.arg.split(',')

    # Initialize more data
    m = TSWmachine(True,args.verbosity)
    if args.action != 'init':
	logging.debug('Loading of conffile: %s', args.config)
	logging.debug('Loading of seriefile: %s', args.seriefile)
	result = m.openFiles(args.config, args.seriefile)
	if result['rtn']!='200':
		print("Please first use tvShowWatch --action init")
		sys.exit()
    else:
        result = m.createConf(args.config)
        if result['rtn']!='200':
            print('Error during creation of the configuration file: '+result['error'])
            sys.exit()

    action_fct = {
            'list':action_list,
            'run':action_run,
            'add':action_add,
            'init':action_reset,
            'config':action_config,
            'del':action_del,
            'getconf':action_getconf
        }

    # Call for action
    logging.debug('Action from the parameter: %s', args.action)
    
    fct = action_fct[args.action]
    logging.debug('Action function: %s', fct)
    fct(m)

if __name__ == '__main__':
    main()

