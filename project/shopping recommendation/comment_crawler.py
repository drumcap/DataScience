# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import requests
from bs4 import BeautifulSoup
import re
from productdb import ProductDB
from commentdb import CommentDB


class CrawlComment(object):
    def __init__(self, productdb, commentdb):
        self.productdb = productdb
        self.commentdb = commentdb
        self.product_links = self.productdb.get_product_link()

    def crawl_products_comments(self):
        for product_link in self.product_links:
            self.crawl_product_comments(product_link, pagenum=1)


    def crawl_product_comments(self, product_link, pagenum):

        product_code_1 = re.search(r'product_no=\d+', product_link)
        product_code_2 = re.search(r'\d+', product_code_1.group(0))
        product_code = product_code_2.group(0)

        widget_url = 'http://widgets1.cre.ma/imvely.com/products/reviews?app=0&iframe_id=crema-product-reviews-2&order=20&page={}&parent_url={}&product_code={}'.format(pagenum, product_link, product_code)
        print widget_url

        response = requests.get(widget_url)
        soup = BeautifulSoup(response.content)
        try:
            body = soup.find('div', attrs = {'class' : 'widget widget-reviews pagination-list '})
            comment_lists = body.find('ul', attrs = {'class' : 'reviews reviews-product'})
            comment_list = comment_lists.select('> li')

            if comment_list:
                for comment in comment_list:
                    comment_div = comment.find('div', attrs = {'class' : 'review-content-summary'})

                    comment_writer_1 = comment_div.find('div', attrs = {'class' : 'col author'})
                    comment_writer = str(comment_writer_1.get_text())

                    comment_grade_1 = comment_div.find('div', attrs = {'class' : 'col score'})
                    comment_grade_2 = comment_grade_1.find('div', attrs = {'class' : 'star-rating-container'})
                    comment_grade_3 = comment_grade_2.find_all('span', attrs = {'class' : 'sprites-star-full'})
                    comment_grade = 0
                    for grade in comment_grade_3:
                        comment_grade += 1

                    print comment_writer, comment_grade
                    try:
                        self.commentdb.save_comment_info(product_link, comment_writer, comment_grade)
                    except Exception as e:
                        print e

                pagenum += 1
                self.crawl_product_comments(product_link, pagenum)

        except Exception as e:
            print e


            """
            comment_div_2 = comment.find('div', attrs = {'class' : 'review-content'})
            print comment
            comment_option_content = comment_div_2.find('div', attrs = {'class' : 'panel-body no-border'})
            comment_options = comment_option_content.find('div', attrs = {'class' : 'review-options review-options--online'})

            comment_option_list = comment_options.select('> div')
            for comment_option in comment_option_list:
                each_comment_option = comment_option.select('> div').get_text()
                print each_comment_option
            """


if __name__ == '__main__':
    productdb = ProductDB()
    commentdb = CommentDB()

    result = CrawlComment(productdb, commentdb)
    result.crawl_products_comments()
