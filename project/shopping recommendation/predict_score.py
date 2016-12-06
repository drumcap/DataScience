# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from gradedb import GradeDB
from similaritydb import SimilarityDB
from traintestdb import TrainTestDB

class PredictScore(ojbect):
    def __init__(self, gradedb, similaritydb, traintestdb):
        self.gradedb = gradedb
        self.blank_uservector = self.gradedb.get_uservector('test', blank = True)
        self.correct_uservector = self.gradedb.get_uservector('test', blank = False)
        self.similaritydb = similaritydb
        self.itemcevtor = self.gradedb.get_itemvector()
        self.traintestdb = traintestdb
        self.blank_comment_set = self.traintestdb.get_blank_test_set()
        self.item_list = self.traintestdb.product_train_test_set()[1]
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
                    temp_dict[item] = float(temp_score) / float(temp_sim_sum)
                    test_uservector[user] = temp_dict
                else:
                    test_uservector[user][item] = float(temp_score) / float(temp_sim_sum)

        return self.get_mae(test_uservector), self.get_recall(test_uservector), self.get_precision(test_uservector)



    def get_item_score(self, method):
        test_uservector = {}
        for user in self.user_list:
            for item in self.item_list:
                temp_score = 0
                temp_sim_sum = 0
                for writer in self.blank_uservector.keys():
                    if user == writer:
                        for similar_item in self.blank_uservector[writer].keys():
                            if similar_item == item:
                                continue
                            between_similarity = self.similaritydb.get_item_similarity(similar_item, item, method, value = True)
                            temp_score += self.blank_uservector[writer][similar_item] * between_similarity
                            temp_sim_sum += between_similarity
                if not user in test_uservector.keys():
                    temp_dict = {}
                    temp_dict[item] = float(temp_score) / float(temp_sim_sum)
                    test_uservector[user] = temp_dict
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
                    temp_dict[item] = float(temp_score) / float(temp_sim_sum)
                    test_uservector[user] = temp_dict
                else:
                    test_uservector[user][item] = float(temp_score) / float(temp_sim_sum)

        return self.get_mae(test_uservector), self.get_recall(test_uservector), self.get_precision(test_uservector)


    def get_mae(self, test_uservector):
        temp_count = 0
        temp_sum = 0
        for link_writer in self.blank_comment_set:
            temp_count += 1
            correct_grade = self.correct_uservector[link_writer[1]][link_writer[0]]
            estimated_grade = test_uservector[link_writer[1]][link_writer[0]]
            temp_val = abs(correct_grade - estimated_grade)
            temp_sum += temp_val

        mae_val = float(temp_sum) / float(temp_count)
        return mae_val

    def get_recall(self, test_uservector):
        nouse, expected, intersect = self.get_fds(test_uservector)
        recall_value = float(len(intersect)) / float(len(expected))
        return recall_value


    def get_precision(self, test_uservector):
        expect, nouse, intersect = self.get_fds(test_uservector)
        precision_value = float(len(intersect)) / float(len(expect))
        return precision_value


    def get_fds(self, test_uservector):
        expect_user_tuple = []
        expected_user_tuple = []
        intersect_user_tuple = []

        for test_user in test_uservector.keys():
            for test_item in test_user.keys():
                if test_uservector[test_user][test_item] >= 4:
                    expect_user_tuple.append((test_user, test_item))


        for link_writer in self.blank_comment_set:
            if self.correct_uservector[link_writer[1]][link_writer[0]] >= 4:
                expected_user_tuple.append((link_writer[1], link_writer[0]))

        for user_tuple in expect_user_tuple:
            if user_tuple in expected_user_tuple:
                intersect_user_tuple.append(user_tuple)

        return expect_user_tuple, expected_user_tuple, intersect_user_tuple



if __name__ == '__main__':
    gradedb = GradeDB()
    similaritydb = SimilarityDB()
    traintestdb = TrainTestDB()
    result = PredictScore(gradedb, similaritydb, traintestdb)

    result.get_score(model = 'user_based', method = 'cosine')
    '''
    result.get_score(model = 'user_based', method = 'pearson')
    result.get_score(model = 'user_based', method = 'jaccard')
    result.get_score(model = 'item_based', method = 'cosine')
    result.get_score(model = 'item_based', method = 'jaccard')
    result.get_score(model = 'item_based', method = 'pearson')
    result.get_score(model = 'populuarity_based', method = None)

    '''
