# -*- coding: utf-8 -*-
__author__ = "zjt"

import json,time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

from core.user import load_user,dump_user
from conf import settings


def login(db_path,username="",password=""):

	exit_flag = False
	lock_count = 0
	while not exit_flag :
		if username == "" or password == "" :
			username = input("请输入用户名：").strip()
			if username == "b" or username == "B":
				return "back"
			password = input("请输入密码：").strip()
			# password = hashlib.sha1(password.encode("utf8")).hexdigest()
		userdata = load_user(username,db_path)
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
					dump_user(userdata,db_path)
					print('\033[31;1m【%s】已被锁死，请联系管理员解锁！\033[0m' % (username))
					#exit_flag  = True
					return False
				else:
					print('\033[31;1m密码错误，请重新输入，您还有%d次机会，账户将被锁死！\033[0m\n'% (3 - lock_count ))

			else:
				#print('\033[31;1m登录成功，欢迎-- %s --回来！\033[0m' % (username))
				return userdata



def auth1(func):

	def wrapper(*args,**kwargs):
		print("学生登录".center(80,"-") )
		path = os.path.join(settings.ACCOUNTS_DB_DIR,'students')
		userdata = login(path)
		if not userdata:
			print('\033[1;31;1m登录失败！\033[0m')
		elif userdata == 'back':
			print("返回上一级...")
		else:
			print("\033[32;1m登录成功！\033[0m")
			res = func(userdata)

			#return func(*args,**kwargs)
			return res
	return wrapper

def auth2(func):

	def wrapper(*args,**kwargs):
		print("教师\管理员登录".center(80,"-") )
		path = os.path.join(settings.ACCOUNTS_DB_DIR,'teachers')
		userdata = login(path)
		if not userdata:
			print('\033[1;31;1m登录失败！\033[0m')
		elif userdata == 'back':
			print("返回上一级...")
		else:
			print("\033[32;1m登录成功！\033[0m")
			res = func(*args)

			#return func(*args,**kwargs)
			return res
	return wrapper

def auth3(func):
	def wrapper(*args,**kwargs):
		print("管理员登录".center(50, "-"))
		path = os.path.join(settings.ACCOUNTS_DB_DIR,'admins')
		userdata = login(path)
		if not userdata:
			print('\033[31;1m登录失败！\033[0m')
		elif userdata == 'back':
			print("返回上一级...")
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