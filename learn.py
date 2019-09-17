#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 21:37:24 2019

@author: gtl
"""
import numpy as np

a = np.arange(6).reshape((2,3))
print('a=',a)
print('全局最大=',np.max(a)) 
print('每列最大=',np.max(a,axis=0)) 
print('每行最大=',np.max(a,axis=1)) 

#然后用where得到最大值的索引，返回值中，前面的array对应行数，后者对应列数
idx_max = np.where(a==np.max(a,axis=0))#列最大值对应索引
print('列最大值对应索引：',idx_max)
print('列最大值对应索引的行标：',idx_max[0][0]) 
print('列最大值对应索引的列标：',idx_max[1]) 
print('第二列最大值所在行对应的第一列数据：',a[idx_max[0][0],idx_max[1][0]]) 
#如果array中有相同的最大值，where会将其位置全部给出
a[1,0]=2
print('anew=',a)
print(np.where(a==np.max(a)))
