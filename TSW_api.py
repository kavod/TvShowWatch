#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import logging
import argparse
import json
from TSWmachine import *

CONFIG_FILE = sys.path[0] + '/config.xml' if sys.path[0] != '' else 'config.xml'
LIST_FILE = sys.path[0] + '/series.xml' if sys.path[0] != '' else 'series.xml'

def main():
	# Get input parameters
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-a",
		"--action",
		default='',
		choices=['run', 'list', 'init', 'add','config','getconf','del','update','getEpisode','resetKeywords','resetAllKeywords'],
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
		"--admin",
		action="store_true",
		help='admin mode'
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
	logging.info('TSW started in verbosity mode')
	
	# Parse arguments
	if args.arg != '':
		try:
			arg = json.loads(args.arg)
		except:
			print(json.dumps({'rtn':'415','error':messages.returnCode['415']}))
			sys.exit()
	else:
		arg = {}

	# Initialize more data
	m = TSWmachine(args.admin,args.verbosity)
	if args.admin:
		logging.info('TSW loaded in admin mode')

	if args.action != 'init':
		logging.debug('Loading of conffile: %s', args.config)
		logging.debug('Loading of seriefile: %s', args.seriefile)
		result = m.openFiles(args.config, args.seriefile)
		if result['rtn']!='200':
			print(json.dumps(result))
			sys.exit()

	if args.action == 'init':
		result = m.createConf(args.config,arg['conf'])
		print(json.dumps(result))
		sys.exit()

	if args.action == 'run':
		m.run()
		sys.exit()

	if args.action == 'list':
		if 'ids' not in arg.keys():
			arg['ids'] = 'all'
		if 'load_tvdb' not in arg.keys():
			arg['load_tvdb'] = False
		print(json.dumps(m.getSeries(arg['ids'],json_c=True,load_tvdb=arg['load_tvdb'])))
		sys.exit()

	if args.action == 'add':
		if 'emails' not in arg.keys():
			arg['emails'] = []
		print(json.dumps(m.addSeries(arg['id'],arg['emails'])))
		sys.exit()

	if args.action == 'update':
		if 'param' not in arg.keys():
			arg['param'] = {}
		print(json.dumps(m.setSerie(arg['id'],arg['param'],json_c=True)))
		sys.exit()

	if args.action == 'resetKeywords':
		print(json.dumps(m.resetKeywords(arg['id'])))
		sys.exit()

	if args.action == 'resetAllKeywords':
		print(json.dumps(m.resetAllKeywords()))
		sys.exit()

	if args.action == 'config':
		result = m.setConf(arg['conf'])
		if (result['rtn'] != '200'):
			print(json.dumps(result))
		else:
			print(json.dumps(m.getConf()))
		sys.exit()

	if args.action == 'getconf':
                if 'arg' not in locals():                                                
                        arg = {}
                if 'conf' not in arg.keys():
                        arg['conf'] = 'all'
		print(json.dumps(m.getConf(arg['conf'])))
		sys.exit()

	if args.action == 'del':
		print(json.dumps(m.delSerie(arg['id'])))
		sys.exit()

	if args.action == 'getEpisode':
		print(json.dumps(m.getEpisode(arg['id'],arg['season'],arg['episode'])))
		sys.exit()

	print(json.dumps({'rtn':'400','error':messages.returnCode['400'].format(args.action)}))
	sys.exit()

if __name__ == '__main__':
    main()
