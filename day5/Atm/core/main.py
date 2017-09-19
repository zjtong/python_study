# -*- coding: utf-8 -*-
__author__ = "zjt"


import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import shopping,cards
from admin import shop_manage,card_manage

def show_menu():
    """功能菜单"""
    menu = '''
	-------- ATM + 购物商城系统 --------
	1.  购物商城系统
	2.  ATM信用卡系统
	3.  用户管理系统
	4.  信用卡管理系统
	5.  退出
	'''
    menu_dic = {
		"1" : shopping.shopping,
		"2" : cards.interactive,
		"3" : shop_manage.shop_menu,
        "4" : card_manage.card_menu,
		"5" : exit

	}
    exit_flag = False
    while not exit_flag:
        print(menu)
        choice = input("\033[32;1m请选择>>>>:\033[0m").strip()
        if choice in menu_dic:
            menu_dic[choice ]()
        else:
            print('\033[31;1m输入错误!请重新输入...\033[0m')

if __name__ == '__main__':
    show_menu()
