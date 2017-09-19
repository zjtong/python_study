#_*_coding:utf-8_*_
__author__ = 'Linhaifeng'
import time
import pickle
import os,sys

BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR )
from conf import settings
from core import identifer


class BaseModel:
    def save(self):
        file_path=os.path.join(self.db_path,str(self.nid))
        with open(file_path,'wb') as f:
            #print(self.data)
            pickle.dump(self.data,f)

    @classmethod
    def get_all_obj_list(cls):
        ret=[]
        for filename in os.listdir(cls.db_path):
            file_path=os.path.join(cls.db_path,filename)
            with open(file_path, 'rb') as f:
                item = pickle.loads(f.read())
            ret.append(item)
        return ret


class School(BaseModel):
    db_path=settings.SCHOOL_DB_DIR
    def __init__(self,name,addr):
        self.nid=identifer.SchoolNid(self.db_path)
        self.name=name
        self.addr=addr
        self.create_time=time.strftime('%Y-%m-%d %X')
        self.data = {'nid':self.nid,'name':self.name,'addr':self.addr,'create_time':self.create_time }
        self.__income=0

    def __str__(self):
        return self.name

class Teacher(BaseModel):
    db_path=settings.TEACHER_DB_DIR
    def __init__(self,name,level):
        self.nid=identifer.TeacherNid(self.db_path)
        self.name=name
        self.level=level
        self.__account=0
        self.create_time=time.strftime('%Y-%m-%d %X')
        self.data = {'nid': self.nid, 'name': self.name, 'level': self.level, 'create_time': self.create_time}

class Course(BaseModel):
    db_path=settings.COURSE_DB_DIR
    def __init__(self,name,price,period,school_nid):
        self.nid=identifer.CourseNid(self.db_path)
        self.name=name
        self.price=price
        self.period=period
        self.school_nid=school_nid
        self.data = {'nid': self.nid, 'name': self.name, 'price': self.price, 'period': self.period,'school_nid':self.school_nid }

class Course_to_teacher(BaseModel):
    db_path=settings.COURSE_TO_TEACHER_DB_DIR
    def __init__(self,course_nid,school_nid,teacher_nid):
        self.nid=identifer.Course_to_teacherNid(self.db_path)
        self.course_nid=course_nid
        self.school_nid=school_nid
        self.teacher_nid=teacher_nid
        self.data = {'nid': self.nid,'teacher_nid':self.teacher_nid, 'course_nid': self.course_nid, 'school_nid': self.school_nid }

    def get_course_to_teacher_list(self):
        ret=self.get_all_obj_list()
        if ret:
            return [ret['course_nid'].get_obj_by_uuid(),ret['classes_nid'].get_obj_by_uuid()]
        return [None,None]

class Classes(BaseModel):
    db_path=settings.CLASSES_DB_DIR
    def __init__(self,name,school_nid,course_to_teacher_list):
        self.nid=identifer.ClassesNid(self.db_path)
        self.name=name
        self.school_nid=school_nid
        self.course_to_teacher_list=course_to_teacher_list
        self.data = {'nid': self.nid,'name':self.name,'school_nid': self.school_nid,\
                     'course_to_teacher_list':self.course_to_teacher_list }

class Student(BaseModel):
    db_path=settings.STUDENT_DB_DIR
    def __init__(self,name,age,qq,classes_nid):
        self.nid=identifer.StudentNid(self.db_path)
        self.name=name
        self.age=age
        self.qq=qq
        self.classes_nid=classes_nid
        self.score=Score(self.nid)  #Scored 的 nid == Student 的 nid
        self.data = {'nid': self.nid, 'name': self.name, 'age': self.age,'qq': self.qq,\
                     'classes_nid': self.classes_nid, \
                     'score': self.score}

class Score(BaseModel ):
    db_path=settings.SCORE_DB_DIR

    def __init__(self,nid):
        self.nid=nid
        self.score_dict={}
        # self.db_path = settings.SCORE_DB_DIR
        self.data = {'nid': self.nid,'score_dict':self.score_dict}

    def set(self,course_to_teacher_nid,number):
        self.score_dict['score']=number
        self.score_dict['course_to_teacher_nid']=course_to_teacher_nid


    def get(self,course_to_teacher_nid):
        return self.score_dict.get(course_to_teacher_nid)

    # def save(self):
    #     file_path=os.path.join(settings.SCORE_DB_DIR,str(self.nid))
    #     with open(file_path,'wb') as f:
    #         data = {'nid': self.nid,'score_dict':self.score_dict}
	#
    #         pickle.dump(data,f)