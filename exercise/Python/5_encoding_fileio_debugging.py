#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""뉴스내용에서 특정단어 검출"""
import requests
from bs4 import BeautifulSoup

def get_news_content(url):
    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content)

    div = soup.find('div', attrs = {'id' : 'kakaoContent'})

    content = ''
    for paragraph in div.find_all('p'):
        content += paragraph.get_text()

    return content

news1 = get_news_content('http://v.media.daum.net/v/20160920150157073')

for word in news1.split(' '):
    if word =='미국':
        print 'exist'
        break

print news1.split('@')[0].split('.')[-1], '@', news1.split('@')[1].split('<')[0]


"""tf-idf 문제"""
import os
from collections import Counter

content_list = []
for root, dirs, files in os.walk('./sample/5_tf_idf'):
    for f in files:
        with open("{}/{}".format(root, f), "r") as fin:
            content_list.append(fin.read())

#c_word1 = Counter(content_list[0].split())

#print c_word1

def find_tf(f_word):
    tf_result = {}
    for i, cont in enumerate(content_list):
        count_word = Counter(cont.split())

        if f_word not in cont:
            tf_result[i] = 0

        else:
            tf_result[i] = float(count_word[f_word])

    return tf_result

def find_idf(f_word2):
    count_num = 0
    idf_result = {}

    for cont in content_list:
        if f_word2 in cont:
            count_num += 1

    for i, num in find_tf(f_word2).items():
        idf_result[i] = num / count_num

    return idf_result

print find_tf("is")
print find_idf("weather")


"""sample.csv에서 전체 도시의 평균 인구 및 최대 면적 도시 계산"""
import csv

with open('./sample/5_csv/sample.csv', 'r') as s_file:
    rows = csv.reader(s_file)
    rows.next()
    pop_num = 0
    cnt = 0
    max_area = 0
    max_city = ""

    for row in rows:
        pop_num += int(row[2])
        cnt += 1
        if row[3] > max_area:
            max_area = row[3]
            max_city = row[1]

    print pop_num / cnt
    print max_city


"""naver 뉴스 html을 5_news.html에 저장"""
import requests
from bs4 import BeautifulSoup

response = requests.get('http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=008&aid=0003743755')
content = response.text
content2 = response.text.decode('utf-8').encode('euc-kr')
print response.encoding

with open('./sample/5_news.html', 'w') as f:
    f.write(content)

with open('./sample/5_news2.html', 'w') as f:
    f.write(content2)
