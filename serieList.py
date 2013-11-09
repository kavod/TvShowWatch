#!/usr/bin/env python
#encoding:utf-8

from MyFile import *
from myDate import *

LIST_FILE = sys.path[0] + '/series.xml' if sys.path[0] != '' else 'series.xml'
LIST_VERSION = "1.1"

class SerieList(MyFile):
	def __init__(self, filename = LIST_FILE):
		MyFile.__init__(self, filename, 'series', 'Serie list')

	def _version(self):
		return LIST_VERSION

	def _create(self):
		self._create_root()
		self._save()
		return True

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
	def addSerie(self, s_id, seriesname, s_episode, emails):

		if self.testSerieExists(s_id):
			print('TV Show already scheduled')
			return False
 
		series = self.tree.getroot()		
		serie = ET.SubElement(series, "serie")
		serie_id = ET.SubElement(serie, "id")
		serie_id.text = str(s_id)
		name = ET.SubElement(serie, "name")
		name.text = str(seriesname)
		serie_s = ET.SubElement(serie, "season")
		serie_s.text = str(s_episode['season'])
		serie_e = ET.SubElement(serie, "episode")
		serie_e.text = str(s_episode['episode'])
		status = ET.SubElement(serie, "status")
		status.text = str(10)
		slot_id = ET.SubElement(serie, "slot_id")
		slot_id.text = str(0)
		expected = ET.SubElement(serie, "expected")
		expected.text = s_episode['aired'].strftime("%Y-%m-%d")

		for email in emails:
			node = ET.SubElement(serie, "email")
			node.text = email

		self._save()
		return True

	def delSerie(self, s_id):
		result = False
		series = self.tree.getroot()
		for serie in series.findall('serie'):
			if serie.find('id').text == str(s_id):
				series.remove(serie)
				result = True
		self._save()
		return result

	"""
		The ``testSerieExists`` method
		==============================
		
		Use it in order to know if a TV show already is in configuration file

		:param s_id: TvDB ID of the TV show
		:type question: Integer

		:return: True if TV Show is in the configuration file
		:rtype: boolean

		:Example:

		>>> f.testSerieExists(5262)
		False
		
	"""
	def testSerieExists(self, s_id):
		series = self.tree.getroot()
		for serie in series.findall('serie'):
			if serie.find('id').text == str(s_id):
				return True
		return False

	"""
		The ``listSeries`` method
		=========================
		
		Return the list of TV Shows in configuration file

		:return: list of TV Shows ID
		:rtype: list of Integers

		:Example:
		f.listSeries()
		[542,5428,45758]
		
	"""
	def listSeries(self):
		result = []
		series = self.tree.getroot()
		for serie in series.findall('serie'):
			emails_list = []
			for email in serie.findall('email'):
				emails_list.append(email.text)
			result.append({
				'id': 		int(serie.find('id').text),
				'name':		str(serie.find('name').text),
				'season': 	int(serie.find('season').text),
				'episode': 	int(serie.find('episode').text),
				'status': 	int(serie.find('status').text),
				'slot_id': 	int(serie.find('slot_id').text),
				'expected':	convert_date(serie.find('expected').text),
				'emails': 	emails_list
					})
		return result

	def updateSerie(self,s_id,values):
		result = False
		series = self.tree.getroot()
		for serie in series.findall('serie'):
			if serie.find('id').text == str(s_id):
				for val in values.keys():
					serie.find(val).text = str(values[val])
				result = True
		self._save()
		return result

