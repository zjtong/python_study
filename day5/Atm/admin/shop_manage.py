__author__ = "zjt"



import json,hashlib,time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print('%s\\db\\users.txt' % (BASE_DIR))
sys.path.append(BASE_DIR)

from core import user
from core import auth


@auth.auth2
def shop_menu():
    menu = """
    -------- 商城管理系统 --------
	1.  用户注册
	2.  用户解锁
	3.  添加商品
	4.  金额充值
	5.  退出
    """
    menu_dic = {
        "1" : register,
        "2" : unlock,
        "3" : product_add,
        "4" : money_recharge,
		"5" : exit
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        choice = input("\033[32;1m请选择(返回上一级：b)>>>>:\033[0m").strip().lower()
        if choice not in menu_dic:
            #menu_dic[choice]()
            print('\033[31;1m输入错误!请重新选择...\033[0m')
        if choice == '1':
            print('用户注册'.center(50,'*'))
            register()
        elif choice == '2':
            if unlock():
                print('\033[32;1m解锁成功！\033[0m')
            continue
        elif choice == '3':
            if product_add():
                print('\033[1;32;1m新增商品成功！\033[0m')
            continue
            # amin_card
        elif choice == '4':
            if money_recharge():
                print("\033[1;32;1m金额充值成功！\033[0m")
        elif choice == "5":
            menu_dic[choice]()
        elif choice == "b":
            return



def register():
    exit_flag = False
    while not exit_flag:
        username = input('请输入您要注册的用户名：').strip()
        temp_user = user.load_user(username)
        if temp_user:
            print('\033[31;1m此用户名已被注册！Change one!\033[0m')
            continue
        else:
            while not exit_flag:
                password = input('请输入密码：').strip()
                re_password = input('再次确认密码：').strip()
                if password != re_password:
                    print('\033[31;1m两次输入的密码不一致!\033[0m')
                    continue
                else:
                    exit_flag = True
                    userdata = {
                        "username" : "%s"%(username ),
                        "password" : "%s"%(password ),
                        "card_id" : "",
                        "locked" : False ,
                        "login_flag" : False,
                        "authority" : False,
                        "money" : 0
                                }
                    act = input("新用户设为管理员？（确认：Y，取消：N）>>>").strip().lower()
                    if act == "y":
                        userdata["authority"] = True
                    user.dump_user(userdata)
    print("\033[31;1m用户注册成功!\033[0m")
    return userdata
#register()

def unlock(username=""):
    if username == "":
        username = input("请输入要解锁的用户名：").strip()
    res = False
    userdata = user.load_user(username)
    if not userdata:
        print("用户[%s]未注册，无法解锁！"%username )
    else:
        if  not userdata["locked"]:
            print("用户[%s]已解锁，无法再次解锁！"%username)
        else:
            userdata["locked"] = False
            print("\033[31;1m用户[%s]已解锁！\033[0m"%username)
            user.dump_user(userdata)
            res = True
    return res
#unlock("zjt")


def product_add():
    with open('%s\\db\\products.json' % (BASE_DIR), 'r', encoding='utf-8') as f:
        products = json.loads(f.read())
        print("商城已有的商品为：",products )
    while True:
        product_name = input('输入新商品名称：')
        if product_name == "b":
            return False
        price = input('输入商品价格：')
        if price.isdigit():
            price = int(price)
            products[product_name] = price
            with open('%s\\db\\products.json' % (BASE_DIR),'w',encoding='utf-8') as f:
                f.write(json.dumps(products,ensure_ascii=False) )
            return True
        else:
            print('\033[1;31;1m错误：\033[0m','\033[1;36;1m商品价格必须是整数！\033[0m')
            continue

#product_add()

def money_recharge(username=""):
    if username == "":
        username = input("请输入要充值金额的用户名：").strip()
    res = False
    userdata = user.load_user(username)
    if not userdata:
        print("用户[%s]未注册，无法充值！"%username )
    else:
        while True:
            recharge = input("输入充值金额：").strip()
            if recharge .isdigit() :
                userdata["money"] = int(recharge ) + userdata["money"]
                user.dump_user(userdata)
                return True
            else:
                print("输入错误，请重新输入！")

#money_recharge()
# if __name__ == '__main__':
#     shop_menu()
#     #product_add()