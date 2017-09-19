# -*- coding: utf-8 -*-
__author__ = "zjt"

import os,sys,pickle
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR )
from core.models import Student
from core.models import Classes
from conf import settings
from core.user import load_user,dump_user
from core import auth

def show_menu():
    menu = '''
        ------ 学生菜单 ------
           1. 学生注册
           2. 查询成绩
           3. 退出
        '''

    menu_dic = {
        "1": register,
        "2": score,
        "3": exit
    }

    while True:
        print(menu)
        choice = input("\033[32;1m请选择(‘b':返回上一级>>>:\033[0m").strip().lower()
        if choice in menu_dic:
            menu_dic[choice]()
        elif choice == "b":
            break
        else:
            print('\033[31;1m输入错误!请重新输入...\033[0m')


def register():
    db_path = os.path.join(settings.ACCOUNTS_DB_DIR,'students')
    #print(db_path)
    exit_flag = False
    while not exit_flag :
        print("学生用户注册".center(50,"="))
        #username == student.name
        username = input("请输入您要注册的用户名【用户名必须为真实姓名】：").strip()
        if username in os.listdir(db_path):
            print("该用户名已注册，不能重新注册！")
            return False
        else:

            student_list= Student.get_all_obj_list()
            #print(student_list)
            for obj in student_list :
                #print(obj)
                if username == obj['name'] :
                    # student_obj = obj
                    password = input("请输入密码：").strip()
                    re_password = input('再次确认密码：').strip()
                    if password != re_password:
                        print('\033[31;1m两次输入的密码不一致!\033[0m')
                        continue
                    userdata = {
                                    "username" : username,
                                    "password" : password,
                                    'locked' : False,
                                    'authority': False,
                                    "student_nid" : obj['nid']
                                            }
                    dump_user(userdata,db_path )
                    print('\033[31;1m学生[%s] 注册成功！\033[0m'%username)
                    return True
            else:
                print("学生[%s] 不存在，无法注册！请联系管理员创建 学生[%s]！"%(username,username))
                    # exit_flag = True
                return False


@auth.auth1
def score(user):
    #print(user['student_nid'].get_obj_by_uuid()['score'])
    db_path=settings.SCORE_DB_DIR
    #print(db_path)

    score_nid = str(user['student_nid'])
    #print(type(score_nid ),score_nid)
    #print(os.listdir(db_path))
    for filename in os.listdir(db_path):
        if filename == score_nid:
            file_path = os.path.join(db_path, filename)
            #print(file_path)
            with open(file_path, 'rb') as f:
                item = pickle.loads(f.read())
                #print(item)
                print("学生[%s]  课程[%s]  分数【%s】"%(user['username'],\
                        item['score_dict']['course_to_teacher_nid'].get_obj_by_uuid(settings.COURSE_TO_TEACHER_DB_DIR)['course_nid'].get_obj_by_uuid(settings.COURSE_DB_DIR)['name'],\
                                              item['score_dict']['score']))

                return True

    else:
        print("教师还没有设置分数！")


if __name__ == '__main__':
    show_menu()