# encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""섭씨에서 화씨 변환 함수 생성"""
def c_to_f(temper):
    f = temper * 1.8 + 32
    return f

print c_to_f(30)

"""리스트에서 홀수만 합해서 반환"""
def odd_sum(numlist):
    numsum = 0
    for num in numlist:
        if num % 2 != 0:
            numsum += num
    return numsum

def odd_sum2(numlist):
    return sum(num for num in numlist if num % 2 != 0)
print odd_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print odd_sum2([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

"""리스트에서 가장 큰 수 반환"""
def maxnum(numlist):
    return sorted(numlist)[-1]

print maxnum([3, 6, 8, 21, 8, 35, 10])


"""문자열 거꾸로 반환"""
def reversestring(var):
    return var[::-1]

print reversestring("hello")


"""factorial 출력"""
def makefact(num):
    fact = 1
    if num < 1:
        return "input error"
    else:
        while num > 1:
            fact *= num
            num -= 1
        return fact

print makefact(1)


"""숫자 리스트에서 중복 제거"""
def del_overlap(numlist):
    return list(set(numlist))

def del_overlap2(numlist):
    result = []
    for num in numlist:
        if not num in result:
            result.append(num)
    return result

print del_overlap([1, 1, 2, 3, 4, 4, 5, 2, 1])
print del_overlap2([1, 1, 2, 3, 4, 4, 5, 2, 1])


"""리스트에서 숫자 검색"""
def find_num(fnum, numlist):
    if fnum in numlist:
        return numlist.index(fnum)
    else:
        return "input error"

print find_num(0, [1, 3, 2])


"""정렬된 숫자 리스트에서 특정 숫자를 이진탐색"""
def binary_find_num(fnum, numlist):
    new_list = numlist
    new_index = 0
    while len(new_list) > 0:
        lenlist = len(new_list)
        if fnum > new_list[lenlist / 2]:
            new_list = new_list[lenlist / 2 + 1 :]
            new_index += lenlist / 2 + 1
        elif fnum < new_list[lenlist / 2]:
            new_list = new_list[: lenlist / 2]
        else:
            return new_index + len(new_list) / 2

print binary_find_num(8, [1, 2, 4, 5, 6, 7, 8, 9, 11, 12])


"""숫자 리스트의 합 구하는 재귀함수"""
def recursive_sum(numlist):
    new_numlist = numlist
    if len(new_numlist) == 1:
        return numlist[0]
    return new_numlist[-1] + recursive_sum(numlist[:-1])

def recursive_sum2(numlist, i):
    if i == len(numlist):
        return 0
    return numlist[i] + recursive_sum2(numlist, i+1)

print recursive_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print recursive_sum2([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0)


"""자리수의 합을 구하는 재귀함수"""
def place_value_sum(num, i):
    numstr = str(num)
    if len(numstr) == i:
        return 0
    return int(numstr[i]) + place_value_sum(num, i+1)

print place_value_sum(1234, 0)


"""최대공약수 찾기 재귀함수"""
def gcd(a, b):
    if a == 0:
        return b
    return gcd(b%a, a)

gcd(10, 20)


"""fiter 함수 구현"""
def filter2(func, numlist):
    newlist=[]
    for i in numlist:
        if func(i):
            newlist.append(i)
    return newlist
nums = [1, 2, 3, 4, 5, 6]
print filter2(lambda x : x % 2 == 0, nums)


"""map 함수 구현"""
def map2(func, numlist):
    newlist = []
    for i in numlist:
        newlist.append(func(i))

    return newlist

print map2(lambda x : x ** 2, nums)


"""다트를 던져 파이 값을 계산"""
import numpy as np
dart = np.random.rand(1000, 2)
inner_circle = len([[i, j] for i, j in dart if i ** 2 + j ** 2 <= 1])
pi = float(inner_circle) / 1000 * 4
print pi


"""reduce 함수 구현"""
def reduce2(func, numlist):
    if len(numlist) == 1:
        return numlist

    newlist = numlist
    newlist.append(func(newlist[0], newlist[1]))
    newlist.remove(newlist[1])
    newlist.remove(newlist[0])

    return reduce2(func, newlist)

def reduce3(func, numlist):
    new_val = numlist[0]
    for i in numlist:
        new_val = func(new_val, i)
    return new_val

print reduce2(lambda x, y : x if x > y else y, [1, 1, 2, 3, 4, 5])
print reduce3(lambda x, y : x if x > y else y, [1, 1, 2, 3, 4, 5])


"""이진탐색 재귀함수"""

def recursive_binary(fnum, numlist, reindex):
    newlist = numlist
    newindex = len(newlist) / 2
    if fnum == newlist[newindex]:
        return reindex + newindex
    elif fnum >= newlist[newindex]:
        return recursive_binary(fnum, newlist[newindex + 1 :],
        reindex + newindex + 1)
    else:
        return recursive_binary(fnum, newlist[:newindex], reindex)

print recursive_binary(7, [0, 1, 2, 3, 4, 5, 6, 7, 8], 0)
