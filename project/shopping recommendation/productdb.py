# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from connection import Session
from model import Product
import datetime
import re

crawltime_1 = datetime.datetime.now()
crawltime = re.sub(r'\.\d+', '', crawltime_1.isoformat())


class ProductDB(object):
    def __init__(self):
        pass

    def save_product_info(self, link, title, category):
        if self.get_product_id(link):
            session = Session()
            insert_product = Product(Link = link, Name = title, Category = category, Enrolltime = crawltime)
            session.add(insert_product)
            session.commit()
            session.close()
        else:
            self.update_product_info(link, title, category)


    def update_product_info(self, link, title, category):
        session = Session()
        update_product = session.query(Product).filter(Product.Link == link).one()
        if update_product.Name != title:
            update_product.Name = title
            update_product.Category = category
            update_product.Enrolltime = crawltime
            session.commit()
        session.close()


    def get_product_id(self, link):
        session = Session()
        find_product = session.query(Product).filter(Product.Link == link).all()

        if find_product:
            return False

        else:
            return True

        session.close()


    def get_product_link(self):
        session = Session()
        find_product_link = session.query(Product).all()

        result = [row.Link for row in find_product_link]

        return result
