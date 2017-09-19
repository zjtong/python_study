# -*- coding: utf-8 -*-
__author__ = "zjt"

import json,time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

from core.user import load_user,dump_user
# from core import logger
#
#
# access_logger = logger.logger('access')

def login(username="",password=""):
	"""
 	登录接口，默认登录参数空
 	:param username:
 	:param password:
	 :return: userdata
	"""
	exit_flag = False
	lock_count = 0
	while not exit_flag :
		if username == "" or password == "" :
			username = input("请输入用户名：").strip()
			password = input("请输入密码：").strip()
			# password = hashlib.sha1(password.encode("utf8")).hexdigest()
		userdata = load_user(username)
		#print(users)
		#print(username)
		if  not userdata :		#用户名不存在,读取不到用户信息
			username = ""
			print("\033[31;1m用户名不存在！请重新输入\033[0m\n")
			#login_flag = False
			continue
		else:
			if userdata["locked"] == True :	#用户被锁定
				exit_flag = True
				res = False
				print('\033[31;1m【%s】已被锁死，请联系管理员解锁！\033[0m' % (username))

			elif password != userdata["password"]:	#用户密码错误
				password = ""
				lock_count +=1
				if lock_count == 3 :
					userdata["locked"] = True
					dump_user(userdata)
					print('\033[31;1m【%s】已被锁死，请联系管理员解锁！\033[0m' % (username))
					#exit_flag  = True
					return False
				else:
					print('\033[31;1m密码错误，请重新输入，您还有%d次机会，账户将被锁死！\033[0m\n'% (3 - lock_count ))

			else:
				print('\033[31;1m登录成功，欢迎-- %s --回来！\033[0m' % (username))
				return userdata



def auth1(func):
	"""普通用户登录"""
	def wrapper(*args,**kwargs):
		print("用户登录".center(80,"-") )
		userdata = login()
		if not userdata:
			print('\033[1;31;1m登录失败！\033[0m')
		else:
			print("\033[32;1m用户登录成功！\033[0m")
			func(userdata)

			#return func(*args,**kwargs)
			#return res
	return wrapper

def auth2(func):
	def wrapper(*args,**kwargs):
		print("管理员登录".center(50, "-"))
		userdata = login()
		if not userdata:
			print('\033[31;1m登录失败！\033[0m')
		else:
			if userdata['authority']:#是否是管理员身份
				#func()
				print("\033[32;1m管理员登录成功！\033[0m")
				return func(*args,**kwargs)
			else:
				print('\033[31;1m您没有管理权限！\033[0m')
				exit()
	return wrapper

# @auth2
# def text(username):
# 	print("in the text",username)
#
# text("zjt")
# login()