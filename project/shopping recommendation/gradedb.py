# -*-coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session, Mongo
from model import Comment, Product
from traintestdb import TrainTestDB
from sqlalchemy import distinct

class GradeDB(object):
    def __init__(self):
        self.traintestdb = TrainTestDB()

    def save_uservector(self):
        session = Session()
        user_vector = {}
        grades_list = session.query(Comment).join(Product, Product.ProductNo == Comment.ProductNo).filter(Product.TrainTest == 'train').all()
        count = 0
        for user_grade in grades_list:
            count += 1
            user = user_grade.Writer
            if not user in user_vector.keys():
                grade_dict = {}
                grade_dict[str(user_grade.ProductNo)] = int(user_grade.Grade)
                user_vector[user] = grade_dict
            else:
                user_vector[user][str(user_grade.ProductNo)] = int(user_grade.Grade)
        if count % 10 == 0:
            print user_vector
        session.close()
        Mongo.vector.insert_one({'cat' : 'user', 'vector': user_vector})
        print "saved"

    def save_itemvector(self):
        user_list = self.traintestdb.get_user_list('train')
        session = Session()
        item_vector = {}
        grades_list = session.query(Comment).join(User, User.UserId == Comment.Writer).filter(User.TrainTest == 'train').all()
        count = 0

        for user_grade in grades_list:
            count += 1
            item = user_grade.ProductNo
            if not item in item_vector.keys():
                grade_dict = {}
                grade_dict[user_grade.Writer] = int(user_grade.Grade)
                item_vector[item] = grade_dict
            else:
                item_vector[item][user_grade.Writer] = int(user_grade.Grade)
        if count % 10 == 0:
            print item_vector
        session.close()
        Mongo.vector.insert_one({'cat' : 'item', 'vector': item_vector})
        print "saved"

    def delete_vector(self):
        Mongo.vector.drop()
        print "deleted"

    def get_vector(self, cat):
        result = Mongo.vector.find_one({'cat' : cat})['vector']
        return result
