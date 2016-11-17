#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""n보다 작거나 같은 모든 소수를 반환하는 함수"""
def prime_n(num):
    if num < 1:
        yield "wrong input"

    if num >= 1:
        yield 1

        if num >= 2:
            yield 2

            if num >= 3:
                for i in xrange(3, num + 1 ):
                    k = 0
                    for j in xrange(2, i):
                        if i % j == 0:
                            k = 1
                    if k == 0:
                        yield i

for i in prime_n(15):
    print i,


"""generator range 함수 만들기"""
def range2(start, end):
    if end <= start:
        yield "incorrect parameter"
    else:
        while start < end:
            yield start
            start += 1

a = range2(3, 6)
for i in a:
    print i

for i in a:
    print i


"""함수 호출 시 parameter 정보를 출력하는 decorator"""
def deco_parm(func):
    def deco_parm2(*args):
        result = []
        for arg in args:
            result.append(arg)
        return "parm_val:{0}, parm_cnt:{1}, result:{2}".format(result, len(args), func(*args))
    return deco_parm2


@deco_parm
def make_sentence(a, b, c, d):
    return a + " " + b + " " + c + " " + d

make_sentence("My", "name", "is", "alex")
