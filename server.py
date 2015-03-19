#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import imp
import json
import subprocess
import cherrypy
from TSWmachine import *
from functions import *
import time
import myConstants

from cherrypy.process.plugins import Daemonizer
from cherrypy.process.plugins import PIDFile
d = Daemonizer(cherrypy.engine)
d.subscribe()
PIDFile(cherrypy.engine, myConstants.PID_FILE).subscribe()

class TvShowWatch():
	def __init__(self,conffile = myConstants.CONFIG_FILE, serielist = myConstants.SERIES_FILE, debug = False):
		self.debug = debug != False
		self.auth = False
		if not os.path.isfile(conffile):
			raise Exception("Configuration file " + conffile + " does not exist",401)
		self.conffile = conffile
		self.serielist = serielist
		self.m = TSWmachine(True,False)
		result = self.m.openFiles(conffile, serielist)
		if result['rtn'] != '200':
			return result

	def setAuth(self,auth=True):
		if self.auth != auth:
			self.auth = auth

	def isAuth(self):
		return self.auth

	def __exec_cmd(self,cmd,method="unknown",json_rtn=True):
		try:
			result = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as e:
			raise e
		except:
			if self.debug:
				print cmd
			raise Exception(method)
		if self.debug:
			print cmd
			print result
		if json_rtn:
			return json.loads(result)
		else:
			return result
		
	def getConf(self):
		return self.m.getConf()

	def setConf(self,conf):
		return self.m.setConf(conf)

	def createConf(self,conf):
		return self.m.createConf(conf)

	def getSeries(self,load_tvdb=False):
		return self.m.getSeries('all',json_c=True,load_tvdb=load_tvdb)

	def getSerie(self,id):
		return self.m.getSeries(int(id),json_c=True,load_tvdb=False)

	def getEpisode(self,serie_id,season,episode,lang='en'):
		return self.m.getEpisode(int(serie_id),int(season),int(episode))
		
	def setSerie(self,id,param):
		arg = {"status": 15}
		for (key,value) in param.items():
			if key == "emails" and len(value) > 0:
				arg['emails'] = value
			elif key == "emails" and len(value) < 1:
				arg['emails'] = []
			elif key == "keywords" and len(value) > 0:
				arg['keywords'] = value
			elif key == "keywords" and len(value) < 1:
				arg['keywords'] = []
			else:
				arg[str(key)] = str(value)
		return self.m.setSerie(int(id),arg,json_c=True)
	
	def addemail(self,id,email):
		serie = self.getSerie(id)
		emails = serie['result']['emails']
		if email not in emails:
			emails.append(email)
		return self.setSerie(id,{"emails":emails})

	def delemail(self,id,email):
		serie = self.getSerie(id)
		emails = serie['result']['emails']
		if email in emails:
			emails.remove(email)
		return self.setSerie(id,{"emails":emails})

	def delSerie(self,id):
		return self.m.delSerie(int(id))

	def addSerie(self,id):
		return self.m.addSeries(int(id),[])

	def resetSerieKeywords(self,id):
		return self.m.resetKeywords(int(id))

	def resetAllKeywords(self):
		return self.m.resetAllKeywords()

	def search(self,pattern):
		if pattern is None or len(pattern) < 1:
			return {'rtn':415,'error':'Blank search'}
		return self.m.search(pattern)

	def testRunning(self):
		cmd = [myConstants.START_STOP_FILE,'status']
		try:
			return self.__exec_cmd(cmd,"testRunning",json_rtn=False).replace('tvShowWatch is ','')
		except subprocess.CalledProcessError as e:
			return "Not running..."

	def push(self,serie_id,destination):
		return self.m.pushTorrent(int(serie_id),destination)

	def run(self):
		cmd = ["date"]
		print self.__exec_cmd(cmd,"date",json_rtn=False)
		self.m.run()

	def logs(self):
		return self.m.logs(json_c=True)

class Root(object):
	pass
	
class Requete(object):
	def POST(self,**param):
		self.POST(self,**param)
	
class get_conf(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {'rtn':e.args[0],'error':e.args[1]}
			sys.exit()
		TSW.setAuth()
		return TSW.getConf()
		sys.exit()
		
class run(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.run()

class save_conf(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		result = {
			"tracker": tracker_api_conf(form),
			"transmission":transmission_api_conf(form),
			"smtp": email_api_conf(form)
			}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		if os.path.isfile(myConstants.CONFIG_FILE):
			conf = TSW.setConf(result)
			if conf['rtn']=='200' or conf['rtn']=='302':
				msg = "Configuration file saved"
			else:
				msg = "Error during configuration save: " + conf['error']
		else:
			conf = TSW.createConf(result)
			if conf['rtn']=='200':
				msg = 'Configuration file created'
			else:
				msg = 'Error during configuration creation: ' + conf['error']
		
		return {"rtn":conf['rtn'],"error":msg}
		
class save_keywords(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'keywords[]' in params.keys():
			keywords = params['keywords[]']
		else:
			keywords = []
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		if 'serie_id' in params.keys() and int(params['serie_id'])>0:
			res = TSW.setSerie(int(params['serie_id']),{"keywords":keywords})
			if res['rtn']!='200':
				return {"rtn":res['rtn'],"error":res['error']}
			return {"rtn":200,"error":"Keywords updated"}
		else:
			res = TSW.setConf({"keywords":keywords})
			if res['rtn']!='200':
				return {"rtn":res['rtn'],"error":res['error']}
			return {"rtn":200,"error":"Keywords updated"}

class getSeries(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		load_tvdb = ('load_tvdb' in params and params['load_tvdb']=='1')
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.getSeries(load_tvdb)

class streamGetSeries(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	def GET(self, _=None):
		cherrypy.response.headers["Content-Type"] = "text/event-stream"
		cherrypy.response.headers['Cache-Control'] = 'no-cache'
		cherrypy.response.headers['Connection'] = 'keep-alive'
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,False)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		if _:
			data = "retry: 5000\r\nEvent: server-time\r\ndata: 3" + time.ctime(os.path.getmtime(myConstants.SERIES_FILE)) + "\n\n"
			return data
		else:
			def content():
				yield "retry: 5000\r\n"
				while True:
					data = "Event: server-time\r\ndata: 4" + time.ctime(os.path.getmtime(myConstants.SERIES_FILE)) + "\n\n"
					yield data
					time.sleep(5)
					
			return content()
	GET._cp_config = {'response.stream': True, 'tools.encode.encoding':'utf-8'}   

class getSerie(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'id' in params.keys():
			serie_id = int(params['id'])
		else:
			return {'rtn':'415','error':messages.returnCode['415']}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.getSerie(serie_id)
		
class delSerie(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn':'415','error':messages.returnCode['415']}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.delSerie(serie_id)
		
class addSerie(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn':'415','error':messages.returnCode['415']}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.addSerie(serie_id)
		
class getEpisode(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn':'415','error':messages.returnCode['415']}
		if 'season' in params.keys():
			season = int(params['season'])
		else:
			return {'rtn':'415','error':messages.returnCode['415']}
		if 'episode' in params.keys():
			episode = int(params['episode'])
		else:
			return {'rtn':'415','error':messages.returnCode['415']}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.getEpisode(serie_id,season,episode)

class setSerie(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn' : 499, 'error' : 'TV Show not found'}
		if 'season' in params.keys():
			season = int(params['season'])
		else:
			return {'rtn' : 499, 'error' : 'You must indicate both of Season and Episode numbers'}
		if 'episode' in params.keys():
			episode = int(params['episode'])
		else:
			return {'rtn' : 499, 'error' : 'You must indicate both of Season and Episode numbers'}
		pattern = params['pattern'] if 'pattern' in params.keys() else ''
		if season * episode != 0:
			try:
				TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
			except Exception as e:
				return {"rtn":e.args[0],"error":e.args[1]}
			TSW.setAuth()
			try:
				val_episode = TSW.getEpisode(serie_id, season, episode, 'en')
			except Exception as e:
				return {'rtn' : 419, 'error' : 'Episode S' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ' does not exist'}
		else:
			return {'rtn' : 499, 'error' : 'You must indicate both of Season and Episode numbers'}

		update = TSW.setSerie(serie_id,{'season':season,'episode':episode,'pattern':pattern,'expected':val_episode['result']['firstaired'],'status':15})
		if update['rtn'] != '200':
			return {'rtn' : update['rtn'], 'error' : 'Error during TV Show update<br />'+update['error']}
		else:
			return {'rtn' : 200, 'error' : 'TV Show updated'}
			
class addemail(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn' : 499, 'error' : 'TV Show not found'}
		if 'email' in params.keys():
			email = params['email']
		else:
			return {'rtn' : 499, 'error' : 'Email blank'}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		update = TSW.addemail(serie_id,email)
		if update['rtn'] != '200':
			return update
		else:
			return {'rtn':200,'error':'Tv Show updated'}
			
class delemail(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn' : 499, 'error' : 'TV Show not found'}
		if 'email' in params.keys():
			email = params['email']
		else:
			return {'rtn' : 499, 'error' : 'Email blank'}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		update = TSW.delemail(serie_id,email)
		if update['rtn'] != '200':
			return update
		else:
			return {'rtn':200,'error':'Tv Show updated'}

class reset_serie_keywords(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn' : 499, 'error' : 'TV Show not found'}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		update = TSW.resetSerieKeywords(serie_id)
		if update['rtn'] != '200':
			return update
		else:
			return {'rtn':200,'error':'Keywords updated'}	

class reset_all_keywords(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		update = TSW.resetAllKeywords()
		if update['rtn'] != '200':
			return update
		else:
			return {'rtn':200,'error':'Keywords updated for all TV Shows'}

class search(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'pattern' in params:
			pattern = params['pattern']
		else:
			return {'rtn':'415','error':messages.returnCode['415']}
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.search(pattern)
		
class pushTorrent(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		if 'serie_id' in params.keys():
			serie_id = int(params['serie_id'])
		else:
			return {'rtn' : 499, 'error' : 'TV Show not found'}
		if params['torrent'].file:
			fn = os.path.basename(form['torrent'].file.name)
			destination = myConstants.TMP_PATH + '/' + fn
			open(destination, 'wb').write(params['torrent'].file.read())
			try:
				TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
			except Exception as e:
				return {"rtn":e.args[0],"error":e.args[1]}
			TSW.setAuth()
			return TSW.push(serie_id,destination)
		else:
			return {"rtn":499,"error":'Enable to upload file'}

class logs(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.logs()

class get_arch(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, **params):
		debug = ('debug' in params.keys())
		return myConstants.ARCH

class testRunning(Requete):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	def GET(self, **params):
		debug = ('debug' in params.keys())
		try:
			TSW = TvShowWatch(myConstants.CONFIG_FILE,myConstants.SERIES_FILE,debug)
		except Exception as e:
			return {"rtn":e.args[0],"error":e.args[1]}
		TSW.setAuth()
		return TSW.testRunning()

class Api(object):
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	def GET(self, **params):
		if 'action' in params.keys():
			m = globals()[params['action']]()
			if params['action'] == 'streamGetSeries':
				cherrypy.response.headers["Content-Type"] = "text/event-stream"
				cherrypy.response.headers['Cache-Control'] = 'no-cache'
				cherrypy.response.headers['Connection'] = 'keep-alive'
				return m.GET()
			if params['action'] not in ['testRunning','get_arch','run','streamGetSeries']:
				#cherrypy.response.headers['Content-Type'] = "application/json"
				return json.dumps(m.GET(**params))
			return m.GET(**params)
			
	@cherrypy.tools.accept(media='text/plain')
	def POST(self, **params):
		return self.GET(**params)

if __name__ == '__main__':
	root = Root()
	root.api = Root()
	root.api.tvshowwatch = Api()
	root.api.get_conf = get_conf()
	root.api.run = run()
	root.api.save_conf = save_conf()
	root.api.save_keywords = save_keywords()
	root.api.getSeries = getSeries()
	root.api.streamGetSeries = streamGetSeries()
	root.api.getSerie = getSerie()
	root.api.delSerie = delSerie()
	root.api.addSerie = addSerie()
	root.api.getEpisode = getEpisode()
	root.api.setSerie = setSerie()
	root.api.addemail = addemail()
	root.api.delemail = delemail()
	root.api.reset_serie_keywords = reset_serie_keywords()
	root.api.reset_all_keywords = reset_all_keywords()
	root.api.search = search()
	root.api.pushTorrent = pushTorrent()
	root.api.logs = logs()
	root.api.get_arch = get_arch()
	root.api.testRunning = testRunning()
	
	conf = {
		  'global' : {
						'server.socket_host' : '0.0.0.0',
						'server.socket_port' : 1204,
						'server.thread_pool' : 8
					},
			'/': {
				        'tools.staticdir.on': True,
                		'tools.staticdir.root':myConstants.TSW_PATH,
				        'tools.staticdir.dir': './application',
				        'tools.staticdir.index': 'index.html',
		            },
			'/api': {
				        'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
				        'tools.sessions.on': True,
                		'tools.staticdir.root':myConstants.TSW_PATH,
				        'tools.response_headers.on': True,
				        'tools.response_headers.headers': [
				            ('Content-Type', 'text/plain')],
		            },
		}
	
	cherrypy.quickstart(root, '/', conf)

