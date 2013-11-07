#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import logging
import xml.etree.ElementTree as ET
from Prompt import *

FILE = sys.path[0] + '/test.xml' if sys.path[0] != '' else 'test.xml'
FILE_VERSION = "1.0"

class MyFile:
	def __init__(self, filename = FILE, root = 'root', description = 'file'):
		self.description = description
		self.root = root
		self.filename = filename
		if not self.testFileExists():
			logging.info(description + " creation")
			self._create()
		else:
			self.tree = ET.parse(self.filename)
			if self.getVersion() != self._version():
				if promptYN("Your {0} file version ({1}) is obsolet (<{2}). Do you want reset it?".format(description,self.getVersion(),self._version()),'N'):
					self._create()
				else:
					sys.exit()

	# You MUST redifine this method with the appropriate constant
	def _version(self):
		return FILE_VERSION

	def _create(self):
		self._create_root()
		self._save()
		return self._create_root()

	def _create_root(self):
		root = ET.Element(self.root)
		self.tree = ET.ElementTree(root)
		version = ET.SubElement(root,'version')
		version.text = self._version()

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
	def reset(self):
		if promptYN("Are you sure you want to delete " + self.description + " ?",'N'):
			self._create()
			print(self.description + " reseted")
			return True
		return False

	def getVersion(self):
		conf = self.tree.getroot()
		return conf.find('version').text

	def change(self,configData):
		value = getattr(self, "select_" + configData)()
		conf = self.tree.getroot()
		conf.find(configData).text = str(value)
		self._save()
	

