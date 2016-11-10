#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""리스트에서 처음과 마지막 원소만 갖는 리스트로 변환"""
a = [1, 2, 3, 4, 5, 6]
b = [a[0], a[-1]]

print b, a[::len(a)-1]


"""리스트에서 임의의 두 원소의 합의 최대값 구하기"""
a = [1, 0, 7, 8, 2, 5, 11]
maxsum = 0
for i in range(len(a)):
    if len(a) < 2:
        print 'error length'
        break
    for j in range(i + 1, len(a)):
        if a[i] + a[j] > maxsum:
            maxsum = a[i] + a[j]
print maxsum

a_sorted = sorted(a)
print a_sorted[-1] + a_sorted[-2]


"""apple@google.com을 사용자명과 도메인으로 분리"""
email = 'apple@google.com'
email_list = email.split('@')
email_tuple = tuple(email.split('@'))
name, domain = tuple(email.split('@'))
print email_list, type(email_list)
print email_tuple, type(email_tuple)
print name, domain


"""a = {11 : 3, 4 : 9, 14 : 22, 21 : 20, 5 : 8, 2 : 23}에서 키의 최소값에 대응하는
 값과 키의 최대값에 대응하는 값을 출력"""
a = {11 : 3, 4 : 9, 14 : 22, 21 : 20, 5 : 8, 2 : 23}
maxval = 0
minval = 0
key = sorted(a.keys())
maxval = a[key[-1]]
minval = a[key[0]]
print maxval, minval


"""문장 translate"""
translater = {'This' : 'Este', 'is' : 'es', 'python' : 'piton'}

sent = 'This is python'
sent_space = sent.split(' ')
pre_new_sent = []
for voc in sent_space:
    pre_new_sent.append(translater[voc])
print ' '.join(pre_new_sent)
print 'This is python'.replace('This',translater['This']).replace('is',
       translater['is']).replace('python', translater['python'])


"""다음 집합의 전체 학생 중 두과목 모두 듣는  학생의 비율"""
english = {'Aaron', 'Tracy', 'David', 'Grant', 'Michael', 'Tim'}
math = {'Aaron', 'David', 'Smith', 'Bill', 'Tim', 'Cathy', 'Carl'}

overall = len(english | math)
intersect = len(english & math)
print float(intersect) / overall * 100
