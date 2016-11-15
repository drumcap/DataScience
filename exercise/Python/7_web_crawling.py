#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""주소를 통해 좌표 추출"""
import requests
import json
from exer_connection import Api_key_google_map

api_end_point = 'https://maps.googleapis.com/maps/api/geocode/json?address=서울특별시 양천구 목동 현대월드타워&key=' + Api_key_google_map

res = requests.get(api_end_point)
data = json.loads(res.text)
print data['results'][0]['geometry']['location']
