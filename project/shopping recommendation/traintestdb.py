# -*-coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import Comment, Product, Blank
import random
from sqlalchemy import distinct

class TrainTestDB(object):
    def __init__(self):
        self.product_train = None
        self.product_test = None

    def product_train_test_set(self):
        session = Session()

        product_num_1 = session.query(Product).all()
        product_num = len(product_num_1)
        product_train_num = int(0.9 * product_num)
        product_test_num = product_num - product_train_num

        self.product_train = session.query(Product).order_by(Product.Enrolltime, Product.Link).slice(0, product_train_num).all()
        self.product_test  = session.query(Product).order_by(Product.Enrolltime, Product.Link).slice(product_train_num, product_num+1).all()
        session.close()

        return self.product_train, self.product_test

    def make_blank_test_set(self):

        self.product_train_test_set()
        session = Session()
        session.query(Blank).delete()

        for test_link in self.product_test:
            grades_list = session.query(Comment).filter(Comment.Link == test_link.Link).all()
            blank_comment_num = random.sample(range(len(grades_list)), 1)
            print grades_list[blank_comment_num[0]].Link, grades_list[blank_comment_num[0]].Writer

            insert_blank_index = Blank(Link = grades_list[blank_comment_num[0]].Link, Writer = grades_list[blank_comment_num[0]].Writer)
            session.add(insert_blank_index)
            session.commit()

        session.close()

    def get_blank_test_set(self):
        blank_comment_link = []
        blank_comment_writer = []
        blank_comment_set = []

        session = Session()
        blank_zip = session.query(Blank).all()
        if blank_zip:
            for blank_comment in blank_zip:
                blank_comment_set.append((blank_comment.Link, blank_comment.Writer))
        session.close()

        return blank_comment_set


    def get_user_list(self):
        session = Session()
        user_list = session.query(distinct(Comment.Writer)).all()
        return user_list
