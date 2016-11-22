#encoding:utf-8

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

#import os
#import sys
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func, Float
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    ID              = Column(Integer, primary_key = True, nullable = False, autoincrement = True)
    Name            = Column(CHAR(35), nullable = False)
    Age             = Column(Integer, nullable = False, default = 25)
    MajorCode       = Column(String(10), nullable = True, default = None)
    stID            = Column(CHAR(35))

class Major(Base):
    __tablename__ = 'majors'

    ID              = Column(Integer, primary_key = True, nullable = False, autoincrement = True)
    Code            = Column(String(10), nullable = False)
    Name            = Column(String(45), nullable = False)
    Description     = Column(String(45), nullable = False, default = None)

class Course(Base):
    __tablename__ = 'courses'
    ############
    Code            = Column(String(20), primary_key = True, nullable = False, unique = True)
    Name            = Column(String(100), nullable = False)

class Score(Base):
    __tablename__ = 'scores'

    ID = Column(Integer, primary_key = True, nullable = False, autoincrement = True)
    #######
    StudentID = Column(CHAR(30), nullable = False)
    CourseCode = Column(CHAR(30), nullable = False)
    Score = Column(Float, nullable = False, default = 0)
