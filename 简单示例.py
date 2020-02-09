# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:58:38 2020

@author: DELL
"""

import tensorflow as tf
import numpy as np

#使用numpy生成100个随机点
x_data = np.random.rand(100)
#y_data = x_data * 0.1 + 0.3 
y_data = x_data*x_data * 0.1 + 0.3

#构造一个线性模型
k = tf.Variable(0.)
b = tf.Variable(0.)
#print(k,b)
#y = k * x_data + b
y = k*x_data*x_data + b

#二次代价函数
loss = tf.reduce_mean(tf.square(y_data-y))
#定义一个梯度下降法来进行训练的优化器
optimizer = tf.train.GradientDescentOptimizer(0.2)
#最小化代价函数
train = optimizer.minimize(loss)

#初始化变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    
    for i in range(500):
        sess.run(train)
        if i % 20 == 0:
            print(i,sess.run([k,b]))
            