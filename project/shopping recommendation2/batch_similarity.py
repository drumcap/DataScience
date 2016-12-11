# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
from gradedb import GradeDB
from similaritydb import SimilarityDB


def cosine(grades1, grades2):
    grades1_val = np.array(grades1.values())
    grades2_val = np.array(grades2.values())

    norm_value = float(np.sqrt(sum(grades1_val**2)) * np.sqrt(sum(grades2_val**2)))
    dot_value = float(sum([grades1[product_link] * grades2[product_link] for product_link in grades1.keys() if product_link in grades2.keys()]))
    if norm_value == 0:
        return 0
    return float(dot_value / norm_value)


def jaccard(grades1, grades2):
    temp_grades1 = grades1
    temp_grades2 = grades2

    for product_link in temp_grades1.keys():
        if not product_link in temp_grades2.keys():
            temp_grades2[product_link] = 0

    for product_link in temp_grades2.keys():
        if not product_link in temp_grades1.keys():
            temp_grades1[product_link] = 0

    min_sum = float(sum([min(temp_grades1[product_link], temp_grades2[product_link]) for product_link in temp_grades1.keys()]))
    max_sum = float(sum([max(temp_grades1[product_link], temp_grades2[product_link]) for product_link in temp_grades1.keys()]))
    if max_sum == 0:
        return 0
    return float(min_sum / max_sum)

def pearson(grades1, grades2):
    temp_grades1 = grades1
    temp_grades2 = grades2

    for product_link in temp_grades1.keys():
        if not product_link in temp_grades2.keys():
            temp_grades2[product_link] = 0

    for product_link in temp_grades2.keys():
        if not product_link in temp_grades1.keys():
            temp_grades1[product_link] = 0

    grades1_val = np.array(temp_grades1.values())
    grades2_val = np.array(temp_grades2.values())

    grades1_mean = float(sum(grades1_val)) / len(grades1_val)
    grades2_mean = float(sum(grades2_val)) / len(grades2_val)

    numerator = float(sum([(temp_grades1[product_link] - grades1_mean) * (temp_grades2[product_link] - grades2_mean) for product_link in temp_grades1.keys()]))
    denominator1 = float(sum([(temp_grades1[product_link] - grades1_mean)**2 for product_link in temp_grades1.keys()]))
    denominator2 = float(sum([(temp_grades2[product_link] - grades2_mean)**2 for product_link in temp_grades2.keys()]))

    return float(numerator / (np.sqrt(denominator1) * np.sqrt(denominator2)))


class BatchModel(object):
    def __init__(self, gradedb, similaritydb):
        self.gradedb = gradedb
        self.uservector = self.gradedb.get_vector('user')
        self.itemvector = self.gradedb.get_vector('item')
        self.similaritydb = similaritydb

    def get_similarity(self, model, method, part):

        if model == 'user_based':
            users = self.uservector.keys()
            users.sort()
            divide = len(users) / 5

            divided_users = users[(part-1) * divide : part * divide]
            if part == 5:
                divided_users = users[(part-1) * divide : ]

            existing_user = []

            for user1 in divided_users:
                existing_user.append(user1)
                for user2 in users:
                    if user2 in existing_user:
                        continue
                    else:
                        users_similarity = method(self.uservector[user1], self.uservector[user2])
                        if users_similarity != 0:
                            print user1, user2, users_similarity
                            self.insert_similarity(user1, user2, users_similarity, model, method.func_name)

        elif model == 'item_based':
            items = self.itemvector.keys()
            existing_item = []

            for item1 in items:
                existing_item.append(item1)
                for item2 in items:
                    if item2 in existing_item:
                        continue
                    else:
                        items_similarity = method(self.itemvector[item1], self.itemvector[item2])
                        if items_similarity != 0:
                            print item1, item2, items_similarity
                            self.insert_similarity(item1, item2, items_similarity, model, method.func_name)


    def insert_similarity(self, item1, item2, items_similarity, model, func_name):
        if model == 'user_based':
            try:
                self.similaritydb.save_user_similarity(item1, item2, items_similarity, func_name)
            except Exception as e:
                    print e

        elif model == 'item_based':
            try:
                self.similaritydb.save_item_similarity(item1, item2, items_similarity, func_name)
            except Exception as e:
                    print e


if __name__ == '__main__':
    gradedb = GradeDB()
    similaritydb = SimilarityDB()

    result = BatchModel(gradedb, similaritydb)
    #result.get_similarity(model = 'user_based', method = cosine, part = 1)
    #result.get_similarity(model = 'user_based', method = cosine, part = 2)
    #result.get_similarity(model = 'user_based', method = cosine, part = 3)
    #result.get_similarity(model = 'user_based', method = cosine, part = 4)
    #result.get_similarity(model = 'user_based', method = cosine, part = 5)

    #result.get_similarity(model = 'user_based', method = jaccard, part = 1)
    #result.get_similarity(model = 'user_based', method = jaccard, part = 2)
    #result.get_similarity(model = 'user_based', method = jaccard, part = 3)
    #result.get_similarity(model = 'user_based', method = jaccard, part = 4)
    #result.get_similarity(model = 'user_based', method = jaccard, part = 5)

    #result.get_similarity(model = 'user_based', method = pearson, part = 1)

    result.get_similarity(model = 'item_based', method = cosine, part = 1)
    #result.get_similarity(model = 'item_based', method = jaccard , part = 1)
    #result.get_similarity(model = 'item_based', method = pearson , part = 1)
