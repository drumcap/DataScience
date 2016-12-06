# -*-coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import ImvelyComment, ImvelyProduct, ImvelyBlankComment
from traintestdb import TrainTestDB

class GradeDB(object):
    def __init__(self):
        self.traintestdb = TrainTestDB()
        self.product_train, self.product_test = self.traintestdb.product_train_test_set()

        self.blank_comment_set = self.traintestdb.get_blank_test_set()


    def get_uservector(self, traintestcategory, blank = True):
        session = Session()
        user_vector = {}

        if traintestcategory == 'train':
            product_zip = self.product_train

        elif traintestcategory=='test':
            product_zip = self.product_test

        for traintestlink in product_zip:
            grades_list = session.query(ImvelyComment).filter(ImvelyComment.Link == traintestlink.Link).all()

            for user_grade in grades_list:
                if blank == True:
                    if (user_grade.Link, user_grade.Writer) in self.blank_comment_set:
                        continue

                user = user_grade.Writer
                if not user in user_vector.keys():
                    grade_dict = {}
                    grade_dict[user_grade.Link] = user_grade.Grade
                    user_vector[user] = grade_dict
                else:
                    user_vector[user][user_grade.Link] = user_grade.Grade

        session.close()

        return user_vector

    def get_itemvector(self):
        session = Session()
        item_vector = {}

        grades_list = session.query(ImvelyComment).all()

        for user_grade in grades_list:
            if (user_grade.Link, user_grade.Writer) in self.blank_comment_set:
                continue

            item = user_grade.Link
            if not item in item_vector.keys():
                grade_dict = {}
                grade_dict[user_grade.Writer] = user_grade.Grade
                item_vector[item] = grade_dict
            else:
                item_vector[item][user_grade.Writer] = user_grade.Grade

        session.close()
        return item_vector
