#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import logging
import xml.etree.ElementTree as ET
from Prompt import *
import messages

FILE = sys.path[0] + '/test.xml' if sys.path[0] != '' else 'test.xml'
FILE_VERSION = "1.0"

class MyFile:
	def __init__(self, root = 'root', description = 'file'):
		self.description = description
		self.root = root
		self.pushOpened(False)

	def openFile(self,filename = FILE,createIfNotExist=True):
		self.filename = filename
		if not self.testFileExists():
			if (createIfNotExist):
				logging.info(self.description + " creation")
				self.createBlankFile(filename)
				return self._create()
			else:
				self.pushOpened(False)
				return {'rtn':'401','error':messages.returnCode['401'].format(self.description)}
		else:
			self.tree = ET.parse(self.filename)
			if self.getVersion() != self._version():
				mig_meth = "migration_" + str(self.getVersion()) + "_to_" + str(self._version())
				if mig_meth in dir(self):
					migration_res = getattr(self,mig_meth)()
					self.pushOpened(True)
					return {'rtn':'200','error':messages.returnCode['200']}
				else: 
					self.pushOpened(False)
					return {'rtn':'402','error':messages.returnCode['402'].format(self.description,self.getVersion(),self._version())}
			else:
				self.pushOpened(True)
				return {'rtn':'200','error':messages.returnCode['200']}
	
	def pushOpened(self,state=False):
		self.opened = state
		logging.info(self.description + " opened state is now " + str(self.opened))

	# You MUST redefine this method with the appropriate constant
	def _version(self):
		return FILE_VERSION

	def createBlankFile(self,filename = FILE):
		self.filename = filename
		self._create_root()
		self.pushOpened(True)

	def openedFile(self):
		logging.info("Opened file : " + str(self.opened))
		if(self.opened):
			return {'rtn':'200','error':messages.returnCode['200']}
		else:
			return {'rtn':'403','error':messages.returnCode['403'].format(self.description)}

	def _create(self):
		logging.info("Creating file " + str(self.filename))
		#self._create_root()
		self._save()
		self.pushOpened(True)
		return {'rtn':'200','error':messages.returnCode['200']}
		#return self._create_root()

	def _create_root(self):
		root = ET.Element(self.root)
		self.tree = ET.ElementTree(root)
		version = ET.SubElement(root,'version')
		version.text = self._version()
		self.pushOpened(False)

		return root

	"""
		The ``_save`` method
		====================
		
		Save configuration in config file

		:return: True if file saving is OK
		:rtype: boolean

		:Example:

		>>> f._save()
		True
		
	"""
	def _save(self):
		#ET.dump(self.tree)
		self.tree.write(self.filename)
		return True

	"""
		The ``testFileExists`` method
		=============================
		
		Use it in order to test if configuration file exists

		:return: True if file exists
		:rtype: boolean

		:Example:

		>>> f._testFileExists()
		True
		
	"""
	def testFileExists(self):
		if os.path.isfile(self.filename): 
			conffile = open(self.filename, 'r')
			conffile.readlines()
			conffile.close()
			return True
		else:
			return False

	"""
		The ``reset`` method
		====================
		
		Use it in order to reset configuration file.

		:return: True if reset completed
		:rtype: boolean

		:Example:
		>>> f.reset()
		Are you sure you want to delete configuration? [y/N]
		n
		False
		
	"""
	def reset(self,filename = FILE):
		if promptYN("Do you want to delete " + self.description + " ?",'N'):
			self.createBlankFile(filename)
			self._create()
			print(self.description + " reseted")
			return True
		return False

	def getVersion(self):
		conf = self.tree.getroot()
		return conf.find('version').text

	def change(self,configData,value='None'):
		path = configData.split('_')
		if value == 'None':
			value = getattr(self, "select_" + configData)()
		conf = self.tree
		node = conf.getroot()
		
		for path in configData.split('_'):
			if node.find(path) is None:
				node = ET.SubElement(node,path)
			else:
				node = node.find(path)
		
		node.text = str(value)
		self.tree = conf
		return str(value)
#		self._save()
	

