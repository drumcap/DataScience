#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""기자 이메일 추출"""
import requests
from bs4 import BeautifulSoup
import re

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

print news1

m = re.search(r'\w+@[\w.]+', news1)
print m.group()


"""전화번호 패턴 정규식 만들기"""
m = re.search(r'^0\d{2}-\d{4}-\d{4}', '010-3333-2323')
print m.group()


"""올바른 파이썬 변수명 판단"""
variables = ['abc', '3dbd', 'a_bdd', 'good344', 'aB_23']

for var in variables:
    m = re.search(r'^[a-zA-Z_]+[\w\d]*', var)
    if not m == None:
        print m.group()

for var in variables:
    m = re.match(r'[a-zA-Z_]+[\w\d]*', var)
    if not m == None:
        print m.group()

"""tf_idf1에서 the 개수 세기"""
with open('./sample/5_tf_idf/tf_idf1.txt', 'r') as f:
    cont = f.read()
    m = re.findall('\sthe\s', cont, re.IGNORECASE)
    print len(m)


"""찾는 문자열인지 확인"""
def is_substring(s, query):
    m = re.match(query, s)
    if not m == None:
        return "correct"
    else:
        return "not match"

print is_substring("moonkwoo@yonsei.ac.kr", r'[\w\d]+@[\w.]+')


"""'one,two three.four*five:six'에서 문자만 추출"""
a = 'one,two three.four*five:six'

new_a = a.replace(',', ' ')
new_a = new_a.replace('.', ' ')
new_a = new_a.replace('*', ' ')
new_a = new_a.replace(':', ' ')

new_a2 = re.split(r'[:,.*\s]+', a)

print new_a
print new_a2


"""ip address 판별 정규표현식"""
ip1 = '192.168.0.114'
ip2 = '192.168.112.'
m = re.search(r'\d+\.\d+\.\d+\.\d+', ip1)
if m:
    print m.group()

m2 = re.search(r'\d+\.\d+\.\d+\.\d+', ip2)
if m2:
    print m2.group()


"""올바른 web url 판별 정규표현식"""
webs = ["http://www.test.com",
        "https://www.test1.com",
        "http://www.test.com",
        "ftp://www.test.com",
        "http:://www.test.com",
        "htp://www.test.com",
        "http://www.google.com",
        "https://www.homepage.com"]

for web in webs:
    print re.search(r'^http[s]*://www\.[\w]+\.com', web)
