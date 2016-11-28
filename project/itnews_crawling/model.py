#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'newsarticles'

    Link            = Column(CHAR(200), primary_key = True, nullable = False)
    Title           = Column(CHAR(200), nullable = False)
    Content         = Column(TEXT, nullable = False)
    NewsCompany     = Column(CHAR(50), nullable = True)
    ReporterEmail   = Column(CHAR(50), nullable = True)
    ReportDate      = Column(Date, nullable = True)


class CommentList(Base):
    __tablename__ = 'commentlists'

    Id              = Column(Integer, primary_key = True, nullable = False)
    Link            = Column(CHAR(200), nullable = False)
    Mcontent        = Column(TEXT, nullable = True)
    User            = Column(CHAR(50), nullable = False)
    Sympathy        = Column(Integer, nullable = True)
    Antipathy       = Column(Integer, nullable = True)
    Enrolltime      = Column(Date, nullable = True)
