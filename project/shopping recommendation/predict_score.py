# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from gradedb import GradeDB
from similaritydb import SimilarityDB
from traintestdb import TrainTestDB

class PredictScore(object):
    def __init__(self, gradedb, similaritydb, traintestdb):
        self.gradedb = gradedb
        self.similaritydb = similaritydb
        self.traintestdb = traintestdb
        #item_ist and user_list is from test set.
        self.item_list = self.traintestdb.get_item_list('test')
        self.user_list = self.traintestdb.get_user_list('test')
        self.itemvector = self.gradedb.get_vector('item')
        self.uservector = self.gradedb.get_vector('user')
        #blank_comment_set is only used to find MAE.
        self.blank_comment_set = self.traintestdb.get_blank_set(value = False)

    #Find MAE, Recall, Precision
    def get_score(self, model, method, threshold):
        if model == 'user_based':
            mae_point, recall_point, precision_point = \
                                        self.get_user_score(method, threshold)

        elif model == 'item_based':
            mae_point, recall_point, precision_point = \
                                        self.get_item_score(method, threshold)

        elif model == 'popularity_based':
            mae_point, recall_point, precision_point = self.get_popular_score()

        result_m = 'The MAE of {} model by using {} similarity is {}.\n'\
                                        .format(model, method, mae_point)
        result_r = 'The Recall of {} model by using {} similarity is {}.\n'\
                                        .format(model, method, recall_point)
        result_p = 'The Precision of {} model by using {} similarity is {}.\n'\
                                        .format(model, method, precision_point)

        print result_m
        print result_r
        print result_p

    def get_user_score(self, method, threshold):
        #Make test_uservector by using test users and test items.
        test_uservector = {}
        for user in self.user_list:
            for item in self.item_list:
                temp_score = 0
                temp_sim_sum = 0
                for item_link in self.itemvector.keys():
                    if item == item_link:
                        for similar_user in self.itemvector[item_link].keys():
                            betw_sim = \
                            self.similaritydb.get_user_similarity(similar_user,
                                                    user, method, value = True)
                            #Only use the similarity larger than threshold.
                            if betw_sim < threshold:
                                continue
                            temp_score += \
                            self.itemvector[item_link][similar_user] * betw_sim
                            temp_sim_sum += betw_sim
                            #Checkpoint
                            print 'userbased : testvector is {}, {}'\
                            .format(user, item),
                            print 'and similar is {}, {}'\
                            .format(similar_user, item_link)

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
                        test_uservector[user][item] = \
                                        float(temp_score) / float(temp_sim_sum)

        return self.get_mae(test_uservector), \
               self.get_recall(test_uservector), \
               self.get_precision(test_uservector)

    def get_item_score(self, method, threshold):
        #Make test_uservector by using test users and test items.
        test_uservector = {}
        for user in self.user_list:
            for item in self.item_list:
                temp_score = 0
                temp_sim_sum = 0
                for writer in self.uservector.keys():
                    if writer == user:
                        for similar_item in self.uservector[writer].keys():
                            betw_sim = \
                            self.similaritydb.get_item_similarity(similar_item,
                                                    item, method, value = True)
                            #Only use the similarity larger than threshold.
                            if betw_sim < threshold:
                                continue
                            temp_score += \
                            self.uservector[writer][similar_item] * betw_sim
                            temp_sim_sum += betw_sim
                            #Checkpoint
                            print 'itembased : testvector is {}, {}'\
                            .format(user, item),
                            print 'and similar is {}, {}'\
                            .format(writer, similar_item)

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
                        test_uservector[user][item] = \
                                        float(temp_score) / float(temp_sim_sum)

        return self.get_mae(test_uservector), \
               self.get_recall(test_uservector), \
               self.get_precision(test_uservector)


    def get_popular_score(self):
        #Make test_uservector by using test users and test items.
        test_uservector = {}
        for user in self.user_list:
            for item in self.item_list:
                temp_score = 0
                temp_sum = 0
                for item_link in self.itemvector.keys():
                    if item == item_link:
                        for similar_user in self.itemvector[item_link].keys():
                            temp_score += \
                                        self.itemvector[item_link][similar_user]
                            temp_sum += 1
                            #Checkpoint
                            print 'popularitybased : testvector is {}, {}'\
                            .format(user, item),
                            print 'and similar is {}, {}'\
                            .format(similar_user, item_link)

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
                        test_uservector[user][item]\
                                        = float(temp_score) / float(temp_sum)

        return self.get_mae(test_uservector), \
               self.get_recall(test_uservector), \
               self.get_precision(test_uservector)


    def get_mae(self, test_uservector):

        temp_count = 0
        temp_sum = 0
        #Calculate only at the blank set.
        for iugrade in self.blank_comment_set:
            temp_count += 1
            correct_grade = iugrade[2]
            estimated_grade = test_uservector[iugrade[1]][str(iugrade[0])]
            temp_val = abs(correct_grade - estimated_grade)
            temp_sum += temp_val
            #Checkpoint
            print "correct grade is {} estimated grade is {}"\
                        .format(correct_grade, estimated_grade)

        mae_val = float(temp_sum) / float(temp_count)
        return mae_val

    def get_recall(self, test_uservector):
        #Expected elements and intersect elements is needed for get Recall.
        no_use, expected, intersect = self.get_fds(test_uservector)
        if len(expected) > 0:
            recall_value = float(len(intersect)) / float(len(expected))
            return recall_value
        else:
            return "no expected"


    def get_precision(self, test_uservector):
        #Expecting elements and intersect elements is needed for get Precision.
        expect, no_use, intersect = self.get_fds(test_uservector)
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
                #Only get the elements which grade is larger than or equal to 4.
                if test_uservector[test_user][test_item] >= 4:
                    #Remove elements which have correct value already.
                    for iugrade in self.blank_comment_set:
                        if test_user == iugrade[1] and test_item == iugrade[0]:
                            continue
                    expect_user_tuple.append((test_user, test_item))


        for iugrade in self.blank_comment_set:
            #Only get the elements which grade is larger than or equal to 4.
            if iugrade[2] >= 4:
                expected_user_tuple.append((iugrade[1], str(iugrade[0])))

        #Find intersect elements.
        for user_tuple in expect_user_tuple:
            if user_tuple in expected_user_tuple:
                intersect_user_tuple.append(user_tuple)

        return expect_user_tuple, expected_user_tuple, intersect_user_tuple



if __name__ == '__main__':
    gradedb = GradeDB()
    similaritydb = SimilarityDB()
    traintestdb = TrainTestDB()
    result = PredictScore(gradedb, similaritydb, traintestdb)

    result.get_score(model = 'user_based', method = 'cosine', threshold = 0)
    #result.get_score(model = 'user_based', method = 'pearson')
    #result.get_score(model = 'user_based', method = 'jaccard')
    result.get_score(model = 'item_based', method = 'cosine', threshold = 0.1)
    #result.get_score(model = 'item_based', method = 'jaccard')
    #result.get_score(model = 'item_based', method = 'pearson')
    result.get_score(model = 'popularity_based', method = None,
                                                            threshold = None)
