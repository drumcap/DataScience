# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from traintestdb import TrainTestDB
from similaritydb import SimilarityDB


class SetModel(object):
    def __init__(self, traintestdb, similaritydb):
        self.traintestdb = traintestdb
        self.similaritydb = similaritydb

    def set_model(self):
        self.traintestdb.make_blank_test_set()
        self.similaritydb.reset_similarity()


if __name__ == '__main__':
    traintestdb = TrainTestDB()
    similaritydb = SimilarityDB()

    result = SetModel(traintestdb, similaritydb)
    result.set_model()
