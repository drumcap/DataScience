# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import requests
from bs4 import BeautifulSoup
import re
import time
import random
from productdb import ProductDB
from commentdb import CommentDB
from sortcommentdb import SortCommentDB

class CrawlComment(object):
    def __init__(self, productdb, commentdb, sortcommentdb):
        self.productdb = productdb
        self.commentdb = commentdb
        self.sortcommentdb = sortcommentdb
        self.product_links = self.productdb.get_product_link()

    def crawl_products_comments(self):
        for product_link in self.product_links:
            self.crawl_product_comments(product_link[0],product_link[1],
                                        pagenum=1)


    def crawl_product_comments(self, product_link, productno, pagenum):

        product_code_1 = re.search(r'product_no=\d+', product_link)
        product_code_2 = re.search(r'\d+', product_code_1.group(0))
        product_code = product_code_2.group(0)

        #Comments is in wideturl.
        widget_url = 'http://widgets1.cre.ma/imvely.com/products/reviews?\
                      app=0&iframe_id=crema-product-reviews-2&order=20&\
                      page={}&parent_url={}&product_code={}'\
                      .format(pagenum, product_link, product_code)
        print widget_url

        #Use timesleep to access without any problems.
        sec = random.random()
        time.sleep(sec)

        response = requests.get(widget_url)
        soup = BeautifulSoup(response.content)
        try:
            body = soup.find('div', attrs = {'class' : 'widget widget-reviews \
                                                        pagination-list '})
            comment_lists = body.find('ul', attrs = {'class' : 'reviews \
                                                      reviews-product'})
            comment_list = comment_lists.select('> li')

            if comment_list:
                for com in comment_list:
                    com_div = com.find('div', attrs = {'class' :
                                                      'review-content-summary'})

                    com_writer_1 = com_div.find('div', attrs = {'class' :
                                                                'col author'})
                    com_writer = str(com_writer_1.get_text())

                    com_grade_1 = com_div.find('div', attrs = {'class' :
                                                               'col score'})
                    com_grade_2 = com_grade_1.find('div',
                                    attrs = {'class' : 'star-rating-container'})
                    com_grade_3 = com_grade_2.find_all('span',
                                    attrs = {'class' : 'sprites-star-full'})
                    com_grade = 0
                    #Grade is the number of special class.
                    for grade in com_grade_3:
                        com_grade += 1

                    print com_writer, com_grade
                    try:
                        self.commentdb.save_comment_info(productno,
                                                         com_writer, com_grade)
                    except Exception as e:
                        print e

                pagenum += 1
                #Recursive function
                self.crawl_product_comments(product_link, productno, pagenum)

        except Exception as e:
            print e

    #Count reviews per product and per user.
    def sort_count(self):
        self.sortcommentdb.sort_count()
        self.sortcommentdb.make_user_list()

if __name__ == '__main__':
    productdb = ProductDB()
    commentdb = CommentDB()
    sortcommentdb = SortCommentDB()

    result = CrawlComment(productdb, commentdb, sortcommentdb)
    result.crawl_products_comments()
    result.sort_count()
