#!/usr/bin/env python
#encoding:utf-8

# Usage: VAR=$(./bashconstant.py dict_key < file.json)

import json,sys;

obj=json.load(sys.stdin);
print obj[sys.argv[1]]
