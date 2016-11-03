#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""일주일은 몇 초 인가"""
week_to_sec = 60 * 60 * 24 * 7
print week_to_sec


"""구구단 7단을 계산하여 답을 순서대로 출력하시오"""
for i in range(1,10):
    print "7 * {0} = {1}".format(i, 7 * i)


"1에서 11까지의 합을 구하시오"
numsum = 0
for i in range(1,12):
    numsum += i
print numsum


"우사인 볼트는 100m를 9.5초에 뛰었습니다. 평균 시속(km/h)은?"
print 100.0 / 1000 / 9.5 * 3600


"반지름이 10cm인 원의 넓이와 둘레를 출력하세요"
import numpy as np
print np.pi * 2 * 0.1 , np.pi * 0.1**2


"a='python is great language'에서 소문자p를 대문자P로 변경"
a='python is great language'
a1= a.replace("p","P")
print a1
print a[0].upper() + a[1:]
