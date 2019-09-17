#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 09:58:18 2019

@author: gtl
"""
dict_sc = {'CLOSE_MA5':['S_DQ_CLOSE','MA5','%',1]
        ,'CLOSE_MA10':['S_DQ_CLOSE','MA10','%',1]
        ,'CLOSE_MA20':['S_DQ_CLOSE','MA20','%',2]
        ,'CLOSE_MA30':['S_DQ_CLOSE','MA30','%',2]
        ,'CLOSE_MA60':['S_DQ_CLOSE','MA60','%',2]
        ,'MA5_MA5':['MA5','MA10','%',1]
        ,'MA10_MA20':['MA10','MA20','%',1]
        ,'MA20_MA30':['MA20','MA30','%',2]
        ,'MA30_MA60':['MA30','MA60','%',2]
        }

#定义打分函数 arr含有对应数据的一维数组
def get_score(arr):
    score = 0
    for i in dict_sc.keys():
        dif = arr[dict_sc[i][0]] - arr[dict_sc[i][1]]
        if dict_sc[i][2] == '%':
            dif = int(dif/arr[dict_sc[i][1]]*100)
        if dif < 0:
            dif *= 2
        score += dif*dict_sc[i][3]
    return score

def get_Posion(sco):
    if sco < 0:
        return 0
    elif sco > 100:
        return 10
    else:
        return int(sco/10)
    
        
if __name__ == '__main__':   #hs300_2016  FISP
    t = {'S_DQ_CLOSE':1000,'MA5':990,'MA10':970,'MA20':940,'MA30':900,'MA60':850}
    print(get_score(t))
    print(111)