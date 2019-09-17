#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 16:03:30 2019
数据预处理，计算得到均值数据
@author: gtl
"""
import pandas as pd
#import numpy as np
import datetime as time

#程序耗时统计 st1:起始时间  name:名称
def time_between(st1, name):
    st2 = time.datetime.now()
    print(name,st2-st1)


#定义均线字典
#dict_ma = {'MA5' :5}
dict_ma = {'MA5' :5,'MA10':10,'MA20':20,'MA30':30,'MA60':60}

#读取数据文件
orgdf = pd.read_csv('/Users/gtl/Downloads/000300.csv')
#取需要的数据列
df = pd.DataFrame(orgdf, columns=['TRADE_DT', 'S_DQ_PRECLOSE','S_DQ_CLOSE', 'S_DQ_VOLUME'])

#去除脏数据
df = df[pd.notnull(df['S_DQ_VOLUME'])]
df = df.reset_index(drop=True)
#print(df)
#预处理得到各类均线数据

#方法一：遍历df  貌似是很蠢的方法。。。效率很低
print(df.index)#da.shape[0]
#rows = df.shape[0] #取行数  df.shape[1]取列数
time1 = time.datetime.now()#time.clock()
for i in df.index:
    for j in dict_ma.keys():
        start = max(0,i-dict_ma[j]+1) #计算起始位置
        #df.loc[df.index[i],j] =df[start:i]['S_DQ_CLOSE'].mean()#df[start:i]实际上不包含i行
        #计算价格均线
        df.loc[df.index[i],j] =df.loc[start:i,'S_DQ_CLOSE'].mean()#df.loc[start:i,'S_DQ_CLOSE']包含i行
        #计算成交量均线
        df.loc[df.index[i],j+'_VOL'] =df.loc[start:i,'S_DQ_VOLUME'].mean()
time_between(time1, '预处理均线耗时：')
"""
#方法二 尝试用apply函数 dat:数据 s:开始位置 e:结束位置 col:列名
def function(dat, s, e, col):
	return dat.loc[s:e,col].mean()

df['MA5'] = df.apply(lambda x: function(x.index, x.), axis = 1)
"""
#计算指数当日收益率
df['YIELD'] = df.apply(lambda x: x['S_DQ_CLOSE']/x['S_DQ_PRECLOSE']-1, axis = 1)

#查看计算结果
#print(df[['TRADE_DT','MA5','MA10','MA20','MA30','MA60']])
#print(df[['TRADE_DT','MA5_VOL','MA10_VOL','MA20_VOL','MA30_VOL','MA60_VOL']])
#print(df[['TRADE_DT','MA5','MA5_VOL']])

df.to_csv('maData.csv',',')

