#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import NewsArticle, CommentList
from cache_news import CacheNews
from sqlalchemy import desc, func
import datetime
import numpy as np

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

    def get_news_contents(self, link):
        try:
            session = Session()
            result = session.query(NewsArticle).filter(NewsArticle.Link == link).first()
            return result.Content
        except Exception as e:
            print e
            return ''
        finally:
            session.close()

    def is_number(self, char):
        return all(string.isdigit() for string in char)

    def get_similar_news(self, link):
        Kkma = Kkma()
        content = self.get_news_contents(link)
        query_nouns = Kkma.nouns(unicode(content))

        news_word_vector = {str(noun) : content.count(str(noun)) for noun in query_nouns
                            if not self.is_number(n) and content.count(str(noun)) > 1 and len(str(noun)) > 1}

        session = Session()
        result = session.query(NewsArticle).filter(NewsArticle.Link != link).limit(50)

        similar_news = []
        for row in result:
            result_nouns = Kkma.nouns(unicode(row.Content))
            another_word_vector = {str(noun) : row.Content.count(str(noun)) for noun in result_nouns
                                    if not self.is_number(noun) and row.Content.count(str(noun)) > 1 and len(str(noun)) > 1}

            if len(another_word_vector) <= 0:
                continue

            query_keys = news_word_vector.keys()
            result_keys = another_word_vector.keys()

            query_keys.extend(result_keys)
            allkeys = list(set(query_keys))
            dot_product = 0
            for key in allkeys:
                q_val = 0
                if key in news_word_vector:
                    q_val = news_word_vector[key]

                r_val = 0
                if key in another_word_vector:
                    r_val = another_word_vector[key]

                dot_product += q_val * r_val

            q_size = np.sqrt(np.sum(np.array(news_word_vector.values()) ** 2))
            r_size = np.sqrt(np.sum(np.array(another_word_vector.values()) ** 2))
            similarity = dot_product / float(q_size * r_size)
            similar_news.append((row.Link, similarity, result_nouns))

        similar_news = sorted(similar_news, key = lambda x : x[1], reverse = True)

        return {'query_noun' : query_nouns, 'similar_news' : similar_news}
