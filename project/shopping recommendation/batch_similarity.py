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


def pearson2(grades1, grades2):
    count_key = len(grades1.keys())
    for product_link in grades2.keys():
        if not product_link in grades1.keys():
            count_key += 1

    sum_grades1 = sum([float(grades1[product_link]) for product_link in grades1.keys()])
    sum_grades2 = sum([float(grades2[product_link]) for product_link in grades2.keys()])

    square_sum1 = sum([float(grades1[product_link])**2 for product_link in grades1.keys()])
    square_sum2 = sum([float(grades2[product_link])**2 for product_link in grades2.keys()])

    dot_value = float(sum([grades1[product_link] * grades2[product_link] for product_link in grades1.keys() if product_link in grades2.keys()]))

    numerator = dot_value - ((sum_grades1 * sum_grades2)/count_key)
    denominator = ((square_sum1 - ((sum_grades1**2)/count_key))*(square_sum2 - ((sum_grades2**2)/count_key)))**0.5

    if denominator == 0:
        return 0
    return float(numerator / denominator)

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
        self.uservector = self.gradedb.get_uservector('train', blank = False)
        self.similaritydb = similaritydb
        self.itemvector = self.gradedb.get_itemvector()
        self.insert_method = None

    def get_similarity(self, model, method):
        if method == cosine:
            self.insert_method = 'cosine'
        elif method == jaccard:
            self.insert_method = 'jaccard'
        elif method == pearson:
            self.insert_method = 'pearson'

        #self.similaritydb.reset_similarity(model, self.insert_method)

        if model == 'user_based':
            users = self.uservector.keys()
            existing_user = []

            for user1 in users:
                existing_user.append(user1)
                for user2 in users:
                    if user2 in existing_user:
                        continue
                    else:
                        users_similarity = method(self.uservector[user1], self.uservector[user2])
                        if users_similarity != 0:
                            print user1, user2, users_similarity
                            self.insert_similarity(user1, user2, users_similarity, model, self.insert_method)

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
                            self.insert_similarity(item1, item2, items_similarity, model, self.insert_method)


    def insert_similarity(self, item1, item2, items_similarity, model, insert_method):
        if model == 'user_based':
            try:
                self.similaritydb.save_user_similarity(item1, item2, items_similarity, insert_method)
            except Exception as e:
                    print e

        elif model == 'item_based':
            try:
                self.similaritydb.save_item_similarity(item1, item2, items_similarity, insert_method)
            except Exception as e:
                    print e


if __name__ == '__main__':
    gradedb = GradeDB()
    similaritydb = SimilarityDB()

    result = BatchModel(gradedb, similaritydb)
    #result.get_similarity(model = 'user_based', method = cosine)
    #result.get_similarity(model = 'user_based', method = jaccard)
    #result.get_similarity(model = 'user_based', method = pearson)
    result.get_similarity(model = 'item_based', method = cosine)
    result.get_similarity(model = 'item_based', method = jaccard)
    result.get_similarity(model = 'item_based', method = pearson)
