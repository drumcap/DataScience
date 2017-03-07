#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
import json
import datetime
from news_db import NewsDb
from comment_db import CommentDb

class NaverItNewsCommentCrawler(object):
    def __init__(self, newsdb, commentdb):
        self.newsdb = newsdb
        self.commentdb = commentdb
        self.threedays_news = self.newsdb.get_somedays_news(countdays=3)

    def crawl_news_comments(self):
        for link in self.threedays_news:
            self.crawl_comments(url=link)
            print link

    def crawl_comments(self, url, pagenum = 1):
        news_aid_1 = re.search(r'aid=\d+', url).group(0)
        news_aid = re.sub(r'aid=', '', news_aid_1)
        news_oid_1 = re.search(r'oid=\d+', url).group(0)
        news_oid = re.sub(r'oid=', '', news_oid_1)



        api = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_it&pool=cbox5&_callback=window.__cbox_jindo_callback._3031&lang=ko&country=KR&objectId=news{}%2C{}&categoryId=&pageSize=20&indexSize=10&groupId=&page={}'.format(news_oid ,news_aid, pagenum)
        referer = url + '&m_view=1&m_url=%2Fcomment%2Fall.nhn%3FserviceId%3Dnews%26gno%3Dnews{}%2C{}%26sort%3Dlikability'.format(news_oid, news_aid)

        headers = {}
        headers['referer'] = referer

        response = requests.get(api, headers = headers)
        res1 = re.sub('window[.\w\d_]+', '', response.content)
        res2 = res1[1:-2]
        res3 = json.loads(res2)
        comments = res3['result']['commentList']

        if len(comments) > 0:
            for comment in comments:
                coId = int(comment['commentNo'])
                mcontent = str(comment['contents'])
                user = str(comment['userName'])
                sympathy = int(comment['sympathyCount'])
                antipathy = int(comment['antipathyCount'])

                enrolltime_1 = str(comment['regTime'])
                enrolltime_2 = re.split(r'[-T:+]+', enrolltime_1)
                enrolltime_3 = map(int, enrolltime_2)
                enrolltime = datetime.datetime(enrolltime_3[0], enrolltime_3[1], enrolltime_3[2], enrolltime_3[3], enrolltime_3[4], enrolltime_3[5])

                self.commentdb.save_comments(coId, url, mcontent, user, sympathy, antipathy, enrolltime)

            pagenum += 1
            self.crawl_comments(url, pagenum)


if __name__ == "__main__":
    newsdb = NewsDb()
    commentdb = CommentDb()

    result = NaverItNewsCommentCrawler(newsdb, commentdb)
    result.crawl_news_comments()
