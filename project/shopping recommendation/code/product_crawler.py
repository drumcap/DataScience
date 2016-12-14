# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import requests
from bs4 import BeautifulSoup
import re
from productdb import ProductDB


class CrawlImvely(object):
    def __init__(self, productdb, product_zip):
        self.productdb = productdb
        self.product_zip = product_zip
        self.product_links = []

    def crawl_products_link(self):
        for category in product_zip:
            self.crawl_ca_products(category, product_zip[category], pagenum = 1)

    def crawl_ca_products(self, category, url, pagenum):
        # The page of cosmetic cateogry is different from others.
        if category != 'cosmetic':
            product_url = url + "&page={}".format(pagenum)
        else:
            product_url = url

        response = requests.get(product_url)
        soup= BeautifulSoup(response.content)

        # The page of cosmetic cateogry is different from others.
        if category != 'cosmetic':
            body = soup.find('div', attrs = {'class' : 'xans-element- \
            xans-product xans-product-normalpackage package_box '})
        else:
            body = soup.find('div', attrs = {'class' : 'xans-element- \
            xans-product xans-product-listmain-42 xans-product-listmain \
            xans-product-42'})

        #Find the information of product.
        product_lists = body.find('ul', attrs = {'class' : 'prdList column4'})

        if product_lists:
            product_list  = product_lists.select('> li')

            for product in product_list:
                name = product.find('p', attrs = {'class' : 'name'})
                link_1 = name.select('> a')
                link = link_1[0]['href']
                productno_1 = re.search(r'product_no=\d*', link).group()
                productno = str(re.sub(r'product_no=', '', productno_1))
                title_1 = name.select('> a > span')[0].get_text()
                title = title_1.encode('utf-8')
                print title

                try:
                    self.productdb.save_product_info(productno ,link,
                                                     title, category)
                except Exception as e:
                    print e

            #Recursive function
            if category != 'cosmetic':
                pagenum += 1
                self.crawl_ca_products(category, url, pagenum)
            else:
                print 0


if __name__ == "__main__":
    productdb = ProductDB()

    #The imvely shopping mall page have some items in each category.
    product_zip = {}
    '''
    link_outer = 'http://www.imvely.com/product/list.html?cate_no=41'
    product_zip['outer'] = link_outer
    link_knit = 'http://www.imvely.com/product/list.html?cate_no=116'
    product_zip['knit'] = link_knit
    link_tee = 'http://www.imvely.com/product/list.html?cate_no=46'
    product_zip['tee'] = link_tee
    link_onepiece = 'http://www.imvely.com/product/list.html?cate_no=52'
    product_zip['onepiece'] = link_onepiece
    link_shirt = 'http://www.imvely.com/product/list.html?cate_no=126'
    product_zip['shirt'] = link_shirt
    link_pants = 'http://www.imvely.com/product/list.html?cate_no=57'
    product_zip['pants'] = link_pants
    link_skirt = 'http://www.imvely.com/product/list.html?cate_no=97'
    product_zip['skirt'] = link_skirt
    link_acc = 'http://www.imvely.com/product/list.html?cate_no=62'
    product_zip['acc'] = link_acc
    link_shoes = 'http://www.imvely.com/product/list.html?cate_no=59'
    product_zip['shoes&bags'] = link_shoes
    '''
    link_cosmetic = 'http://www.imvely.com/beauty_main.html'
    product_zip['cosmetic'] = link_cosmetic


    result = CrawlImvely(productdb, product_zip)
    result.crawl_products_link()
