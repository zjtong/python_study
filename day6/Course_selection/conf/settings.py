# -*- coding: utf-8 -*-
__author__ = "zjt"

import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR )
# print(BASE_DIR)
# print(sys.path)

ADMIN_DB_DIR=os.path.join(BASE_DIR,'db','admin')
SCHOOL_DB_DIR=os.path.join(BASE_DIR,'db','school')
TEACHER_DB_DIR=os.path.join(BASE_DIR,'db','teacher')
COURSE_DB_DIR=os.path.join(BASE_DIR,'db','course')
COURSE_TO_TEACHER_DB_DIR=os.path.join(BASE_DIR,'db','course_to_teacher')
CLASSES_DB_DIR=os.path.join(BASE_DIR,'db','classes')
STUDENT_DB_DIR=os.path.join(BASE_DIR,'db','student')
SCORE_DB_DIR=os.path.join(BASE_DIR,'db','score')
ACCOUNTS_DB_DIR = os.path.join(BASE_DIR,'db','accounts')

#print(CLASSES_DB_DIR)