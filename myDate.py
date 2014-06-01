#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import string
from datetime import datetime, date, time

FORMAT = "%Y-%m-%dT%H:%M:%S"

def convert_date(str_date):
	try:
		split_date = string.split(str_date,'-')
		return date(int(split_date[0]),int(split_date[1]),int(split_date[2]))
	except:
		return None

def print_date(ma_date):
	return ma_date.strftime('%d/%m/%Y')

def isoparse(s):
	try:
		return datetime.strptime(s,FORMAT)
		return datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]),
			int(s[11:13]), int(s[14:16]), int(s[17:19]))
	except:
		print(s)
		return None

def myToday():
	return date.today()
