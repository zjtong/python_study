#!_*_coding:utf-8_*_
#__author__:"Alex Li"

from conf import settings
from core import cards
from core import logger
#transaction logger



def make_transaction(log_obj,carddata,tran_type,amount,**others):
    '''
    处理用户所有的交易：还款、提现、转账
    :param account_data: user account data
    :param tran_type: transaction type
    :param amount: transaction amount
    :param others: mainly for logging usage
    :return:
    '''
    amount = float(amount)
    if tran_type in  settings.TRANSACTION_TYPE:
        #手续费
        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_banlance = carddata['banlance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_banlance = old_banlance + amount + interest
            if carddata ["credit"] - new_banlance < 0:
                print("\033[31;1m您的账单额度： [%s] ，本次还款金额为： [%s], 还款金额大于账单金额！\033[0m"%((carddata ["credit"] - carddata['banlance']),(amount + interest)))
                return (False ,carddata)
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_banlance = old_banlance - amount - interest
            #check credit
            if  new_banlance <0:
                print('\033[31;1m您的可用额度： [%s] ，本次交易金额为： [%s], 您的可用额度不足以完成本次交易！\033[0m' %(carddata['banlance'],(amount + interest) ))
                return (False ,carddata)
        carddata['banlance'] = new_banlance

        cards.dump_cards(carddata) #save the new balance back to file

        log_obj.info("username:%s   card_id:%s   tran_type:%s    amount:%s   interest:%s" %
                          (carddata["owner"],carddata["card_id"], tran_type, amount,interest) )
        return (True ,carddata)
    else:
        print("\033[31;1m交易类型： [%s] 不存在!\033[0m" % tran_type)
