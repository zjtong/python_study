# -*- coding: utf-8 -*-
__author__ = "zjt"

"""
信用卡管理接口
"""

import json
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

from core import user
from core import auth
from core import cards

@auth.auth2
def card_menu():
    menu = """
    -------- 信用卡管理系统 --------
	1.  添加信用卡
	2.  修改用户额度
	3.  冻结账户
	4.  解冻账户
	5.  退出
    """
    menu_dic = {
        "1" : card_add,
        "2" : card_modify,
        "3" : card_freeze,
		"4" : card_unfreeze,
        "5" : exit
    }

    exit_flag = False
    while not exit_flag:
        print(menu)
        choice = input("\033[32;1m请选择(返回上一级：b)>>>>:\033[0m").strip().lower()
        if choice in menu_dic:
            menu_dic[choice]()
        elif choice == "b":
            return
        else:
            print('\033[31;1m输入错误!请重新选择...\033[0m')

def card_add(username=""):
    """
	添加用户名下的信用卡账户
	:param username
	:return: (username,card_id)
	"""
    res = False
    exit_flag = False
    if username == "":
        username = input("请输入要添加信用卡的用户名：").strip()
    userdata = user.load_user(username)
    if  userdata["card_id"]:
        print("%s 名下已有信用卡，无法再次申请！"%username)
    else:
        while not exit_flag:
            card_id = input('请输入信用卡卡号（必须为纯数字8位）：')

            if  card_id.isdigit() and len(card_id) == 8:
                if userdata["card_id"] == card_id :
                    print('\033[31;1m卡号已存在!\033[0m')
                else:
                    userdata["card_id"] = card_id
                    while not exit_flag:
                        card_credit = input('请输入信用卡最高额度：').strip()
                        if card_credit.isdigit():
                            carddata = {
                                "card_id" : card_id ,
                                "owner" : username,
                                "credit" : int(card_credit),
                                "banlance" : int(card_credit),
                                "frozen" : False
                            }

                            with open("%s\\db\\accounts\\%s.json" % (BASE_DIR, username), "w", encoding="utf-8") as f1,\
                                open("%s\\db\\cards\\%s.json" % (BASE_DIR, card_id), "w", encoding="utf-8") as f2:
                                f1.write(json.dumps(userdata))
                                f2.write(json.dumps(carddata))
                            res = (username,card_id)
                            exit_flag = True
                            print("%s 添加信用卡成功！"%username)
                        else:
                            print('\033[1;31;1m信用卡额度必须为整数!\033[0m')
            else:
                print('\033[31;1m卡号错误!请重新输入...\033[0m\n')



    return res

def card_modify(card_id=""):
    """
    信用卡额度修改
    :param card_id
    :return: carddata
    """
    print('信用卡额度修改'.center(80, '-'))
    res = False
    if card_id == "":
        card_id = input("请输入要修改额度的信用卡卡号（8位纯数字)：").strip()

    card = cards.get_cards(card_id )
    if not card :
        print("信用卡卡号无效，无法修改额度！" )
    else:
        while True :
            new_credit = input("'请为卡号：%s 设定新的信用卡额度（当前额度%d元）：\t"%(card["card_id"],card["credit"])).strip()
            if new_credit.isdigit() :
                new_credit = int(new_credit)
                cost = card["credit"] - card["banlance"]
                if new_credit >= cost:
                    card["banlance"] = new_credit - cost
                    card["credit"] = new_credit
                    with open("%s\\db\\cards\\%s.json" % (BASE_DIR, card_id), "w", encoding="utf-8") as f:
                        f.write(json.dumps(card))
                    res = card
                    print("卡号：%s 额度修改成功！" % card_id)
                    break

                else:
                    print("新额度小于账单金额，无法修改信用卡额度！")
            else:
                 print('\033[31;1m信用卡额度必须为整数!\033[0m')
    return res

def card_freeze(card_id=""):
    """
    冻结信用卡账户
    """
    res = False
    if card_id == "":
        card_id = input("请输入要冻结的信用卡卡号（8位纯数字)：").strip()
    card = cards.get_cards(card_id)
    if not card:
        print("信用卡卡号无效，无法冻结信用卡账户！")
    else:
        if card["frozen"]:
            print("此信用卡已冻结，无需再次冻结！")
        else:
            act = input("确认冻结该信用卡？（确认：Y，取消：N）>>>>:\t").lower()
            if act == "y":
                card["frozen"] = True
                print("\033[31;1m卡号：%s 信用卡已冻结！\033[0m"%card_id)
                with open("%s\\db\\cards\\%s.json" % (BASE_DIR, card_id), "w", encoding="utf-8") as f:
                    f.write(json.dumps(card))
                res = card
                #print("信用卡冻结成功！")
    return res

def  card_unfreeze(card_id=""):
    res = False
    if card_id == "":
        card_id = input("请输入要解冻的信用卡卡号（8位纯数字)：").strip()
    card = cards.get_cards(card_id)
    if not card:
        print("信用卡卡号无效，无法解冻信用卡账户！" )
    else:
        if  not card["frozen"]:
            print("此信用卡已解冻，无需再次解冻！")
        else:
            act = input("确认解冻该信用卡？（确认：Y，取消：N）>>>>:\t").lower()
            if act == "y":
                card["frozen"] = False
                print("\033[31;1m卡号：%s 信用卡已解冻！\033[0m"%card_id )
                with open("%s\\db\\cards\\%s.json" % (BASE_DIR, card_id), "w", encoding="utf-8") as f:
                    f.write(json.dumps(card))
                res = card
                #print("信用卡解冻成功！")
    return res




if __name__ == '__main__':
     card_menu()

#print(card_add("zjt"))
#card_modify("zjt")
#card_frozen("zjt")
#card_unlock("zjt")