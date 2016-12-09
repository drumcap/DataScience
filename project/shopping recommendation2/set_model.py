# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from traintestdb import TrainTestDB
from similaritydb import SimilarityDB
from gradedb import GradeDB

class SetModel(object):
    def __init__(self, traintestdb, similaritydb):
        self.traintestdb = traintestdb
        self.similaritydb = similaritydb

    def set_model(self):
        self.traintestdb.product_train_test_set()
        self.traintestdb.user_train_test_set()
        print self.traintestdb.get_blank_set(value = True)
        self.similaritydb.reset_similarity()

        self.set_vector()

    def set_vector(self):
        gradedb = GradeDB()
        gradedb.delete_vector()
        gradedb.save_uservector()
        gradedb.save_itemvector()

if __name__ == '__main__':
    traintestdb = TrainTestDB()
    similaritydb = SimilarityDB()

    result = SetModel(traintestdb, similaritydb)
    result.set_model()
