# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 15:48:18 2020

@author: DELL
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


'''
矩阵相乘
m1 = tf.constant([[3,3]])
m2 = tf.constant([[2],[3]])

product = tf.matmul(m1,m2)

with tf.Session() as sess:
    print(sess.run(product))
'''

'''
变量
x = tf.Variable([1,2])
y = tf.constant([3,3])

#增加一个减法op
sub = tf.subtract(x,y)
#增加一个加法op
add = tf.add(x,y)
new_data = tf.add(x,1)

#增加一个赋值op
updata = tf.assign(x,new_data)

# 全局变量初始化
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(sub))
    print(sess.run(add))
    #变量自加
    for _ in range(5):
        print(sess.run(updata))
'''

'''
#fetch feed

#fetch -> 可以同时执行多个op
input1 = tf.constant(4.0)
input2 = tf.constant(3.0)
input3 = tf.constant(2.0)

add = tf.add(input1,input2)
mul = tf.multiply(input3,add)

with tf.Session() as sess:
    for _ in range(5):
        print(sess.run([mul,add])) 
        
#feed
#创建占位符
input4 = tf.placeholder(tf.float32)
input5 = tf.placeholder(tf.float32)

output = tf.multiply(input4,input5)

with tf.Session() as sess:
    #feed 的数据以字典的形式传入
    print(sess.run(output,feed_dict = {input4:[1.2],input5:[2.0]}))
'''

#线性回归
#使用numpy生成200个随机点
x_data = np.linspace(-0.5,0.5,200)[:,np.newaxis]
noise = np.random.normal(0,0.02,x_data.shape)
y_data = np.square(x_data) + noise

#定义两个placeholder
x = tf.placeholder(tf.float32,[None,1])
y = tf.placeholder(tf.float32,[None,1])

#定义神经网络中间层
Weights_L1 = tf.Variable(tf.random.normal([1,10]))
biases_L1 = tf.Variable(tf.zeros([1,10]))
Wx_plus_b_L1 = tf.matmul(x,Weights_L1) + biases_L1
L1 = tf.nn.tanh(Wx_plus_b_L1) # 双曲正切线

#定义神经网络输出
Weights_L2 = tf.Variable(tf.random.normal([10,1]))
biases_L2 = tf.Variable(tf.zeros([1,1]))
Wx_plus_b_L2 = tf.matmul(L1,Weights_L2) + biases_L2
prediction = tf.nn.tanh(Wx_plus_b_L2)

#二次代价函数
loss = tf.reduce_mean(tf.square(y-prediction))
#梯度下降训练法
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

with tf.Session() as sess:
    #变量初始化
    sess.run(tf.global_variables_initializer())
    for _ in range(2000):
        sess.run(train_step,feed_dict = {x:x_data,y:y_data})
        
    #获得预测值
    prediction_value = sess.run(prediction,feed_dict = {x:x_data})
    
    #画图
    plt.figure()
    plt.scatter(x_data,y_data) #绘制点
    plt.plot(x_data,prediction_value,'y-',lw = 5)
    plt.show()
        



 














