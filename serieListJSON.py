#!/usr/bin/env python
#encoding:utf-8

import MyFileJSON
from myDate import *
from myTvDB import *
import myConstants
import messages

LIST_VERSION = "2.0"

class SerieList(MyFileJSON.MyFile):
	def __init__(self):
		MyFileJSON.MyFile.__init__(self, 'series', 'Serie list')

	def openFile(self,filename = myConstants.SERIES_FILE,createIfNotExist=True):
		return MyFileJSON.MyFile.openFile(self,filename,createIfNotExist)
		
	def _create(self):
		result = MyFileJSON.MyFile._create(self)
		self.tree['version'] = LIST_VERSION
		self._save
		return result

	def _version(self):
		return LIST_VERSION

	"""
		The ``addSerie`` method
		=============================
		
		Use it in order to add an additional TV show in configuration file

		:param s_id: TvDB ID of the TV show
		:type question: Integer

		:param s_season: TV Show season number
		:type question: Integer

		:param s_episode: TV Show episode number of the season
		:type question: Integer

		:return: True when append of the TV Show completed
		:rtype: boolean

		:Example:

		>>> f.addSerie(2546,{'season':5,'episode':8,date(2013,10,3),['niouf@niouf.fr','niorf@niorf.fi'])
		True
		
	"""
	def addSerie(self, s_id, seriesname, s_episode, emails, keywords = []):
		if self.testSerieExists(s_id):
			print('TV Show already scheduled')
			return False
		series = self.tree['series']
		serie = {
					'id':		int(s_id),
					'name':		str(seriesname),
					'pattern':	str(seriesname),
					'slot_id':	int(0),
					'emails':	[],
					'keywords':	[]
				}
		if s_episode is not None:
			serie.update({
							'season': 	int(s_episode['season']),
							'episode': 	int(s_episode['episode']),
							'status': 	10,
							'expected': s_episode['aired'].strftime("%Y-%m-%d")
						})
		else:
			serie.update({
							'season': 	0,
							'episode': 	0,
							'status': 	90,
							'expected': "9999-12-31"
						})

		for email in emails:
			serie['email'].append(str(email))

		for keyword in keywords:
			serie['keywords'].append(str(keyword))

		series.append(serie)
		self._save()
		return True

	def delSerie(self, s_id):
		series = self.tree['series']
		result = [serie for serie in series if serie['id'] != s_id]
		if len(result)>0:
			self.tree['series'] = result
			self._save()
			return True
		return False

	"""
		The ``testSerieExists`` method
		==============================
		
		Use it in order to know if a TV show already is in configuration file

		:param s_id: TvDB ID of the TV show
		:type s_id: Integer

		:return: True if TV Show is in the configuration file
		:rtype: boolean

		:Example:
t
		>>> f.testSerieExists(5262)
		False
		
	"""
	def testSerieExists(self, s_id):
		return len([serie for serie in self.tree['series'] if serie['id'] == s_id])>0

	"""
		The ``getSerie`` method
		==============================
		
		Return the TV Show data from configuration file

		:param s_id: TvDB ID of the TV show
		:type s_id: Integer

		:param json_c: True if dates must be format as text (for json serialization purpose). False (by default) for datetime format.
		:type json_c: Boolean

		:param retr_tvdb_data: True if theTvDB data must be retrieved (requires connection delay). False (by default) to prevent connection.
		:type retr_tvdb_data: Boolean

		:return: dict of TV show
		:rtype: dict

		:Example:
t
		>>> f.getSerie(5262)
		{'id':5262,'name':'Foo','pattern':'foo','season':1,'episode':1,status:10,'slot_id':10,'expected':'12-05-2042','emails':[],'keywords':'720p','tvdb':{},'lastEpisode':{},'nextEpisode':{}}
		
	"""
	def getSerie(self, s_id,json_c=False,retr_tvdb_data=False):
		if retr_tvdb_data:
			t = myTvDB()
		if self.testSerieExists(s_id):
			serie = [serie for serie in self.tree['series'] if serie['id'] == s_id][0]
			if retr_tvdb_data:
				tvdb_data = t[int(serie['id'])]
				serie.update({
						'tvdb':		tvdb_data.data if retr_tvdb_data else {},
						'lastEpisode': tvdb_data.lastAired() if retr_tvdb_data else {},
						'nextEpisode': tvdb_data.nextAired() if retr_tvdb_data else {}
						})
			return serie
		else:
			return False

	"""
		The ``listSeries`` method
		=========================
		
		Return the list of TV Shows in configuration file

		:return: list of dict of TV shows
		:rtype: list
		
	"""
	def listSeries(self,json_c=False,retr_tvdb_data=False):
		series = []
		for serie in self.tree['series']:
			series.append(self.getSerie(serie['id'],json_c,retr_tvdb_data))
		return series

	def updateSerie(self,s_id,values):
		if self.testSerieExists(s_id):
			serie = [serie for serie in self.tree['series'] if serie['id'] == s_id][0]
			for val in values.keys():
				serie[val] = values[val]
			#	serie[val] = int(values[val]) if values[val].isdigit() else str(values[val])
			self._save()
			return self.getSerie(s_id)
		return False

	def changeEmails(self,s_id,emails=[]):
		return self.changeList('email',s_id,emails)

	def changeKeywords(self,s_id,keywords=[]):
		return self.changeList('keyword',s_id,keywords)

	def changeList(self,listtype,s_id,values=[]):
		listtype += 's'
		if self.testSerieExists(s_id):
			serie = [serie for serie in self.tree['series'] if serie['id'] == s_id][0]
			serie[listtype] = values
			self._save()
			return True
		return False
		
if __name__ == '__main__':
	s = SerieList()
	print "OpenFile",
	print s.openFile()['rtn'] == '200'
	print "test serie exists",
	print s.testSerieExists(121361)
	print "listSeries",
	serielist = s.listSeries()
	print len(serielist)>0
	
