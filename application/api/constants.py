#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import json

filepath = '../../directory.json'
json_data = open(filepath)
directories = json.load(json_data)

TSW=True
ARCH=directories['arch']
CONF_VERSION='1.8'
CONF_FILE=directories['configpath']+'/config.xml'
SERIES_FILE=directories['seriepath']+'/series.xml'
API_FILE=directories['scriptpath']+'/TSW_api.py'
RUN_FILE=directories['scriptpath']+'/tvShowWatch.py'
TMP_DIR='tmp'
PYTHON_EXEC=[directories['python_exec']]
CMD=[PYTHON_EXEC,RUN_FILE,'-c',CONF_FILE]
os.environ['PATH'] = directories['python_path'] + ':' + os.environ['PATH']

