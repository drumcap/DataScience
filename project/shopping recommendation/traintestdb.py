# -*-coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import Comment, Product, User
import random
from sqlalchemy import distinct, func

class TrainTestDB(object):
    def __init__(self):
        pass

    def product_train_test_set(self):
        session = Session()

        product_num = session.query(Product).count()
        product_train_num = int(0.95 * int(product_num))
        product_test_num = product_num - product_train_num

        product_train_list = session.query(Product).order_by(Product.Enrolltime, Product.ProductNo).slice(0, product_train_num).all()
        for product_train in product_train_list:
            update_tt = session.query(Product).filter(Product.ProductNo == product_train.ProductNo).one()
            update_tt.TrainTest = 'train'
            session.commit()

        product_test_list  = session.query(Product).order_by(Product.Enrolltime, Product.ProductNo).slice(product_train_num, product_num+1).all()
        for product_test in product_test_list:
            update_tt = session.query(Product).filter(Product.ProductNo == product_test.ProductNo).one()
            update_tt.TrainTest = 'test'
            session.commit()
        session.close()

        print 'updated product'

    def user_train_test_set(self):
        session = Session()
        reset_tt = session.query(User).filter(User.TrainTest == 'test').all()
        if reset_tt:
            for row in reset_tt:
                row.TrainTest = 'train'
                session.commit()
        print 'reset'
        user_num = session.query(User).count()
        user_test_num = int(0.05 * int(user_num))
        print user_test_num

        for row in session.query(User).order_by(func.rand()).limit(user_test_num):
            print row.UserId
            row.TrainTest = 'test'
            session.commit()
        session.close()
        print 'updated user'

    def get_item_list(self, tt):
        session = Session()
        item_list = []
        result = session.query(Product).filter(Product.TrainTest == tt).all()
        for row in result:
            item_list.append(row.ProductNo)
        session.close()
        return item_list

    def get_user_list(self, tt):
        session = Session()
        user_list = []
        result = session.query(User).filter(User.TrainTest == tt).all()
        for row in result:
            user_list.append(row.UserId)
        session.close()
        return user_list

    def get_blank_set(self, value):
        print 'find blank set'
        blank_set = []
        blank_count = 0
        session = Session()
        result = session.query(Comment).join(Product, Product.ProductNo == Comment.ProductNo).join(User, User.UserId == Comment.Writer).filter(User.TrainTest == 'test', Product.TrainTest == 'test').all()
        if result:
            for row in result:
                blank_set.append((row.ProductNo, row.Writer, row.Grade))
                blank_count += 1
                print 'item is {}, user is {} counting {}'.format(row.ProductNo, row.Writer, blank_count)
        if value:
            return blank_count
        else:
            return blank_set
