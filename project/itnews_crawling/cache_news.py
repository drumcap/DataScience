#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from connection import server, redis_connection

class CacheNews(object):
    def __init__(self):
        self.r= redis_connection

    def delete_news_url(self):
        self.r.delete('urllist')

    def cache_news_url(self, news_url):
        self.r.rpush('urllist', news_url)

    def cache_recent_news(self, news_title):
        self.r.rpush('recentlist', news_title)
        self.r.ltrim('recentlist', -10, -1)

    def get_recent_news(self):
        return self.r.lrange('recentlist', 0, -1)

    def hold_user_key(self, user_id, apikey):
        self.r.hset('auth_users', user_id, apikey)

    def auth_user(self, user_id, apikey):
        if user_id == None or apikey == None:
            return False

        return self.r.hget('auth_users', user_id) == apikey
