# -*- coding:utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import uuid

from flask import Flask, jsonify, request
from news_db import NewsDb
from cache_news import CacheNews
from comment_db import CommentDb

app = Flask(__name__)

@app.route('/')
def hello_word():
    return 'Hello, World!'

@app.route('/test')
def hello_json():
    data = {'name' : 'alex', 'description' : 'implemented web api on this page'}
    return jsonify(data)

@app.route('/news/search/<keyword>')
def search_contents(keyword):
    newsdb = NewsDb()
    cachenews = CacheNews()

    user_id = request.args.get('user_id')
    apikey = request.args.get('apikey')

    print user_id, apikey
    if cachenews.auth_user(user_id, apikey):
        result = newsdb.find_keyword_in_contents(str(keyword))
    else:
        result = {'result' : '인증 실패'}
    return jsonify(result)

@app.route('/news/recent')
def get_recent_10():
    cachenews = CacheNews()
    result = cachenews.get_recent_news()
    return jsonify(result)

@app.route('/news/top5')
def get_top_news():
    newsdb = NewsDb()
    sort = request.args.get('sort')
    result = newsdb.get_top_news(sort)

    return jsonify(result)

@app.route('/comment/search/<keyword>')
def search_comment(keyword):
    commentdb = CommentDb()
    page = int(request.args.get('page'))
    page_size = int(request.args.get('pagesize'))

    result = commentdb.get_comment_by_keyword(str(keyword), page, page_size)
    return jsonify(result)

@app.route('/news/<link>', methods = ['DELETE'])
def delete_news(link):
    newsdb = NewsDb()
    result = newsdb.delete_news(link)

    return jsonify({'result' : result})

@app.route('/auth')
def auth():
    cachenews = CacheNews()
    user_id = request.args.get('user_id')
    apikey = str(uuid.uuid4())

    cachenews.hold_user_key(user_id, apikey)
    return jsonify({'apikey': apikey})
    #id: moonkwoo
    #api: 0e368fcb-2816-43ae-b866-4585bbd62186

@app.route('/similar_news/<news_id>')
def get_similar_news(news_id):
    ids = news_id.split(':')
    news_id = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1={}&oid={}&aid={}'.format(ids[0], ids[1], ids[2])
    newsdb = NewsDb()
    result = newsdb.get_similar_news(news_id)

    return jsonify(result)

@app.route('/news/test', methods=['POST'])
def news_post_test():
    print request
    test = request.form['email']
    test2 = request.form['password']

    return jsonify({'result' : 1})

@app.route('/users', methods=['GET'])
def users():
    user_id = request.args.get('user_id')
    return jsonify({'user' : user_id})

@app.route('/users/<int:user_id>', methods=['GET'])
def users_rest(user_id):
    return jsonify({'user' : user_id})

@app.route('/method', methods=['GET', 'POST', 'DELETE'])
def method():
    if request.method == 'GET':
        print request.args.get('user')
        print 'GET'
    elif request.method == 'POST':
        print 'POST'
    elif request.method == 'DELETE':
        print 'DELETE'
    elif request.method == 'PUT':
        print 'PUT'

    return jsonify({'result' : request.method})

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
