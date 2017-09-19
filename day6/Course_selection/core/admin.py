# -*- coding: utf-8 -*-
__author__ = "zjt"

import os,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR )
# print(BASE_DIR)

from core.models import School
from core.models import Teacher
from core.models import Student
from core.models import Course
from core.models import Course_to_teacher
from core.models import Classes
from conf import settings
from core.user import load_user,dump_user
from core import auth


def create_school():
    try:
        name=input('请输入学校名字: ').strip()
        addr=input('请输入学校地址: ').strip()
        school_name_list=[(obj['name'],obj['addr']) for obj in School.get_all_obj_list()]
        if (name,addr) in school_name_list:
            raise Exception('\033[43;1m[%s] [%s]校区 已经存在,不可重复创建\033[0m' %(name,addr))
        obj=School(name,addr)
        obj.save()
        status=True
        error=''
        data='\033[33;1m[%s] [%s]校区 创建成功\033[0m' %(obj.name,obj.addr)
        print(data)
    except Exception as e:
        status=False
        error=str(e)
        print('error: %s'%error)
        data=''
    return {'status':status,'error':error,'data':data}

def show_school():
    for obj in School.get_all_obj_list():
        print('\033[45;1m学校[%s] 地址[%s] 创建日期[%s]\033[0m'.center(60,'-') \
              %(obj['name'],obj['addr'],obj['create_time']))

def create_teacher():
    try:
        name=input('请输入老师姓名: ').strip()
        level=input('请输入老师级别: ').strip()
        teacher_name_list=[obj['name'] for obj in Teacher.get_all_obj_list()]
        if name in teacher_name_list:
            raise Exception('\033[43;1m老师[%s] 已经存在,不可重复创建\033[0m' %(name))
        obj=Teacher(name,level)
        obj.save()
        status=True
        error=''
        data='\033[33;1m老师[%s] 级别[%s] 时间[%s]创建成功\033[0m' %(obj.name,obj.level,obj.create_time)
        print(data)
    except Exception as e:
        status=False
        error=str(e)
        print('error: %s'%error)
        data=''
    return {'status':status,'error':error,'data':data}

def show_teacher():
    for obj in Teacher.get_all_obj_list():
        #print(obj)
        print('\033[33;1m老师[%s] 级别[%s] 创建时间[%s]\033[0m'.center(60,'-') \
              %(obj['name'],obj['level'],obj['create_time']))

def create_course():
    try:
        print('创建课程'.center(60,'='))
        school_list=School.get_all_obj_list()
        for k,obj in enumerate(school_list):
            print(k,obj['name'],obj['addr'])
        id=int(input('请选择学校: '))
        school_obj=school_list[id]
        #print(school_obj,school_obj ['nid'] )

        name=input('请输入课程名: ').strip()
        price=input('请输入课程价格: ').strip()
        period=input('请输入课程周期: ').strip()

        course_name_list=[(obj['name'],obj['school_nid']) for obj in Course.get_all_obj_list()]
        if name in course_name_list:
            raise Exception('\033[43;1m课程[%s] 已经存在,不可重复创建\033[0m' %(name))
        obj=Course(name,price,period,school_obj['nid'])
        obj.save()
        status=True
        error=''
        data='\033[33;1m课程[%s] 价格[%s] 周期[%s]创建成功\033[0m' %(obj.name,obj.price,obj.period)
        print(data)
    except Exception as e:
        status=False
        error=str(e)
        print('error: %s'%error)
        data=''
    return {'status':status,'error':error,'data':data}

def show_course():
    for obj in Course.get_all_obj_list():
        # print(obj)

        print('\033[33;1m[%s] [%s]校区 [%s]课程 价格[%s] 周期[%s]\033[0m'.center(60,'-') \
			  %(obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['name'],obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'],\
				obj['name'],obj['price'],obj['period']))

def create_course_to_teacher():
    try:
        print('关联教师与课程'.center(60,'='))
        teacher_list=Teacher.get_all_obj_list()
        for k,obj in enumerate(teacher_list):
            print('%s 老师[%s] 级别[%s]'%(k,obj['name'],obj['level']))
        id=int(input('请选择教师: '))
        teacher_obj=teacher_list[id]
        #print(teacher_obj,teacher_obj['nid'] )

        course_list = Course.get_all_obj_list()
        for k, obj in enumerate(course_list):
            print('%s [%s][%s]校区 [%s]课程 价格[%s] 周期[%s]'.center(60, '-') \
				  % (k,obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR )['name'],\
                     obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'], \
					 obj['name'], obj['price'], obj['period']))
        id = int(input('请选择课程: '))
        course_obj = course_list[id]
        #print(course_obj )
        obj = Course_to_teacher(course_obj ['nid'],course_obj ['school_nid'],teacher_obj['nid'])

        obj.save()
        status = True
        error = ''
        data = '\033[33;1m[%s][%s]校区 [%s]课程 关联 教师[%s] 关联成功\033[0m' %(obj.school_nid.get_obj_by_uuid(settings.SCHOOL_DB_DIR )['name'],\
                                                                     obj.school_nid.get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'],\
                                                                    course_obj['name'],teacher_obj['name'])
        print(data)

    except Exception as e:
        status=False
        error=str(e)
        print('error: %s'%error)
        data=''
    return {'status':status,'error':error,'data':data}

def create_classes():
    try:
        print('创建班级'.center(60, '='))
        course_to_teacher_list = Course_to_teacher.get_all_obj_list()
        #print(course_to_teacher_list)
        for k, obj in enumerate(course_to_teacher_list):
            # print(k,obj['school_nid'].get_obj_by_uuid()['name'])
            print('%s [%s][%s]校区 [%s]课程  [%s]教师'% (k, obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR )['name'],\
                                                     obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'],\
                                                     obj['course_nid'].get_obj_by_uuid(settings.COURSE_DB_DIR )['name'],\
                                                     obj['teacher_nid'].get_obj_by_uuid(settings.TEACHER_DB_DIR)['name']))
        id = int(input('请选择要创建班级的课程: '))
        choice_course_to_teacher_list= course_to_teacher_list[id]
        #print(choice_course_to_teacher_list )

        name = input("请输入班级名称：").strip()
        obj = Classes(name,choice_course_to_teacher_list['school_nid'],choice_course_to_teacher_list)

        obj.save()
        #print(obj)
        status = True
        error = ''
        data = '\033[33;1m[%s][%s]校区 班级[%s] 创建成功\033[0m' %(obj.school_nid.get_obj_by_uuid(settings.SCHOOL_DB_DIR )['name'], \
                                                           obj.school_nid.get_obj_by_uuid(settings.SCHOOL_DB_DIR )['addr'],obj.name)
        #print(data)
    except Exception as e:
        status = False
        error = str(e)
        print('error: %s'%error)
        data = ''
    return {'status': status, 'error': error, 'data': data}

def show_classes():
    for obj in Classes.get_all_obj_list():
        # print(obj)

        print('\033[33;1m[%s] [%s]校区 班级[%s] \033[0m'% (obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['name'],\
                                                       obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR)['addr'],obj['name']))

def create_student():
    try:
        name=input('请输入学生姓名: ').strip()
        age=input('请输入学生年龄: ').strip()
        qq = input('请输入学生qq号码: ').strip()
        student_name_list=[obj['name'] for obj in Student.get_all_obj_list()]
        if name in student_name_list:
            raise Exception('\033[43;1m学生[%s] 已经存在,不可重复创建\033[0m' %(name))
        classes_list = Classes.get_all_obj_list()
        for k, obj in enumerate(classes_list):
            print('%s [%s][%s]校区 班级[%s]'.center(60, '-') \
                  % (k, obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR )['name'],\
                     obj['school_nid'].get_obj_by_uuid(settings.SCHOOL_DB_DIR )['addr'], \
                     obj['name']))
        id = int(input('请选择班级: '))
        class_obj= classes_list[id]
        obj=Student(name,age,qq,class_obj['nid'])
        obj.save()
        status=True
        error=''
        data='\033[33;1m学生 名字[%s] 年龄[%s] qq[%s] 班级[%s] 创建成功\033[0m' \
             %(obj.name,obj.age,obj.qq,obj.classes_nid.get_obj_by_uuid(settings.CLASSES_DB_DIR )['name'])
        print(data)
    except Exception as e:
        status=False
        error=str(e)
        print('error: %s'%error)
        data=''
    return {'status':status,'error':error,'data':data}

def show_student():
    for obj in Student.get_all_obj_list():
        print('\033[33;1m学生 名字[%s] 年龄[%s] qq[%s] 班级[%s] \033[0m'\
              % (obj['name'],obj['age'],obj['qq'],\
                 obj['classes_nid'].get_obj_by_uuid(settings.CLASSES_DB_DIR)['name']))

def admin_register():
    db_path = os.path.join(settings.ACCOUNTS_DB_DIR,'admins')
    exit_flag = False
    while not exit_flag :
        print("创建管理员".center(50,"="))
        #username == student.name
        username = input("请输入您要管理员的用户名：").strip()
        if username in os.listdir(db_path):
            print("该用户名已注册，不能重新注册！")
            return False
        else:
                password = input("请输入密码：").strip()
                re_password = input('再次确认密码：').strip()
                if password != re_password:
                    print('\033[31;1m两次输入的密码不一致!\033[0m')
                    continue
                userdata = {
                                "username" : username,
                                "password" : password,
                                'locked' : False,
                                'authority': True,

                                        }
                dump_user(userdata,db_path)
                print('\033[31;1m管理员[%s] 注册成功！\033[0m'%username)
                return True

@auth.auth3
def main():
    menu = '''
	--------管理员菜单-------
	        0:创建管理员账户
	        1:创建学校
	        2:查看学校
	        3:创建老师
	        4:查看老师
	        5:创建课程
	        6:查看课程
	        7:关联老师与课程
	        8:创建班级
	        9:查看班级
	        10:创建学生
	        11:查看学生
	        12:退出
	    '''

    menu_dic={
        '0':admin_register,
        '1':create_school,
        '2':show_school,
        '3':create_teacher,
        '4':show_teacher,
        '5':create_course,
        '6':show_course,
        '7':create_course_to_teacher,
        '8':create_classes,
        '9':show_classes,
        '10':create_student,
        '11':show_student,
        '12':exit
    }

    while True:
        print(menu)
        choice = input("\033[32;1m请选择(‘b':返回上一级>>>:\033[0m").strip().lower()
        if choice in menu_dic:

            menu_dic[choice]()
            # if re['status'] == True:
            #     print(re['data'])
        elif choice == "b":
            break
        else:
            print('\033[31;1m输入错误!请重新输入...\033[0m')


if __name__ == '__main__':
    main()



