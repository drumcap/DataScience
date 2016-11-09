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


"""sorted 함수 구현"""
def sorted2(numlist, key):
    for tnum1 in range(len(numlist)):
        for tnum2 in range(len(numlist)):
            if tnum1 >= tnum2:
                continue
            if key(numlist[tnum1]) >= key(numlist[tnum2]):
                temp = numlist[tnum1]
                numlist[tnum1] = numlist[tnum2]
                numlist[tnum2] = temp

    return numlist

nums = [('a', 3), ('c', 2), ('e', 6), ('b', 1)]
print sorted2(nums, key = lambda x : x[1])


"""완전수 판별 함수"""
def perfectnum(num):
    aliquot = []
    for i in range(1, num):
        if num % i == 0:
            aliquot.append(i)
    if sum(aliquot) == num:
        return "correct"
    else:
        return "No Perfect number"

print perfectnum(7)


"""서로소 판별 함수"""
def relative_prime(num1, num2):
    aliquot1 = []
    aliquot2 = []
    for i in range(2, num1 + 1):
        if num1 % i == 0:
            aliquot1.append(i)
    for j in range(2, num2 + 1):
        if num2 % i == 0:
            aliquot2.append(j)
    for k in aliquot1:
        if k in aliquot2:
            return "No relative prime"
    return "relative prime"

def relative_prime2(num1, num2):
    for i in range(2, num1 + 1):
        if num1 % i == 0 and num2 % i == 0:
            return "No relatice prime"
    return "relative prime"

print relative_prime(3, 7)
print relative_prime2(3, 7)


"""anagram 확인 함수"""
from collections import Counter

def is_anagram(char1, char2):
    count1 = Counter(char1)
    count2 = Counter(char2)
    for key1 in count1:
        if not count1[key1] == count2[key1]:
            return "not anagram"
    return "anagram"

def is_anagram2(char1, char2):
    return sorted(char1) == sorted(char2)

print is_anagram("hello", "olle")
print is_anagram2("hello", "olle")


"""암호화 및 복호화"""
key = {'a':'n', 'b':'o', 'c':'p', 'd':'q', 'e':'r', 'f':'s', 'g':'t', 'h':'u',
       'i':'v', 'j':'w', 'k':'x', 'l':'y', 'm':'z', 'n':'a', 'o':'b', 'p':'c',
       'q':'d', 'r':'e', 's':'f', 't':'g', 'u':'h', 'v':'i', 'w':'j', 'x':'k',
       'y':'l', 'z':'m', 'A':'N', 'B':'O', 'C':'P', 'D':'Q', 'E':'R', 'F':'S',
       'G':'T', 'H':'U', 'I':'V', 'J':'W', 'K':'X', 'L':'Y', 'M':'Z', 'N':'A',
       'O':'B', 'P':'C', 'Q':'D', 'R':'E', 'S':'F', 'T':'G', 'U':'H', 'V':'I',
       'W':'J', 'X':'K', 'Y':'L', 'Z':'M'}

def encode_f(char):
    new_word = ""
    for c in char:
        new_word += key[c]
    return new_word

def decode_f(char):
    new_word = ""
    new_key_dict = {}

    for i, j in key.items():
        new_key_dict[j] = i

    for c in char:
        new_word += new_key_dict[c]
    return new_word

print encode_f("Hello")
print decode_f(encode_f("Hello"))
