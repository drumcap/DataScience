#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""using daum_api and mongodb"""
import requests
import json
from exer_connection import Api_key_daum
from HTMLParser import HTMLParser
import re
from pymongo import MongoClient
from exer_connection_db import mongo_account, server

mongo = MongoClient(server ,27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'],
source = 'test')
daum_api = mongo.test.daum_api

response = requests.get('https://apis.daum.net/search/web?\
apikey={}&q={}&output=json'.format(Api_key_daum, '갤럭시'))

data = json.loads(response.content)
count_num = int(data['channel']['result'])

for i in range(0, count_num):
    pubdate = data['channel']['item'][i]['pubDate']

    title = data['channel']['item'][i]['title']
    unhtml_title = HTMLParser().unescape(title)
    str_title = re.sub("\<[a-zA-Z\/]+\>", "", unhtml_title)

    daum_api.insert_one({'date' : pubdate, 'title' : str_title})

result = daum_api.find()
for doc in result:
    print doc


"""find city whose population is greater than 10,000,000"""
from pymongo import MongoClient
from exer_connection_db import mongo_account, server
mongo = MongoClient(server ,27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'], source = 'test')
zip_collection = mongo.test.zip

pipelines = []
pipelines.append({'$group' : {'_id' :'$state', 'pop' : {'$sum' : '$pop'}}})
pipelines.append({'$match' : {'pop' : {'$gte' : 10 * 1000 * 1000}}})

result = zip_collection.aggregate(pipelines)
for doc in result:
    print doc


from collections import defaultdict

result = zip_collection.find()

state_pop = defaultdict(lambda : 0)

for doc in result:
    state_pop[doc['state']] += doc['pop']

for i, j in state_pop.items():
    if j > 10 * 1000 * 1000:
        print i, j

new_state_pop = {k : v for k, v in state_pop.items() if v > 10 * 1000 * 1000}
print new_state_pop


"""find average poopulation in states"""
from pymongo import MongoClient
from exer_connection_db import mongo_account, server

mongo = MongoClient(server, 27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'], source = 'test')
zip_collection = mongo.test.zip

pipelines = []
pipelines.append({'$group' : {'_id' :{'state' : '$state', 'city' : '$city'}, 'pop' : {'$sum' : '$pop'}}})
pipelines.append({'$group' :{'_id' : '$_id.state', 'avgpop' : {'$avg' : '$pop'}}})

result = zip_collection.aggregate(pipelines)
for doc in result:
    print doc


"""find maximum,  minimun population in states"""
from pymongo import MongoClient
from exer_connection_db import mongo_account, server

mongo = MongoClient(server, 27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'], source = 'test')
zip_collection = mongo.test.zip

pipelines = []
pipelines.append({'$group' : {'_id' : {'state' : "$state", 'city' : "$city"}, 'pop' : {'$sum' : "$pop"}}})
pipelines.append({'$sort' : {'pop' : 1}})
pipelines.append({'$group' : {'_id' : "$_id.state", 'biggestcity' : {'$last' : "$_id.city"}, 'biggestpop' : {'$last' : "$pop"}, 'smallestcity' : {'$first' : "$_id.city"}, 'smallestpop' : {'$first' : "$pop"}}})
pipelines.append({'$project' : {'_id' : 0, 'state' : "$_id", 'biggestcity' : {'name' : "$biggestcity", 'pop' : "$biggestpop"}, 'smallestcity' : {'name' : "$smallestcity", 'pop' : '$smallestpop'}}})


result = zip_collection.aggregate(pipelines)
for doc in result:
    print doc


"""find the number of restaurant per borough"""
mongo = MongoClient(server ,27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'], source = 'test')
rest = mongo.test.rest

pipelines = []
pipelines.append({'$group' : {'_id' : "$borough", 'count' : {'$sum' : 1}}})

result = rest.aggregate(pipelines)
for doc in result:
    print doc


"""find the number of 'Brazilian' restaurant per zipcode"""
mongo = MongoClient(server ,27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'], source = 'test')
rest = mongo.test.rest

pipelines = []
pipelines.append({'$match' : {'cuisine' : 'Brazilian'}})
pipelines.append({'$group' : {'_id' : "$address.zipcode", 'cnt' : {'$sum' : 1}}})

result = rest.aggregate(pipelines)
for doc in result:
    print doc


"""find the most cuisine in the restaurant per borough"""
mongo = MongoClient(server ,27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'], source = 'test')
rest = mongo.test.rest

pipelines = []
pipelines.append({'$group' :{'_id' : {'bo': '$borough', 'cu':'$cuisine'}, 'num' : {'$sum' : 1}}})
pipelines.append({'$sort' : {'num' : -1}})
pipelines.append({'$group' :{'_id' : '$_id.bo', 'best_cuisine' : {'$first':'$_id.cu'}, 'num' : {'$first':'$num'}}})

result = rest.aggregate(pipelines)
for doc in result:
    print doc


"""find the cusine getting high average score"""
mongo = MongoClient(server ,27017)
mongo.the_database.authenticate(mongo_account['id'], mongo_account['pw'], source = 'test')
rest = mongo.test.rest

pipelines = []
pipelines.append({'$unwind' : '$grades'})
pipelines.append({'$group' :{'_id' : '$cuisine', 'avgscore' : {'$avg' : '$grades.score'} } })
pipelines.append({'$limit' : 1})

result = rest.aggregate(pipelines)
for doc in result:
    print doc
