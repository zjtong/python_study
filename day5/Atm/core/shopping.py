__author__ = 'Administrator'


import json,time,datetime
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from admin import shop_manage,card_manage
from core import user,cards,auth,logger
from core import transaction
from conf import settings

#transaction logger
trans_logger = logger.logger('transaction')
shop_logger = logger.logger('shopping')


@auth.auth1
def shopping(userdata):

    #购物
    user_shopping = []
    exit_flag = False
    while not exit_flag:
        product = show_product()    #打印商品列表
        act = input('请选择要购买商品的商品编号（"q" : 结束购物并结账）：').strip()
        if act.isdigit():
            act = int(act)
            if act < len(product):
                user_shopping.append(product[act])
                print('您将【\033[1;32;1m%s\033[0m】加入购物车。' % (product[act][0]))
            else:
                print('\033[1;32;1m选择错误，请重新选择！\033[0m')
        elif act == 'q':
            if user_shopping :
                res = settlement(userdata,user_shopping)
                if res[0]:
                    print("\033[32;1m结算成功,消费金额：%s \033[0m"%res[2])
                    exit_flag = True
                else:
                    print("\033[32;1m 结算失败 \033[0m" )
            else:
                exit_flag = True
        else:
            print('\033[32;1m选择错误，请重新选择！\033[0m')

    shop_logger.info("uaername:%s   bill:%s   shopping_record:%s    " %
                 (userdata["username"], res[2], user_shopping))

def settlement(userdata,shopping_list):
    print("------ 购物车 ------")
    bill = 0
    money = userdata["money"]
    for items in shopping_list:
        print(items)
        bill += items[1]
    print("购物车商品总金额：%s"%bill)
    if money >= bill:
        money -= bill
        userdata["money"] = money
        user.dump_user(userdata)
        return (True,userdata,bill)
    else:
        print("\033[32;1m现金余额不足，请使用信用卡结算！\033[0m")
        while True:
            card_id = input("请输入本人信用卡卡号: ").strip()
            if len(card_id) == 8 and card_id .isdigit():
                carddata = cards.get_cards(card_id )
                if carddata:
                    if userdata["card_id"] != card_id:
                        print("\033[32;1m该信用卡不是本人信用卡，无法使用！\033[0m")
                    elif carddata["frozen"]:
                        print("\033[32;1m该信用卡已被冻结，无法使用！\033[0m")
                        return (False, userdata, bill)
                    else:
                        # banlance = carddata["banlance"]
                        # #total_money = banlance + money
                        # if banlance >= bill:
                        #     # banlance -= bill
                        #     # carddata["banlance"] = banlance
                        #     cards.dump_cards(carddata)
                        #     return (True, userdata,bill)
                        consume_amount = bill
                        res = transaction.make_transaction(trans_logger, carddata, 'consume', consume_amount)
                        if res[0]:
                            return (True, userdata, bill)
                        else:
                            print("\033[32;1m信用卡可用额度不足，无法完成结算！\033[0m")
                            return (False, userdata, 0)
                else:
                    print("\033[31;1m卡号不存在，请重新输入！\033[0m")
            else:
                print("\033[31;1m输入卡号错误，请重新输入！\033[0m")



def show_product():
    product_dict = get_product()
    current_product = []
    print("商品列表".center(60,"*"))
    print("|", "商品编号".center(6, " "), "|", "名称".center(20, " "), "|", "价格".center(20, " "), "|")
    i = 0
    for product in product_dict:
        current_product.append((product,product_dict[product]))
        print("|", str(i).center(10, " "), '|', product.center(22, ' '), '|',str('￥%d元' % (product_dict[product])).center(18, ' '),"|")
        i += 1
    return current_product

def get_product():
    try:
        f = open('%s\\db\\products.json' % (BASE_DIR),'r',encoding='utf-8')
    except FileNotFoundError:
        res = {}
    else:
        try:
            res = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            res = {}
    if not res:
        print('\033[1;31;1m商品列表为空，请以管理员身份登录以添加商品！\033[0m')
        shop_manage.shop_menu()
    return res

if __name__ == '__main__':
    print(shopping())