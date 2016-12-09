# -*-coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session, Mongo
from model import Comment
from traintestdb import TrainTestDB
from sqlalchemy import distinct

class GradeDB(object):
    def __init__(self):
        self.traintestdb = TrainTestDB()
        self.product_train, self.product_test = self.traintestdb.product_train_test_set()

        self.blank_comment_set = self.traintestdb.get_blank_test_set()


    def save_uservector(self, traintestcategory, blank = True):
        session = Session()
        user_vector = {}

        if traintestcategory == 'train':
            product_zip = self.product_train

        elif traintestcategory=='test':
            product_zip = self.product_test

        for traintestlink in product_zip:
            grades_list = session.query(Comment).filter(Comment.ProductNo == traintestlink.ProductNo).all()

            for user_grade in grades_list:
                if blank == True:
                    if (user_grade.ProductNo, user_grade.Writer) in self.blank_comment_set:
                        continue

                user = user_grade.Writer
                if not user in user_vector.keys():
                    grade_dict = {}
                    grade_dict[str(user_grade.ProductNo)] = int(user_grade.Grade)
                    user_vector[user] = grade_dict
                else:
                    user_vector[user][str(user_grade.ProductNo)] = int(user_grade.Grade)

        session.close()

        Mongo.vector.insert_one({'cat' : 'user', 'cat2' : traintestcategory, 'blank' : blank, 'vector': user_vector})
        print "saved"

    def save_itemvector(self):
        session = Session()
        item_vector = {}

        grades_list = session.query(Comment).all()

        for user_grade in grades_list:
            if (user_grade.ProductNo, user_grade.Writer) in self.blank_comment_set:
                continue

            item = str(user_grade.ProductNo)
            if not item in item_vector.keys():
                grade_dict = {}
                grade_dict[user_grade.Writer] = int(user_grade.Grade)
                item_vector[item] = grade_dict
            else:
                item_vector[item][user_grade.Writer] = int(user_grade.Grade)

        session.close()
        Mongo.vector.insert_one({'cat' : 'item', 'vector': item_vector})
        print "saved"

    def get_itemvector(self):
        result = Mongo.vector.find_one({"cat" : 'item'})['vector']
        return result

    def get_uservector(self, traintestcategory, blank):
        result = Mongo.vector.find_one({'cat' : 'user', 'cat2' : traintestcategory, 'blank' : blank})['vector']
        return result

    def delete_vector(self):
        Mongo.vector.drop()
        print "deleted"

    def get_user_list(self):
        session = Session()
        user_list = []
        for users in  session.query(distinct(Comment.Writer)).all():
            user_list.append(users[0])
        return user_list
