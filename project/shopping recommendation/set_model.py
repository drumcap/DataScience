# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from traintestdb import TrainTestDB
from similaritydb import SimilarityDB
from gradedb2 import GradeDB

class SetModel(object):
    def __init__(self, traintestdb, similaritydb):
        self.traintestdb = traintestdb
        self.similaritydb = similaritydb

    def set_model(self):
        self.traintestdb.make_blank_test_set()
        self.similaritydb.reset_similarity()


    def set_vector(self):
        gradedb = GradeDB()
        gradedb.delete_vector()
        gradedb.save_uservector("train", blank = False)
        gradedb.save_uservector("test", blank = True)
        gradedb.save_uservector("test", blank = False)
        gradedb.save_itemvector()

if __name__ == '__main__':
    traintestdb = TrainTestDB()
    similaritydb = SimilarityDB()

    result = SetModel(traintestdb, similaritydb)
    result.set_model()
    result.set_vector()
