# -*-coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import Comment, Product, User
from sqlalchemy import func


class SortCommentDB(object):
    def __init__(self):
        pass

    #Count the number of comments per item.
    def sort_count(self):
        session = Session()
        product_list = session.query(Product).all()
        for product in product_list:
            find_count = session.query(Comment)\
                                .filter(Comment.ProductNo == product.ProductNo)\
                                .count()
            print find_count
            update_product = session.query(Product)\
                            .filter(Product.ProductNo == product.ProductNo)\
                            .one()
            update_product.Review = int(find_count)
            session.commit()
        session.close()

    def make_user_list(self):
        session = Session()
        for row in session.query(Comment.Writer, func.count(Comment.Id))\
                          .group_by(Comment.Writer)\
                          .all():
            if not self.get_userid(row[0]):
                insert_user = User(UserId = row[0], TrainTest = 'train',
                                                        Written = int(row[1]))
                session.add(insert_user)
                session.commit()
                print row[0], 'train', row[1]
            else:
                self.update_user_list(row[0], int(row[1]))
        session.close()

    #Find user in User DB.
    def get_userid(self, userid):
        session = Session()
        if session.query(User).filter(User.UserId == userid).all():
            return True
        else:
            return False
        session.close()

    def update_user_list(self, userid, count):
        session = Session()
        update_user = session.query(User).filter(User.UserId == userid).one()
        update_user.Written = count
        update_user.TrainTest = 'train'                 #ALl of user is train.
        session.commit()
        session.close()
        print 'updated'
