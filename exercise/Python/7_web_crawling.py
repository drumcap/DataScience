#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""주소를 통해 좌표 추출"""
import requests
import json
from exer_connection import Api_key_google_map

api_end_point = 'https://maps.googleapis.com/maps/api/geocode/json?address=\
서울특별시 양천구 목동 현대월드타워&key=' + Api_key_google_map

res = requests.get(api_end_point)
data = json.loads(res.text)
print data['results'][0]['geometry']['location']


"""위도 경도를 통한 거리 구하기"""
import requests
import json
from exer_connection import Api_key_google_map
from math import sin, cos, asin, sqrt, radians, atan2

def get_lat_longitude(place):
    api_end_point = 'https://maps.googleapis.com/maps/api/geocode/json?address=\
                     {}&key='.format(place) + Api_key_google_map
    res = requests.get(api_end_point)
    cont = json.loads(res.text)
    return cont['results'][0]['geometry']['location']['lat'],\
           cont['results'][0]['geometry']['location']['lng']

def get_distance(place1, place2):
    #haversine formula
    R = 6373.0 # circle earth radius(km)

    lat1, lng1 = get_lat_longitude(place1)
    lat2, lng2 = get_lat_longitude(place2)

    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    dlat = lat2 - lat1
    dlng = lng2 - lng1

    hav_d_r = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    distance = 2 * R * asin(sqrt(hav_d_r))
    distance2 = 2 * R * atan2(sqrt(hav_d_r), sqrt(1 - hav_d_r))

    return distance, distance2

print get_distance("서울특별시 양천구 목동 현대월드타워", "서울특별시 서초구 서운로 6")


"""네이버 뉴스 제목 및 내용 파싱"""
import requests
from bs4 import BeautifulSoup

response = requests.get("http://news.naver.com/main/read.nhn?\
mode=LPOD&mid=sec&oid=001&aid=0008825125&isYeonhapFlash=Y")
contents = response.text
soup = BeautifulSoup(contents)

title = soup.find('h3', attrs = {'id' : 'articleTitle'})

content = ''
for paragraph in soup.find_all('div', attrs = {'id' : 'articleBodyContents'}):
    content += paragraph.get_text()

print title
print content


"""cine21에서 배우 이름 순위순으로 가져오기"""
import requests
from bs4 import BeautifulSoup
import re

data1 = {}
data1['section'] = 'actor'
data1['period_start'] = '2016-10'
data1['gender'] = 'all'
data1['page'] = '1'

response = requests.post("http://www.cine21.com/rank/person/content", data = data1)
contents = response.text
soup = BeautifulSoup(contents)

for person in soup.find_all('div', attrs = {'class' : 'name'}):
    print re.sub(r'\(.+\)', ' ' ,person.get_text())


"""daum 검색 api 활용"""
import requests
import json
from exer_connection import Api_key_daum

response = requests.get('https://apis.daum.net/search/web?\
apikey={}&q={}&output=json'.format(Api_key_daum, '카카오프렌즈 -네오'))

data =json.loads(response.text)

print data['channel']['item'][0]['title']


"""naver 검색 api 활용"""
import requests
from exer_connection import Api_key_naver
from exer_connection import Api_secret_naver

naver_url = 'https://openapi.naver.com/v1/search/webkr.xml?\
query={}'.format('갤럭시 노트')

headers = {}
headers['Content-Type'] = 'application/xml'
headers['X-Naver-Client-Id'] = Api_key_naver
headers['X-Naver-Client-Secret'] = Api_secret_naver

response = requests.get(naver_url, headers = headers)
print response.text


"""경향신문 크롤링"""
#utf-8이 아니다.
import requests
from bs4 import BeautifulSoup

response = requests.get('http://news.khan.co.kr/kh_news/khan_art_view.html?\
artid=201611151529001&code=940202')
soup = BeautifulSoup(response.content)

div = soup.find('div', attrs = {'class' : 'art_body'})

contents =''
for paragraph in div.find_all('p'):
    contents += paragraph.get_text()

print contents


"""함수를 이용한 크롤링"""
import requests
from bs4 import BeautifulSoup

def get_news_title3(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content)

    title = soup.find(lambda x : x.name =='h3')

    return title.get_text()

print get_news_title3('http://media.daum.net/digital/newsview?\
newsid=20160929044237479#alex-area')


"""다음 뉴스 댓글 크롤링"""
import requests
import json

def get_news_commment(url):
    response = requests.get(url)
    data = json.loads(response.content)
    comments = [i['content'] for i in data]

result = get_news_comment('http://comment.daum.net/apis/v1/posts/16038594/comments?parentId=0&offset=0&limit=10&sort=RECOMMEND')

for com in result:
    print com


"네이버 실시간 검색 크롤링"
import requests
from bs4 import BeautifulSoup
import re

response = requests.get("http://www.naver.com")
soup = BeautifulSoup(response.content)

ranklist = soup.find('ol', attrs = {'id' : 'realrank'})
for li in ranklist.find_all('li'):
    print li.a['title']


"""가온 차트 100위 까지 크롤링"""
import requests
from bs4 import BeautifulSoup

response = requests.get("http://www.gaonchart.co.kr/main/section/chart/online.gaon")
soup = BeautifulSoup(response.content)

for td in soup.find_all('td', attrs = {'class' : 'subject'}):
    for p in td.find_all(lambda tag : tag.name == 'p' and (tag.has_attr('title'))):
        print p.get_text()


"""selenium으로 daum 뉴스 크롤링"""
from selenium import webdriver

chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.get("http://v.media.daum.net/v/20161116200216866")

title = driver.find_element_by_tag_name("h3").text
article = driver.find_element_by_class_name("article_view").find_elements_by_tag_name("p")
content = ''
for p in article:
    content += p.text

print title
print content

driver.quit()


"""인스타그램 자동 로그인 하기"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.get('https://www.instagram.com')

driver.find_element_by_class_name('_fcn8k').click()
driver.find_element_by_name('username').send_keys("hello")
driver.find_element_by_name('password').send_keys("world")
driver.find_element_by_tag_name('button').click()
