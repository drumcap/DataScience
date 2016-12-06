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

    Link = Column(CHAR(200), primary_key = True, nullable = False)
    Name = Column(CHAR(200), nullable = False)
    Category = Column(CHAR(50), nullable = False)
    Enrolltime = Column(Date, nullable = True)


class Comment(Base):
    __tablename__ = 'comments'

    Id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    Link = Column(CHAR(200), nullable = False)
    Writer = Column(CHAR(50), nullable = False)
    Grade = Column(Integer, nullable = False)
    Enrolltime = Column(Date, nullable = True)


class Blank(Base):
    __tablename__ = 'blanks'

    Id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    Link = Column(CHAR(200), nullable = False)
    Writer = Column(CHAR(50), nullable = False)
