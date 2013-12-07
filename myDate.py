#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import string
import datetime

def convert_date(str_date):
	try:
		split_date = string.split(str_date,'-')
		return datetime.date(int(split_date[0]),int(split_date[1]),int(split_date[2]))
	except:
		return None

def print_date(ma_date):
	return ma_date.strftime('%d/%m/%Y')

def myToday():
	return datetime.date.today()
