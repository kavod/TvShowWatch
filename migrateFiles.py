#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import stat
import myConstants
import ConfFile
import ConfFileJSON
import serieList
import serieListJSON
import json
import myExceptions

class ConfFileMig(ConfFileJSON.ConfFile):
	def __init__(self):
		ConfFileJSON.ConfFile.__init__(self)
		
	def openFile(self,filename = myConstants.CONFIG_FILE):
		resultJSON = ConfFileJSON.ConfFile.openFile(self,filename,createIfNotExist=False)
		if resultJSON['rtn'] == '200':
			return resultJSON
		else:
			filenameXML = os.path.dirname(os.path.abspath(filename)) + os.sep + 'config.xml'
			mig = ConfFile.ConfFile()
			result = mig.openFile(filenameXML)
			if result['rtn'] == '200':
				self.migration(mig)
				return self.openFile(filename)
			else:
				return resultJSON
			
	def migration(self,mig):
		print "Migration of " + str(mig.filename)
		conf = {
			'tracker':mig.getTracker(),
			'transmission':mig.getTransmission(),
			'smtp':mig.getEmail(),
			'keywords':mig.getKeywords(),
			'version':"2.0"
			}
		filename = os.path.dirname(os.path.abspath(mig.filename)) + os.sep + 'config.json'
		with open(filename, 'w') as outfile:
			json.dump(conf, outfile)
		os.chmod(filename,stat.S_IRUSR | stat.S_IWUSR)
		os.remove(mig.filename)
		
class SerieFileMig(serieListJSON.SerieList):
	def __init__(self):
		serieListJSON.SerieList.__init__(self)
		
	def openFile(self,filename = myConstants.SERIES_FILE):
		resultJSON = serieListJSON.SerieList.openFile(self,filename,createIfNotExist=False)
		if resultJSON['rtn'] == '200':
			return resultJSON
		else:
			filenameXML = os.path.dirname(os.path.abspath(filename)) + os.sep + 'series.xml'
			mig = serieList.SerieList()
			result = mig.openFile(filenameXML,createIfNotExist=False)
			if result['rtn'] == '200':
				self.migration(mig)
				return self.openFile(filename)
			else:
				resultJSON = serieListJSON.SerieList.openFile(self,filename,createIfNotExist=True)
				return resultJSON
	
	def migration(self,mig):
		print "Migration of " + str(mig.filename)
		series = mig.listSeries(json_c=True,retr_tvdb_data=False)
		for serie in series:
			del serie['tvdb']
			del serie['lastEpisode']
			del serie['nextEpisode']
		jsonContent = {"version":"2.0","series":series}
		filename = os.path.dirname(os.path.abspath(mig.filename)) + os.sep + 'series.json'
		with open(filename, 'w') as outfile:
			json.dump(jsonContent, outfile)
		os.chmod(filename,stat.S_IRUSR | stat.S_IWUSR)
		os.remove(mig.filename)
		
def migrate():
	c=ConfFileMig()
	c.openFile()
	s=SerieFileMig()
	s.openFile()
		
if __name__ == '__main__':
	c=ConfFileMig()
	print "Conf openFile"
	print c.openFile()
	s=SerieFileMig()
	print "Serie openFile"
	print s.openFile()
