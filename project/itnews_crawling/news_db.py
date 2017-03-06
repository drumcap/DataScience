#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import NewsArticle, CommentList
from cache_news import CacheNews
from sqlalchemy import desc, func
import datetime

class NewsDb(object):
    def __init__(self):
        pass

    def save_news(self, news_url, news_title, news_contents, news_company, news_reporter_email, news_date):

        if self.get_news_id(news_url):
            session = Session()
            insert_news = NewsArticle(Link = news_url, Title = news_title, Content = news_contents, NewsCompany = news_company, ReporterEmail = news_reporter_email, ReportDate = news_date)
            session.add(insert_news)
            session.commit()
            session.close()

        else:
            session = Session()
            update_news = session.query(NewsArticle).filter(NewsArticle.Link == news_url).one()
            update_news.Title = news_title
            update_news.Content = news_contents
            update_news.NewsCompany = news_company
            update_news.ReporterEmail = news_reporter_email
            update_news.ReportDate = news_date
            session.commit()
            session.close()


    def get_news_id(self, news_url):

        session = Session()
        find_news = session.query(NewsArticle).filter(NewsArticle.Link == news_url).all()

        if len(find_news) >= 1:
            return False

        else:
            return True

        session.close()

    def get_recent_news(self):

        session = Session()
        recent_news = session.query(NewsArticle).order_by(desc(NewsArticle.ReportDate)).limit(10)

        for row in recent_news:
            CacheNews().cache_recent_news(str(row.Title.decode('utf-8')))

        session.close()

    def get_somedays_news(self, countdays):

        session = Session()
        somedays_news = session.query(NewsArticle).filter(NewsArticle.ReportDate >= datetime.date.today() - datetime.timedelta(days=countdays)).all()

        result = [row.Link for row in somedays_news]

        return result

    def find_keyword_in_contents(self, keyword):

        session = Session()
        result = session.query(NewsArticle).filter(NewsArticle.Content.like('%' + keyword + '%')).all()
        news_list = []
        for row in result:
            news_dict = {}
            news_dict['link'] = row.Link
            news_dict['title'] = row.Title
            news_dict['content'] = row.Content
            news_list.append(news_dict)
        return news_list

    def get_top_news(self, sort):

        session = Session()
        if sort == 'new':
            result = session.query(NewsArticle).order_by(desc(NewsArticle.ReportDate)).limit(5)
        elif sort == 'comment':
            result = session.query(NewsArticle.Title, NewsArticle.Content, func.count(CommentList.Id).label('cnt'))\
            .join(CommentList, NewsArticle.Link == CommentList.Link)\
            .group_by(NewsArticle.Link).order_by('cnt desc').limit(5)

        title_content = []
        for row in result:
            title_content.append({'title': row.Title, 'content': row.Content})

        return title_content

    def delete_news(self, link):
        try:
            session = Session()
            session.query(NewsArticle).filter(NewsArticle.Link == link).delete()
            #session.commit()
            return 'Success'
        except Exception as e:
            return "Failure"
        finally:
            session.close()

    def get_similar_news(self, link):
