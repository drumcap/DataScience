# -*- coding:utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, jsonify
from news_db import NewsDb
app = Flask(__name__)

@app.route('/')
def hello_word():
    return 'Hello, World!'

@app.route('/test')
def hello_json():
    data = {'name' : 'james', 'company' : 'fastcampus'}
    return jsonify(data)

@app.route('/news/search/<keyword>')
def search_contents(keyword):
    newsdb = NewsDb()
    result = newsdb.find_keyword_in_contents(str(keyword))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
