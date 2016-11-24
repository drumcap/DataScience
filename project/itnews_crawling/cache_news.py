#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import redis
from connection import server, redis_account

class CacheNews(object):
    def __init__(self):
        self.r= redis.Redis(host = server, port = 6379, password = redis_account['pw'])

    def delete_news_url(self):
        self.r.delete('urllist')

    def cache_news_url(self, news_url):
        self.r.rpush('urllist', news_url)
