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
m = re.search(r'0\d{2}-\d{4}-\d{4}', '010-3333-2323')
print m.group()
