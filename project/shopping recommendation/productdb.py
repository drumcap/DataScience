# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from connection import Session
from model import Product
import datetime
import re

#Make crawltime
crawltime_1 = datetime.datetime.now()
crawltime = re.sub(r'\.\d+', '', crawltime_1.isoformat())


class ProductDB(object):
    def __init__(self):
        pass

    def save_product_info(self, productno, link, title, category):
        if self.get_product_id(productno):
            session = Session()
            insert_product = Product(ProductNo = productno,
                                     Link = link,
                                     Name = title,
                                     Category = category,
                                     TrainTest = 'train' ,
                                     Enrolltime = crawltime)
            session.add(insert_product)
            session.commit()
            session.close()
        else:
            self.update_product_info(productno, link, title, category)

    #If there is same product, update it.
    def update_product_info(self, productno, link, title, category):
        session = Session()
        update_product = session.query(Product)\
                                .filter(Product.ProductNo == productno)\
                                .one()
        if update_product.Name != title:
            update_product.Name = title
            update_product.Link = link
            update_product.Category = category
            update_product.TrainTest = 'train'          #all of them is 'train'
            update_product.Enrolltime = crawltime
            session.commit()
        session.close()

    #Find same product.
    def get_product_id(self, productno):
        session = Session()
        find_product = session.query(Product)\
                              .filter(Product.ProductNo == productno)\
                              .all()

        if find_product:
            return False

        else:
            return True

        session.close()

    #It is used in comment_crawler.py to get comments at each product.
    def get_product_link(self):
        session = Session()
        find_product_link = session.query(Product).all()

        result = [(row.Link, row.ProductNo) for row in find_product_link]

        return result
