#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import json

def tracker_api_conf(post):
	conf_out = {"id":post.getvalue('tracker_id'),"user":post.getvalue('tracker_username')}
	if post.getvalue('tracker_password') != 'initial':
		conf_out["password"] = post.getvalue('tracker_password')
	return json.dumps(conf_out)

def transmission_api_conf(post):
	conf_out = {
		"server":post.getvalue('trans_server'),
		"port":post.getvalue('trans_port'),
		"user":post.getvalue('trans_username')
		}
	if post.getvalue('trans_password') != 'initial':
		conf_out["password"] = post.getvalue('trans_password')
	conf_out.update({
		"slotNumber":post.getvalue('trans_slotNumber'),
		"folder":post.getvalue('trans_folder')
		})
	return json.dumps(conf_out)

def email_api_conf(post):
	if values.getvalue('smtp_enable') == '0':
		return json.dumps({"enable":False})
	else:
		values = post
	conf_out = {
		"server":values.getvalue('smtp_server'),
		"port":values.getvalue('smtp_port'),
		"user":values.getvalue('smtp_username'),
		"emailSender":values.getvalue('smtp_emailSender'),
		"ssltls":values.getvalue('smtp_ssltls') == '1'
		}
	if values.getvalue('smtp_password') != 'initial':
		conf_out["password"] = values.getvalue('smtp_password')
	return json.dumps(conf_out)
