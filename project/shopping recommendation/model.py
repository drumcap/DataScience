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

class ImvelyProduct(Base):
    __tablename__ = 'imvelyproducts2'

    Link = Column(CHAR(200), primary_key = True, nullable = False)
    Name = Column(CHAR(200), nullable = False)
    Category = Column(CHAR(50), nullable = False)
    Enrolltime = Column(Date, nullable = True)


class ImvelyComment(Base):
    __tablename__ = 'imvelycomments2'

    Id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    Link = Column(CHAR(200), nullable = False)
    Writer = Column(CHAR(50), nullable = False)
    Grade = Column(Integer, nullable = False)
    Enrolltime = Column(Date, nullable = True)


class ImvelyBlankComment(Base):
    __tablename__ = 'imvelyblankcomments2'

    Id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    Link = Column(CHAR(200), nullable = False)
    Writer = Column(CHAR(50), nullable = False)
