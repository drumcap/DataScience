# -*-coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import ImvelyComment, ImvelyCosineSimilarity
import datetime
import re

crawltime_1 = datetime.datetime.now()
crawltime = re.sub(r'\.\d+', '', crawltime_1.isoformat())

class CommentDB(object):
    def __init__(self):
        pass

    def save_comment_info(self, product_link, comment_writer, comment_grade):
        if self.get_comment_info(product_link, comment_writer):
            session = Session()
            insert_comment = ImvelyComment(Link = product_link, Writer = comment_writer, Grade = comment_grade, Enrolltime = crawltime)
            session.add(insert_comment)
            session.commit()
            session.close()
        else:
            self.update_comment_info(product_link, comment_writer, comment_grade)

    def update_comment_info(self, product_link, comment_writer, comment_grade):
        session = Session()
        update_comment = session.query(ImvelyComment).filter(ImvelyComment.Link == product_link, ImvelyComment.Writer == comment_writer).one()
        if update_comment.Grade != comment_grade:
            update_comment.Grade = comment_grade
            update_comment.Enrolltime = crawltime
            session.commit()
        session.close()


    def get_comment_info(self, product_link, comment_writer):
        session = Session()
        find_comment = session.query(ImvelyComment).filter(ImvelyComment.Link == product_link, ImvelyComment.Writer == comment_writer).all()

        if find_comment:
            return False

        else:
            return True

        session.close()
