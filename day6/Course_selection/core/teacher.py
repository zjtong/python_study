# -*- coding: utf-8 -*-
__author__ = "zjt"

import os,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR )

from core.models import Teacher
from core.models import Student
from core.models import Classes
from conf import settings
from core.user import load_user,dump_user
from core import auth

@auth.auth2
def show_menu():
    menu = '''
        ------ 教师菜单 ------
           0. 教师账号注册
           1. 查看班级信息
           2. 查看学生信息
           3. 设置学生分数
           4. 退出
        '''

    menu_dic = {
        "0":register,
        "1": class_info,
        "2": student_info,
        "3": set_student_score,
		"4": exit
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
    db_path = os.path.join(settings.ACCOUNTS_DB_DIR,'teachers')
    #print(db_path)
    exit_flag = False
    while not exit_flag :
        print("教师账号注册".center(50,"="))
        #username == student.name
        username = input("请输入您要注册的用户名【用户名必须为真实姓名】：").strip()
        if username in os.listdir(db_path):
            print("该用户名已注册，不能重新注册！")
            return False
        else:

            teacher_list= Teacher.get_all_obj_list()
            #print(student_list)
            for obj in teacher_list :
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
                                    "teacher_nid" : obj['nid']
                                            }
                    dump_user(userdata,db_path )
                    print('\033[31;1m教师[%s] 注册成功！\033[0m'%username)
                    return True
            else:
                print("教师[%s] 不存在，无法注册！请联系管理员创建 教师[%s]！"%(username,username))
                    # exit_flag = True
                return False

def class_info():
    """
    查看班级信息
    """
    #db_path = settings.SCHOOL_DB_DIR
    for obj in Classes.get_all_obj_list():
        print('\033[33;1m[%s] [%s]校区 班级[%s] 教师[%s] \033[0m'\
              %(obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['name'],\
                obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'],\
                obj['name'],obj['course_to_teacher_list']['teacher_nid'].get_obj_by_uuid(settings.TEACHER_DB_DIR)['name']))

def student_info():
    """
    查看学生信息
    """
    for obj in Student.get_all_obj_list():
        # print(type(obj['classes_nid']))
        # print(obj['classes_nid'].get_obj_by_uuid()['school_nid'].get_obj_by_uuid()['name'])
        print('\033[33;1m学生 名字[%s] 年龄[%s] qq[%s] [%s] [%s]校区 班级[%s] \033[0m'\
              % (obj['name'],obj['age'],obj['qq'],\
                 obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['name'],\
                 obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'],\
                 obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['name']))


def set_student_score():
    """
    设置学生分数
    """
    student_list = Student.get_all_obj_list()
    for k,obj in enumerate(student_list):
        # print(type(obj['classes_nid']))
        # print(obj['classes_nid'].get_obj_by_uuid()['school_nid'].get_obj_by_uuid()['name'])
        print('\033[33;1m %s 学生 名字[%s] 年龄[%s] qq[%s] [%s] [%s]校区 班级[%s] \033[0m'\
              % (k,obj['name'],obj['age'],obj['qq'],\
                 obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['name'],\
                 obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'],\
                 obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['name']))
    id=int(input('请选择学生: '))
    student_obj = student_list[id]
    #print(student_obj)
    score = input('班级[%s] 学生[%s] 设置分数：'%(student_obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['name'],student_obj['name']))
    course_to_teacher_nid = student_obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['course_to_teacher_list']['nid']
    student_obj['score'].set(course_to_teacher_nid,score)
    # print(student_obj['score'])
    # print(student_obj['score'].nid)
    # print(student_obj['score'].score_dict)
    # print(student_obj['score'].data)
    student_obj['score'].save()

if __name__ == '__main__':
    show_menu()
