# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func, Float
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    ProductNo = Column(CHAR(50), primary_key = True, nullable = False)
    Link = Column(CHAR(200),  nullable = False)
    Name = Column(CHAR(200), nullable = False)
    Category = Column(CHAR(50), nullable = False)
    Enrolltime = Column(Date, nullable = True)
    TrainTest = Column(CHAR(50), nullable = False)
    Review = Column(Integer, nullable = True)

class Comment(Base):
    __tablename__ = 'comments'

    Id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    ProductNo = Column(CHAR(50), nullable = False)
    Writer = Column(CHAR(50), nullable = False)
    Grade = Column(Integer, nullable = False)
    Enrolltime = Column(Date, nullable = True)

class User(Base):
    __tablename__ = 'users'

    UserId = Column(CHAR(50), primary_key = True, nullable = False)
    TrainTest = Column(CHAR(50), nullable = False)
    Written = Column(Integer, nullable = True)
