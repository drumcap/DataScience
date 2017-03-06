#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import CommentList


class CommentDb(object):
    def __init__(self):
        pass

    def save_comments(self, coId, url, mcontent, user, sympathy, antipathy, enrolltime):
        if self.get_comments_id(coId):
            session = Session()
            insert_comment = CommentList(Id = coId, Link = url, Mcontent = mcontent, User = user, Sympathy = sympathy, Antipathy = antipathy, Enrolltime = enrolltime)
            session.add(insert_comment)
            session.commit()
            session.close()

    def get_comments_id(self, coId):
        session = Session()
        find_comment = session.query(CommentList).filter(CommentList.Id == coId).all()

        if len(find_comment) >=1:
            return False

        else:
            return True

        session.close()

    def get_comment_by_keyword(self, keyword, page, page_size):
        if page <= 0 or page_size <= 0:
            return []

        key_comment = []
        session = Session()
        result = session.query(CommentList).filter(CommentList.Mcontent.like('%' + keyword + '%'))\
                        .order_by(CommentList.Enrolltime)\
                        .offset((page-1) * page_size).limit(page_size)

        for row in result:
            comment = {}
            comment['link'] = row.Link
            comment['content'] = row.Mcontent

            key_comment.append(comment)

        session.close()

        return key_comment
