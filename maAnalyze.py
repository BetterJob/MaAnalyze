#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:02:03 2019

@author: gtl
"""

import pandas as pd
import numpy as np

bl = 5
dict_sc = {'CLOSE_MA5':['S_DQ_CLOSE','MA5','%',bl]
        ,'CLOSE_MA10':['S_DQ_CLOSE','MA10','%',bl]
        ,'CLOSE_MA20':['S_DQ_CLOSE','MA20','%',bl]
        ,'CLOSE_MA30':['S_DQ_CLOSE','MA30','%',bl]
        ,'CLOSE_MA60':['S_DQ_CLOSE','MA60','%',bl]
        ,'MA5_MA5':['MA5','MA10','%',bl]
        ,'MA10_MA20':['MA10','MA20','%',bl]
        ,'MA20_MA30':['MA20','MA30','%',bl]
        ,'MA30_MA60':['MA30','MA60','%',bl]
        }

#定义打分函数 arr含有对应数据的一维数组
def get_score(arr,lev):
    score = 0
    for i in dict_sc.keys():
        dif = arr[dict_sc[i][0]] - arr[dict_sc[i][1]]
        if dict_sc[i][2] == '%':
            dif = int(dif/arr[dict_sc[i][1]]*100)
        #if dif < 0:
        #    dif *= 2
        if lev > 0:
            score += dif*lev
        else:
            score += dif*dict_sc[i][3]
    return score
#根据评分得到仓位
def get_Posion(sco):
    if sco < 0:
        return 0
    elif sco > 100:
        return 10
    else:
        return int(sco/10)
#数据处理
def get_PortDetail(df,lev):
    #对数据当前状态进行打分
    #df['POS'] = df.apply(lambda x: sc.get_Posion(sc.get_score(x)), axis = 1)
    df['POS'] = df.apply(lambda x: get_Posion(get_score(x,lev)), axis = 1)
    
    #print(df[['TRADE_DT','MA5','POS']])
    
    #计算该模式下的收益率 注意当日的仓位下一日才能算收益
    lastPos = df['POS'].copy()
    df = df.drop(0) #删除首行
    df = df.reset_index(drop = True)
    
    df['LastPos'] = lastPos
    #计算收益率的方法还需要改善，考虑仓位成本变化
    df['YIELD_PORT'] = df.apply(lambda x: x['YIELD']*x['LastPos']/10+1, axis = 1)
    df['YEAR'] = df.apply(lambda x: int(x['TRADE_DT']/10000), axis = 1) 
    return df

if __name__ == '__main__':   #hs300_2016  FISP
    ret = np.array([])
    #读取处理好的数据
    df = pd.read_csv('maData.csv')
    for i in np.arange(1,10,0.1):
        print('i=',i)
        ret = np.append(ret,i)
        df = get_PortDetail(df,i)
        ret = np.append(ret,df['YIELD_PORT'].prod()-1)
    ret = ret.reshape([-1,2])#转换成两列
    print(ret)
    np.savetxt('b.txt',ret,fmt='%.4f')
    idx = np.where(ret==np.max(ret,0))#每列最大的索引
    #最大收益率对应的key值
    maxdf = get_PortDetail(df,ret[idx[0][0],0])
    tjdf = maxdf.groupby(['YEAR'])['YIELD_PORT'].prod()-1
    print(tjdf)
    maxdf.to_excel('maxdf.xlsx','Sheet1')
    #取最大收益率
    """maxret = np.amax(ret,0)
    print('maxret=',maxret)
    maxdf = get_PortDetail(df,maxret[0])
    tjdf = maxdf.groupby(['YEAR'])['YIELD_PORT'].prod()-1
    print(tjdf)"""
    """    
    #数据处理
    df = get_PortDetail(df)
    #计算每年的收益率
    #tjdf = df.groupby(['YEAR'])['YIELD_PORT'].prod()-1
    #print(tjdf.T)
    
    print(df['YIELD_PORT'].prod()-1)
    #print(df.loc[(df['TRADE_DT']>20050101) & (df['TRADE_DT']<20161231) ])
    
    #保存结果
    #df.to_excel('test1.xlsx','Sheet1')"""
    
     
    print('##################')
