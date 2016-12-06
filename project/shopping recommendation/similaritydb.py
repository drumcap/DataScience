# -*-coding:utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from connection import Session, mongo

class SimilarityDB(object):
    def __init__(self):
        self.usersim = mongo.imvely.userbasedsimilarity
        self.itemsim = mongo.imvely.itembasedsimilarity

    def save_user_similarity(self, user1, user2, users_similarity, method):
        if self.get_user_similarity(user1, user2, method, value = False) == 0:
            self.usersim.insert_one({'user1' : user1, 'user2' : user2, method : users_similarity})
        else:
            user1, user2 = self.get_user_similarity(user1, user2, method, value = False)
            self.update_user_similarity(user1, user2, users_similarity, method)

    def save_item_similarity(self, item1, item2, items_similarity, method):
        if self.get_item_similarity(item1, item2, method, value = False) == 0:
            self.itemsim.insert_one({'item1' : item1, 'item2' : item2, method : items_similarity})
        else:
            item1, item2 = self.get_item_similarity(item1, item2, method, value = False)
            self.update_item_similarity(item1, item2, items_similarity, method)

    def update_user_similarity(self, user1, user2, users_similarity, method):
        self.usersim.update_one({'user1' : user1, 'user2' : user2}, {'$set' : {method : users_similarity}}, upsert = True)

    def update_item_similarity(self, item1, item2, items_similarity, method):
        self.itemsim.update_one({'item1' : item1, 'item2' : item2}, {'$set' : {method : items_similarity}}, upsert = True)

    def reset_similarity(self):
        self.usersim.delete_many({})
        self.itemsim.delete_many({})

    def get_user_similarity(self, user1, user2, method, value):
        result = self.usersim.find_one({'user1' : user1, 'user2' : user2})
        if not result:
            result = self.usersim.find_one({'user1' : user2, 'user2' : user1})
        if not result:
            return 0
        if value:
            return result[method]
        return result['user1'], result['user2']

    def get_item_similarity(self, item1, item2, method, value):
        result = self.itemsim.find_one({'item1' : item1, 'item2' : item2})
        if not result:
            result = self.itemsim.find_one({'item1' : item2, 'item2' : item1})
        if not result:
            return 0
        if value:
            return result[method]
        return result['item1'], result['item2']
