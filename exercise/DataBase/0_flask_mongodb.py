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
from exer_connection_db import mongo_account

mongo = MongoClient('ec2-54-213-224-243.us-west-2.compute.amazonaws.com' ,27017)
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
