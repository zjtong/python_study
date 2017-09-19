# -*- coding: utf-8 -*-
__author__ = "zjt"
import os,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR )
# print(BASE_DIR)

from core import student,teacher,admin
def run():
    menu = '''
    ------ 选课系统 ------
       1. 学生入口
       2. 教师入口
       3. 管理员入口
       4. 退出
    '''

    menu_dic = {
        "1": student.show_menu,
        "2": teacher.show_menu,
        "3": admin.main,
        "4": exit
    }

    while True:
        print(menu)
        choice = input("\033[32;1m请选择(‘b':返回上一级>>>:\033[0m").strip().lower()
        if choice in menu_dic:
            menu_dic[choice]()
        elif choice == "b":
            continue
        else:
            print('\033[31;1m输入错误!请重新输入...\033[0m')

if __name__ == '__main__':
    run()