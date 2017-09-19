__author__ = "zjt"

"""
普通用户信用卡接口
提供：个人账单、信用卡还款、提现业务
"""
import json
import os
import sys
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

from core import auth
from conf import settings
from core import cards
from core import logger
from core import user
from admin import card_manage
from core import transaction

#transaction logger
trans_logger = logger.logger('transaction')
#access logger
access_logger = logger.logger('access')

def repay(userdata):
    '''
    print current balance and let user repay the bill
    :return:
    '''
    carddata = get_cards(userdata["card_id"])
    if carddata:
        # current_balance= ''' --------- 信用卡信息 --------
        #     信用额度 :   %s
        #     可用额度 :   %s
        #     账单金额 :   %s''' %(carddata['credit'],carddata['banlance'],(carddata['credit']-carddata['banlance']))

        back_flag = False
        while not back_flag:
            current_balance= ''' \n--------- 信用卡信息 --------
            信用额度 :   %s
            可用额度 :   %s
            账单金额 :   %s''' %(carddata['credit'],carddata['banlance'],(carddata['credit']-carddata['banlance']))
            print(current_balance)
            repay_amount = input("\033[33;1m\t输入还款金额(返回上一级：b):\033[0m").strip()
            if len(repay_amount) >0 and repay_amount.isdigit():
                res = transaction.make_transaction(trans_logger,carddata,'repay', repay_amount)
                carddata = res[1]
                #new_balance = carddata["banlance"]
                #if new_balance:
                    #print('''\033[42;1m\t可用额度: %s\033[0m''' %(new_balance))
            elif repay_amount == 'b':
                back_flag = True
            else:
                print('\033[31;1m输入错误，请输入大于0的整数！\033[0m' % repay_amount)
    else:
        print("此用户没有信用卡！")

def withdraw(userdata):
    '''
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    '''
    #account_data = accounts.load_current_balance(acc_data['account_id'])
    carddata = get_cards(userdata["card_id"])
    if carddata:

        back_flag = False
        while not back_flag:
            current_banlance= '''
			 --------- 信用卡信息 --------
				信用额度 :   %s
				可用额度 :   %s
				账单金额 :   %s''' %(carddata['credit'],carddata['banlance'],(carddata['credit']-carddata['banlance']))
            print(current_banlance)
            withdraw_amount = input("\033[33;1m\t输入取现金额(返回上一级：b):\033[0m").strip()
            if len(withdraw_amount) >0 and withdraw_amount.isdigit():
                res = transaction.make_transaction(trans_logger,carddata,'withdraw', withdraw_amount)
                carddata = res[1]
                #new_banlance = carddata["banlance"]
                # if new_banlance:
                #     print('''\033[42;1m可用额度: %s\033[0m''' %(new_banlance))
            elif withdraw_amount == 'b':
                back_flag = True
            else:
                print('\033[31;1m[%s] 输入错误, 请输入大于0的整数!\033[0m' % withdraw_amount)
    else:
        print("此用户没有信用卡！")

def transfer(userdata):
    carddata = get_cards(userdata["card_id"])
    if carddata:
        back_flag = False
        while not back_flag:
            current_banlance= '''
			 --------- 信用卡信息 --------
				信用额度 :   %s
				可用额度 :   %s
				账单金额 :   %s''' %(carddata['credit'],carddata['banlance'],(carddata['credit']-carddata['banlance']))
            print(current_banlance)
            transfer_card = input("\033[33;1m\t输入转入卡号(返回上一级：b：\033[0m").strip()
            if len(transfer_card ) == 8 and transfer_card .isdigit():
                transfer_carddata = get_cards(transfer_card )
                if transfer_carddata :
                    transfer_amount = input("\033[33;1m\t输入转账金额(返回上一级：b)：\033[0m").strip()
                    if len(transfer_amount) >0 and transfer_amount .isdigit():
                        res = transaction.make_transaction(trans_logger,carddata,'transfer', transfer_amount )
                        carddata = res[1]
                        if res[0]:
                            transfer_carddata ["banlance"] += int(transfer_amount)
                            dump_cards(transfer_carddata)
                            print("\033[33;1m转账成功！\033[0m")
                    else:
                        print("\033[31;1m 输入错误, 请输入大于0的整数!\033[0m")
                else:
                    print("\033[31;1m卡号不存在，请重新输入！\033[0m")

            elif transfer_card == "b":
                back_flag = True
            else:
                print("\033[31;1m输入卡号错误，请重新输入！\033[0m")
    else:
        print("此用户没有信用卡！")
        #print("\033[31;1m此用户没有信用卡，请以管理员身份登录添加信用卡！\033[0m！")
        #card_manage.card_menu()


def pay_check(userdata):
    carddata = get_cards(userdata["card_id"])
    if carddata:
        current_balance= '''
             --------- 信用卡信息 --------
            信用额度 :   %s
            可用额度 :   %s
            账单金额 :   %s''' %(carddata['credit'],carddata['banlance'],(carddata['credit']-carddata['banlance']))
        print(current_balance)
    else:
        print("此用户没有信用卡！")

# def make_transaction(log_obj,carddata,tran_type,amount,**others):
#     '''
#     处理用户所有的交易：还款、提现、转账
#     :param account_data: user account data
#     :param tran_type: transaction type
#     :param amount: transaction amount
#     :param others: mainly for logging usage
#     :return:
#     '''
#     amount = float(amount)
#     if tran_type in  settings.TRANSACTION_TYPE:
#         #手续费
#         interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
#         old_banlance = carddata['banlance']
#         if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
#             new_banlance = old_banlance + amount + interest
#             if carddata ["credit"] - new_banlance < 0:
#                 print("\033[31;1m您的账单额度： [%s] ，本次还款金额为： [%s], 还款金额大于账单金额！\033[0m"%((carddata ["credit"] - carddata['banlance']),(amount + interest)))
#                 return (False ,carddata)
#         elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
#             new_banlance = old_banlance - amount - interest
#             #check credit
#             if  new_banlance <0:
#                 print('\033[31;1m您的可用额度： [%s] ，本次交易金额为： [%s], 您的可用额度不足以完成本次交易！\033[0m' %(carddata['banlance'],(amount + interest) ))
#                 return (False ,carddata)
#         carddata['banlance'] = new_banlance
#
#         cards.dump_cards(carddata) #save the new balance back to file
#
#         log_obj.info("username:%s   card_id:%s   tran_type:%s    amount:%s   interest:%s" %
#                           (carddata["owner"],carddata["card_id"], tran_type, amount,interest) )
#         return (True ,carddata)
#     else:
#         print("\033[31;1m交易类型： [%s] 不存在!\033[0m" % tran_type)


def get_cards(card_id=""):
    """
    获取信用卡数据
	:param card_id
	:return: res
	"""
    #if card_id == "":
        #card_id = input("请输入信用卡卡号（8位纯数字)：").strip()
    try:
        info = open('%s\\db\\cards\\%s.json' % (BASE_DIR,card_id),'r',encoding='utf-8')
    except FileNotFoundError:
        #with open('%s\\db\\cards\\%s.json' % (BASE_DIR,card_id), 'w', encoding='utf-8') as f:
            #f.write('{}')
        res = {}
    else:
        try:
            res = json.loads(info.read())
        except json.decoder.JSONDecodeError:
            res = {}
    if len(res) == 0:
        print('\033[1;31;1m信用卡列表为空，请添加卡片！\033[0m')
    return res

def dump_cards(carddata):
    """
    	存储信用卡信息到文件中
    	:return: True
    	"""
    if not carddata:
        print("用户数据不存在！")
    else:
        with open("%s\\db\\cards\\%s.json" % (BASE_DIR, carddata["card_id"]), "w", encoding="utf-8") as f:
            f.write(json.dumps(carddata))
        return True

@auth.auth1
def interactive(userdata):
    '''
    interact with user
    :return:
    '''
    menu = '''
    ------- ATM信用卡系统 ---------
    \033[32;1m
    1.  还款
    2.  取款
    3.  转账
    4.  账单
    5.  退出
    \033[0m'''
    card_menu = {
        '1': repay,
        '2': withdraw,
        '3': transfer,
        '4': pay_check,
        '5': exit
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input("请选择(返回上一级：b)>>>>:").strip()
        if user_option in card_menu:
            if user_option == "5":
                exit()
            card_menu[user_option](userdata)
        elif user_option == "b":
            return
        else:
            print("\033[31;1m选项不存在!\033[0m")

#
# interactive()