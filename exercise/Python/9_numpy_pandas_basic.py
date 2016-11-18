#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""find the value of  Math.pi by using numpy"""
print np.pi

x = np.random.rand(1000)
y = np.random.rand(1000)

x_y = np.sqrt(x**2 + y**2)
inner_circle = x_y[x_y <= 1]
quarter_pi = float(len(inner_circle)) / 1000
cal_pi = quarter_pi * 4

print cal_pi


"""make matrix multiplication by using list"""
A = [[1, 2, 3], [4, 5, 6]]
B = [[1, 2], [3, 4] ,[5, 6]]

result = []

for t, i in enumerate(A):
    r_result = []
    for k in range(len(B[0])):
        val_result = 0
        for t2, j in enumerate(i):
            val_result += j * B[t2][k]
        r_result.append(val_result)
    result.append(r_result)
print result


"""handwritten image recognition by svm"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn import svm

df = pd.read_csv("./sample/9_pandas/data.csv", header = 0)

y = df["label"]
x = df.drop(["label"], axis = 1)

x = np.array(x)
y = np.array(y)

x_train = x[:999]
y_train = y[:999]

x_test = x[1000:1200]
y_test = y[1000:1200]

classifier = svm.SVC(gamma = 0.001, C=100.)

classifier.fit(x_train, y_train)

print classifier.score(x_test, y_test)
#bad score

print classifier.predict(x_test[1])
reshaped_example = x_test[1].reshape(28, 28)
plt.imshow(reshaped_example, cmap = cm.Greys_r)
plt.show()
