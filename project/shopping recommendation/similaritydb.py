# -*-coding:utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session
from model import  ImvelyUserbasedSimilarity, ImvelyItembasedSimilarity

class SimilarityDB(object):
    def __init__(self):
        pass

    def save_user_similarity(self, user1, user2, users_similarity, insert_method):
        session = Session()
        if self.get_user_similarity(user1, user2, insert_method) == 0:
            if insert_method == 'cosine':
                insert_similarity = ImvelyUserbasedSimilarity(User1 = user1, User2 = user2, Cossimilarity = users_similarity)
            elif insert_method == 'jaccard':
                insert_similarity = ImvelyUserbasedSimilarity(User1 = user1, User2 = user2, Jacsimilarity = users_similarity)
            elif insert_method == 'pearson':
                insert_similarity = ImvelyUserbasedSimilarity(User1 = user1, User2 = user2, Pearsimilarity = users_similarity)
            session.add(insert_similarity)
            session.commit()
        else:
            self.update_user_similarity(user1, user2, users_similarity, insert_method)
        session.close()

    def save_item_similarity(self, item1, item2, items_similarity, insert_method):
        session = Session()
        if self.get_item_similarity(item1, item2, insert_method) == 0:
            if insert_method == 'cosine':
                insert_similarity = ImvelyItembasedSimilarity(Item1 = item1, Item2 = item2, Cossimilarity = items_similarity)
            elif insert_method == 'jaccard':
                insert_similarity = ImvelyItembasedSimilarity(Item1 = item1, Item2 = item2, Jacsimilarity = items_similarity)
            elif insert_method == 'pearson':
                insert_similarity = ImvelyItembasedSimilarity(Item1 = item1, Item2 = item2, Pearsimilarity = items_similarity)
            session.add(insert_similarity)
            session.commit()
        else:
            self.update_item_similarity(item1, item2, items_similarity, insert_method)
        session.close()

    def update_user_similarity(self, user1, user2, users_similarity, insert_method):
        session = Session()
        update_similarity = session.query(ImvelyUserbasedSimilarity).filter(ImvelyUserbasedSimilarity.User1 == user1, ImvelyUserbasedSimilarity.User2 == user2).all()
        if not update_similarity:
            update_similarity = session.query(ImvelyUserbasedSimilarity).filter(ImvelyUserbasedSimilarity.User1 == user2, ImvelyUserbasedSimilarity.User2 == user1).all()
        if insert_method == 'cosine':
            update_similarity[0].Cossimilarity = users_similarity
        elif insert_method == 'jaccard':
            update_similarity[0].Jacsimilarity = users_similarity
        elif insert_method == 'pearson':
            update_similarity[0].Pearsimilarity = users_similarity
        session.commit()
        session.close()

    def update_item_similarity(self, item1, item2, items_similarity, insert_method):
        session = Session()
        update_similarity = session.query(ImvelyItembasedSimilarity).filter(ImvelyItembasedSimilarity.Item1 == item1, ImvelyItembasedSimilarity.Item2 == item2).all()
        if not update_similarity:
            update_similarity = session.query(ImvelyItembasedSimilarity).filter(ImvelyItembasedSimilarity.Item1 == item2, ImvelyItembasedSimilarity.Item2 == item1).all()
        if insert_method == 'cosine':
            update_similarity[0].Cossimilarity = items_similarity
        elif insert_method == 'jaccard':
            update_similarity[0].Jacsimilarity = items_similarity
        elif insert_method == 'pearson':
            update_similarity[0].Pearsimilarity = items_similarity
        session.commit()
        session.close()

    def reset_similarity(self):
        session = Session()
        session.query(ImvelyUserbasedSimilarity).delete()
        session.query(ImvelyItembasedSimilarity).delete()
        session.commit()
        session.close()


    def get_user_similarity(self, user1, user2, method):
        session = Session()
        result_similarity_row = session.query(ImvelyUserbasedSimilarity).filter(ImvelyUserbasedSimilarity.User1 == user1, ImvelyUserbasedSimilarity.User2 == user2).all()
        if not result_similarity_row:
            result_similarity_row = session.query(ImvelyUserbasedSimilarity).filter(ImvelyUserbasedSimilarity.User1 == user2, ImvelyUserbasedSimilarity.User2 == user1).all()
        if not result_similarity_row:
            return 0
        try:
            if method == 'cosine':
                result_similarity = result_similarity_row[0].Cossimilarity
            elif method == 'jaccard':
                result_similarity = result_similarity_row[0].Jacsimilarity
            elif method == 'pearson':
                result_similarity = result_similarity_row[0].Pearsimilarity
        except Exception as e:
            print e
        session.close()
        return result_similarity

    def get_item_similarity(self, item1, item2, method):
        session = Session()
        result_similarity_row = session.query(ImvelyItembasedSimilarity).filter(ImvelyItembasedSimilarity.Item1 == item1, ImvelyItembasedSimilarity.Item2 == item2).all()
        if not result_similarity_row:
            result_similarity_row = session.query(ImvelyItembasedSimilarity).filter(ImvelyItembasedSimilarity.Item1 == item2, ImvelyItembasedSimilarity.Item2 == item1).all()
        if not result_similarity_row:
            return 0
        try:
            if method == 'cosine':
                result_similarity = result_similarity_row[0].Cossimilarity
            elif method == 'jaccard':
                result_similarity = result_similarity_row[0].Jacsimilarity
            elif method == 'pearson':
                result_similarity = result_similarity_row[0].Pearsimilarity
        except Exception as e:
            print e
        session.close()
        return result_similarity
