#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import requests
import re
import datetime
from bs4 import BeautifulSoup
from cache_news import CacheNews
from news_db import NewsDb

today_1 = datetime.date.today()
today = re.sub('-', '', today_1.isoformat())

class NaverItNewsCrawler(object):
    def __init__(self, url, cachenews, newsdb):
        self.url = url
        self.cachenews = cachenews
        self.newsdb = newsdb

    def news_crawler(self):
        news_url_list = []
        self.cachenews.delete_news_url() # delete news url in redis
        page_num = 1

        #while True:
        while page_num < 2:
            response = requests.post('{}&mid=sec&mode=LSD&date={}&page={}'.format(self.url, today, page_num)) #itnews crawling
            soup = BeautifulSoup(response.content)

            links = soup.find_all('a', attrs={'class' : 'nclicks(fls.list)'}) # news links
            temp_length = len(news_url_list) # for stop [while]

            for link in links:
                if not link.attrs['href'] in news_url_list:
                    news_url_list.append(link.attrs['href'])
                    self.cachenews.cache_news_url(link.attrs['href'])
                    self.get_news_contents(link.attrs['href'])

            if temp_length == len(news_url_list):
                break # for stop [while]

            else:
                page_num += 1

        self.newsdb.get_recent_news()

    def get_news_contents(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content)

        try: # if there is no response,
            news_url                = url
            news_title              = str(soup.find('h3', attrs = {'id' : 'articleTitle'}).get_text())
            news_contents_1         = str(soup.find('div', attrs = {'id' : 'articleBodyContents'}).get_text())
            news_contents           = str(re.sub(r'^\s*//.*\n.*{}\n+', '', news_contents_1)) # delete abnormal sentences
            try:
                news_company        = str(soup.select(".press_logo > a > img ")[0].attrs['title'])
            except Exception as e:
                news_company        = ''
            news_reporter_email_1   = re.findall(r'[\w.-]+@[\w.-]+', news_contents_1)
            try:
                news_reporter_email = str(news_reporter_email_1[-1]) # if there are some e-mail address
            except Exception as e:
                news_reporter_email = ''
            try:
                news_date_1 = str(soup.select('.t11')[0].get_text())
                split_str = re.split(r'[-\s:]+', news_date_1)
                split_int = map(int, split_str)
                news_date = datetime.datetime(split_int[0], split_int[1], split_int[2], split_int[3], split_int[4])
            except Exception as e:
                news_date = ''

            print news_date
            self.newsdb.save_news(news_url, news_title, news_contents, news_company, news_reporter_email, news_date)

        except Exception as e:
            print e




if __name__ == '__main__':
    cachenews = CacheNews()
    newsdb = NewsDb()

    naver_itnews = 'http://news.naver.com/main/list.nhn?sid1=105'
    result = NaverItNewsCrawler(naver_itnews, cachenews, newsdb)
    result.news_crawler()
