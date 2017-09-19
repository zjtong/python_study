# -*- coding: utf-8 -*-
__author__ = "zjt"

import os,sys
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR )

def load_user(username):
	"""
	从文件中读取用户信息
	:return: userdata
	"""
	try:
		info = open("%s\\db\\accounts\\%s.json"%(BASE_DIR,username ),"r",encoding = "utf-8")
	except FileNotFoundError :
		#print("\033[31;1m用户信息文件不存在！\033[0m")
		userdata = {}
		return userdata
	else:
		try:
			userdata = json.loads(info.read())
		except json.decoder.JSONDecodeError:
			#print('\033[31;1m用户信息文件读取错误！\033[0m')
			userdata = {}
	return userdata
#
# print(load_user("zjt") )

def dump_user(userdata):
	"""
	存储用户信息到文件中
	:return: True
	"""
	if  not userdata:
		print("用户数据不存在！")
	else:
		with open("%s\\db\\accounts\\%s.json"%(BASE_DIR,userdata["username"]),"w",encoding = "utf-8") as f:
			f.write(json.dumps(userdata) )
		return True
#
# userdata = {"login_flag": False, "password": "123456", "card_id": "", "payword": "", "limit": 0, "username": "zxy", "banlance": 0, "frozen": False, "locked": False}
#
#
# print(dump_user(userdata) )


