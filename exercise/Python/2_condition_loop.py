#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""구구단을 2-9단까지 출력"""
for i in range(1,10):
    for j in range(1,10):
        print i, '*', j, '=', i * j


"""1-100까지 정수 중 2의 배수와 11의 배수 모두 출력"""
num2_11 = []
for i in range(1,101):
    if i % 2 ==0 or i % 11 == 0:
        num2_11.append(i)
print num2_11


"""a=[22, 1, 3, 4, 7, 98, 21, 55, 87, 99, 19, 20, 45]에서 최대값 최소값 찾기
(sorted, sort 사용x)"""
a=[22, 1, 3, 4, 7, 98, 21, 55, 87, 99, 19, 20, 45]

maxnum = a[0]
minnum = a[0]

for i in a:
    if i > maxnum:
        maxnum = i
    elif i < minnum:
        minnum = i

print maxnum, minnum


"""a=[22, 1, 3, 4, 7, 98, 21, 55, 87, 99, 19, 20, 45]에서 평균 구하기"""
a=[22, 1, 3, 4, 7, 98, 21, 55, 87, 99, 19, 20, 45]
numsum = 0
for i in a:
    numsum += i
print float(numsum) / len(a)


"""15번째가지 피보나치 수열 출력"""
f = [1, 1]

for i in range(2,15):
    #lf = len(f)
    new_f = f[i-1] + f[i-2]
    f.append(new_f)
print f



"""Celsius = [39.2, 36.5, 37.3, 37.8], F = (9/5) * C + 32 comprehension으로
화씨 변환"""
Celsius = [39.2, 36.5, 37.3, 37.8]
Fahrenheit = [float(9/5) * c + 32 for c in Celsius]
print Fahrenheit


"""띄어쓰기 개수"""
sent = 'Today is very nice and I want to go out for dinner'
count_blank = len([c for c in sent if c == " "])
print count_blank


"""모음 제거"""
sent = 'Today is very nice and I want to go out for dinner'
vowel = 'aeiou'
new_sent = ["" if c in vowel else c for c in sent ]
new_sent2 = [c for c in sent if not c in vowel]
print ''.join(new_sent), ''.join(new_sent2)


"""1-1000 중 소수만 출력"""
prime_num = []
for i in range(1, 1001):
    switch = 0
    if i == 1:
        continue
    if i == 2:
        prime_num.append(i)
        continue
    for j in range(2, (i + 1) / 2 + 1):
        if i % j == 0:
            switch = 1
    if switch == 0:
        prime_num.append(i)
print prime_num


"""1-9000 까지 정수 중 palindrome의 개수"""
palinum = []
for i in range(1,9001):
    if str(i) == str(i)[::-1]:
        palinum.append(i)
print palinum
