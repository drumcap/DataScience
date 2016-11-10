#encoding:utf=8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""Circle class 작성"""
import numpy as np

class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    def get_area(self):
        return np.pi * (self.radius ** 2)

    def get_length(self):
        return np.pi * self.radius * 2

cir1 = Circle(4)
print cir1.get_area()


"""BankAccount class 작성"""
class BankAccount(object):
    def __init__(self, amount):
        self.amount = amount

    def withdraw(self, amount):
        self.amount -= amount
        return "amount is {}".format(self.amount)

    def save(self, amount):
        self.amount += amount
        return "amount is {}".format(self.amount)

    def check(self):
        return "amount is {}".format(self.amount)

    def check_interest(self, m_interest, month):
        return self.amount * (1 + m_interest) ** month

p1 = BankAccount(4000)
print p1.amount
print p1.withdraw(300)
print p1.amount
print p1.save(500)
print p1.check()
print p1.check_interest(0.3, 2)


"""성적 관리 class 작성"""
class StudentScore(object):
    def __init__(self, kor, eng, math):
        self.kor = float(kor)
        self.eng = float(eng)
        self.math = float(math)

    def printscore(self):
        return "kor is {}, eng is {}, math is {}".format(self.kor,
                                                    self.eng, self.math)

    def average(self):
        return "average is {}".format((self.kor + self.eng + self.math) / 3)

alex = StudentScore(20, 30, 40)
print alex.printscore()
print alex.average()


"""비디오가게 관리 class 작성"""
import datetime as dt

class VideoStore(object):
    def __init__(self):
        self.videos = {}

    def add_video(self, video, date = None):
        if video in self.videos:
            return "already exist."
        else:
            if date == None:
                self.videos[video] = dt.datetime.now().date()
            else:
                self.videos[video] = date

    def find_video(self, video):
        if video in self.videos:
            return "The date is {}".format(self.videos[video])
        else:
            return "No video"

    def is_new_release(self, video):
        if not video in self.videos:
            return "There is no such video"
        else:
            if self.videos[video] >= (dt.datetime.now().date() -
                                      dt.timedelta(days = 7)):
                return "Yes. this is new."
            else:
                return "NO."

jumbo = VideoStore()
print jumbo.videos
jumbo.add_video("a")
print jumbo.videos
print jumbo.find_video("a")
print jumbo.find_video("b")
jumbo.add_video("b", dt.date(2016, 10, 9))
print jumbo.videos
print jumbo.is_new_release("a")
print jumbo.is_new_release("b")


"""Word객채를 길이 순으로 정렬"""
class Word(object):
    def __init__(self, text):
        self.text = text

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return "Word('" + self.text + "')"

    def getitem(self):
        return self.text[1]


w1 = Word("alex")
w2 = Word("james")
w3 = Word("tonjong")
w4 = Word("ken")

words = [w1, w2, w3, w4]
print sorted(words, key = lambda x : len(x))
print sorted(words, key = lambda x : x.getitem())


"""복소수 class 정의"""
import numpy as np

class Complex(object):
    def __init__(self, re, im):
        self.re = re
        self.im = im

    def __str__(self):
        if self.im > 0:
            return str(self.re) + "+" + str(self.im) + "j"
        elif self.im < 0:
            return str(self.re) + str(self.im) + "j"
        else:
            return str(self.re)

    def __repr__(self):
        if self.im > 0:
            return str(self.re) + "+" + str(self.im) + "j"
        elif self.im < 0:
            return str(self.re) + str(self.im) + "j"
        else:
            return str(self.re)

    def size(self):
        return np.sqrt(self.re ** 2 + self.im ** 2)

    def __add__(self, complex2):
        return Complex(self.re + complex2.re, self.im + complex2.im)

    def __sub__(self, complex2):
        return Complex(self.re - complex2.re, self.im - complex2.im)

    def __mul__(self, complex2):
        return Complex(self.re * complex2.re - self.im * complex2.im,
                       self.re * complex2.im + self.im * complex2.re)

    def __eq__(self, complex2):
        return self.re == complex2.re and self.im == complex2.im

    def __ne__(self, complex2):
        return self.re != complex2.re or self.im != complex2.im

    def __ge__(self, complex2):
        return self.size() >= complex2.size()

    def __le__(self, complex2):
        return self.size() <= complex2.size()

    def __lt__(self, complex2):
        return self.size() < complex2.size()

    def __gt__(self, complex2):
        return self.size() > complex2.size()

cnum1 = Complex(1, 3)
cnum2 = Complex(1, -2)

print cnum1
print cnum2
print cnum1.size()
print cnum1 - cnum2
print cnum1 * cnum2
print cnum1 != cnum2
print cnum1 > cnum2
print cnum1 <= cnum2


"""리스트에서 가장 큰 부분합 구하기"""
def partial_sum(numlist):
    maxsum = 0

    for i in range(2, len(numlist) + 1):
        j = 0
        while i + j <= len(numlist):
            if maxsum < sum(numlist[j : j + i]):
                maxsum = sum(numlist[j : j + i])
            j += 1
    return maxsum

print partial_sum([1, 2, -3, 4])


"""문자열 수식 계산 class
class StrCalculate(object):
    def __init__(self, formula):
        self.formula = formula

    def get_value(self):
        return

f1 = StrCalculate('1 + 4 x 6')
print f1.get_value()
"""


"""Calculator class 작성"""
class Calculator(object):
    def __init__(self, num1, num2, func):
        self.num1 = num1
        self.num2 = num2
        self.func = func

    def applyto(self):
        return self.func(self.num1, self.num2)

def addto(n1, n2):
    return n1 + n2

c1 = Calculator(2, 3, addto)
c2 = Calculator(2, 3, lambda x, y : x * y)
print c1.applyto()
print c2.applyto()


"""MusicChart class 작성"""
from collections import defaultdict
from collections import OrderedDict

class MusicChart(object):
    def __init__(self):
        self.songs = defaultdict(int)

    def listen(self, music):
        self.songs[music] += 1

    def rank(self, music):
        song_rank = OrderedDict(sorted(self.songs.items(), key = lambda x : x[1], reverse = True))
        #print songrank
        for i, j in enumerate(song_rank):
            if j == music:
                return i + 1

m1 = MusicChart()
print m1.songs
m1.listen("First")
m1.listen("First")
m1.listen("Second")
m1.listen("First")
m1.listen("Third")
m1.listen("Second")
print m1.rank("First")


"""학생의 이름, 나이, 전공 class 생성"""
class Student(object):
    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major


"""같은 내용의 namedtuple 생성"""
from collections import namedtuple

student = namedtuple('stu', ['name', 'age', 'major'])

s1 = student('alex', 15, 'programming')
print s1
