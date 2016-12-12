# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from gradedb2 import GradeDB
from similaritydb import SimilarityDB
from traintestdb import TrainTestDB

class PredictScore(object):
    def __init__(self, gradedb, similaritydb, traintestdb):
        self.gradedb = gradedb
        self.blank_uservector = self.gradedb.get_uservector('test', blank = True)
        self.correct_uservector = self.gradedb.get_uservector('test', blank = False)
        self.similaritydb = similaritydb
        self.itemvector = self.gradedb.get_itemvector()
        self.traintestdb = traintestdb
        self.blank_comment_set = self.traintestdb.get_blank_test_set()
        self.item_list = self.traintestdb.get_test_item()
        self.user_list = self.traintestdb.get_user_list()

    def get_score(self, model, method):
        if model == 'user_based':
            mae_point, recall_point, precision_point = self.get_user_score(method)

        elif model == 'item_based':
            mae_point, recall_point, precision_point = self.get_item_score(method)

        elif model == 'popularity_based':
            mae_point, recall_point, precision_point = self.get_popular_score()

        result_mae = 'The MAE of {} model by using {} similarity is {}.\n'.format(model, method, mae_point)
        result_recall = 'The Recall of {} model by using {} similarity is {}.\n'.format(model, method, recall_point)
        result_precision = 'The Precision of {} model by using {} similarity is {}.\n'.format(model, method, precision_point)

        print result_mae
        print result_recall
        print result_precision



    def get_user_score(self, method):
        test_uservector = {}
        for user in self.user_list:
            for item in self.item_list:
                temp_score = 0
                temp_sim_sum = 0
                for item_link in self.itemvector.keys():
                    if item == item_link:
                        for similar_user in self.itemvector[item_link].keys():
                            if similar_user == user:
                                continue
                            between_similarity = self.similaritydb.get_user_similarity(similar_user, user, method, value = True)
                            temp_score += self.itemvector[item_link][similar_user] * between_similarity
                            temp_sim_sum += between_similarity
                if not user in test_uservector.keys():
                    temp_dict = {}
                    if temp_sim_sum == 0:
                        temp_dict[item] = float(temp_score)
                    else:
                        temp_dict[item] = float(temp_score) / float(temp_sim_sum)
                    test_uservector[user] = temp_dict
                else:
                    if temp_sim_sum == 0:
                        test_uservector[user][item] = float(temp_score)
                    else:
                        test_uservector[user][item] = float(temp_score) / float(temp_sim_sum)
        return self.get_mae(test_uservector), self.get_recall(test_uservector), self.get_precision(test_uservector)



    def get_item_score(self, method):
        test_uservector = {}
        for user in self.user_list:
            for item in self.item_list:
                temp_score = 0
                temp_sim_sum = 0

                for similar_item in self.itemvector.keys():
                    if similar_item == item:
                        continue
                    for writer in self.itemvector[similar_item].keys():
                        if writer == user:
                            between_similarity = self.similaritydb.get_item_similarity(similar_item, item, method, value = True)
                            temp_score += self.itemvector[similar_item][writer] * between_similarity
                            temp_sim_sum += between_similarity

                if not user in test_uservector.keys():
                    temp_dict = {}
                    if temp_sim_sum == 0:
                        temp_dict[item] = float(temp_score)
                    else:
                        temp_dict[item] = float(temp_score) / float(temp_sim_sum)
                    test_uservector[user] = temp_dict
                else:
                    if temp_sim_sum == 0:
                        test_uservector[user][item] = float(temp_score)
                    else:
                        test_uservector[user][item] = float(temp_score) / float(temp_sim_sum)

        return self.get_mae(test_uservector), self.get_recall(test_uservector), self.get_precision(test_uservector)


    def get_popular_score(self):
        test_uservector = {}
        for user in self.user_list:
            for item in self.item_list:
                temp_score = 0
                temp_sum = 0
                for item_link in self.itemvector.keys():
                    if item == item_link:
                        for similar_user in self.itemvector[item_link].keys():
                            if similar_user == user:
                                continue
                            temp_score += self.itemvector[item_link][similar_user]
                            temp_sum += 1
                if not user in test_uservector.keys():
                    temp_dict = {}
                    if temp_sum == 0:
                        temp_dict[item] = float(temp_score)
                    else:
                        temp_dict[item] = float(temp_score) / float(temp_sum)
                    test_uservector[user] = temp_dict
                else:
                    if temp_sum == 0:
                        test_uservector[user][item] = float(temp_score)
                    else:
                        test_uservector[user][item] = float(temp_score) / float(temp_sum)

        return self.get_mae(test_uservector), self.get_recall(test_uservector), self.get_precision(test_uservector)


    def get_mae(self, test_uservector):
        print test_uservector
        temp_count = 0
        temp_sum = 0
        for link_writer in self.blank_comment_set:
            temp_count += 1
            correct_grade = self.correct_uservector[link_writer[1]][str(link_writer[0])]
            estimated_grade = test_uservector[link_writer[1]][str(link_writer[0])]
            temp_val = abs(correct_grade - estimated_grade)
            temp_sum += temp_val
            #print correct_grade, estimated_grade
        mae_val = float(temp_sum) / float(temp_count)
        return mae_val

    def get_recall(self, test_uservector):
        nouse, expected, intersect = self.get_fds(test_uservector)
        if len(expected) > 0:
            recall_value = float(len(intersect)) / float(len(expected))
            return recall_value
        else:
            return "no expected"


    def get_precision(self, test_uservector):
        expect, nouse, intersect = self.get_fds(test_uservector)
        if len(expect) > 0:
            precision_value = float(len(intersect)) / float(len(expect))
            return precision_value
        else:
            return "no expect"


    def get_fds(self, test_uservector):
        expect_user_tuple = []
        expected_user_tuple = []
        intersect_user_tuple = []

        for test_user in test_uservector.keys():
            for test_item in test_uservector[test_user].keys():
                if test_uservector[test_user][test_item] >= 4:
                    if test_user in self.blank_uservector:
                        if test_item in self.blank_uservector[test_user]:
                            continue
                    expect_user_tuple.append((test_user, test_item))


        for link_writer in self.blank_comment_set:
            if self.correct_uservector[link_writer[1]][str(link_writer[0])] >= 4:
                expected_user_tuple.append((link_writer[1], str(link_writer[0])))

        for user_tuple in expect_user_tuple:
            if user_tuple in expected_user_tuple:
                intersect_user_tuple.append(user_tuple)
        print expect_user_tuple, expected_user_tuple
        return expect_user_tuple, expected_user_tuple, intersect_user_tuple



if __name__ == '__main__':
    gradedb = GradeDB()
    similaritydb = SimilarityDB()
    traintestdb = TrainTestDB()
    result = PredictScore(gradedb, similaritydb, traintestdb)

    result.get_score(model = 'user_based', method = 'cosine')
    #result.get_score(model = 'user_based', method = 'pearson')
    #result.get_score(model = 'user_based', method = 'jaccard')
    result.get_score(model = 'item_based', method = 'cosine')
    #result.get_score(model = 'item_based', method = 'jaccard')
    #result.get_score(model = 'item_based', method = 'pearson')
    result.get_score(model = 'popularity_based', method = None)
