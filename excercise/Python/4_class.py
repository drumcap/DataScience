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
        return "kor is {}, eng is {}, math is {}".format(self.kor, self.eng, self.math)

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
            if self.videos[video] >= (dt.datetime.now().date() - dt.timedelta(days = 7)):
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
