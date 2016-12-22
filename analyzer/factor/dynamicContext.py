# -*- coding: utf-8 -*-
#ref 动态情景多因子Alpha模型----因子选股系列研究之八
#ref https://uqer.io/community/share/57ff3f9e228e5b3658fac3ed
import numpy as np
import pandas as pd
import scipy.stats as st
from loadData import FactorLoader

class DCAMAnalyzer(object):
    def __init__(self, layerFactor, factor, secReturn, tiaoCangDate):
        self.__layerFactor = layerFactor
        self.__factor = factor
        self.__secReturn = secReturn
        self.__tiaoCangDate = tiaoCangDate

    # 给定某一时间，按分层因子layerFactor把股票分为数量相同的两组（大小）
    def getGroup(self, date):
        data = self.__layerFactor.loc[self.__layerFactor.index.get_level_values('tiaoCangDate') == date]
        data.sort_values(ascending=True, inplace=True)     #按分层因子值从小到大排序
        secIDs = data.index.get_level_values('secID').tolist()
        group_low = secIDs[:np.round(len(data))/2]        #分组,因子值小的哪一组股票为low,高的为high
        group_high = secIDs[np.round(len(data))/2:]
        return group_low, group_high

    # 给定某一时间，和股票代码列表，返回收益序列
    def getReturn(self, secIDs, date):
        data = self.__secReturn.loc[self.__secReturn.index.get_level_values('tiaoCangDate') == date]
        data = data.loc[data.index.get_level_values('secID').isin(secIDs)]
        ret = pd.DataFrame(data=data.values, index=data.index.get_level_values('secID'), columns=[data.name])
        return ret

    # 给定某一时间, 和股票代码列表, 返回因子列表
    def getFactor(self, secIDs, date):
        ret = pd.DataFrame()
        for i in range(len(self.__factor)):
            data = self.__factor[i].loc[self.__factor[i].index.get_level_values('tiaoCangDate') == date]
            data = data.loc[data.index.get_level_values('secID').isin(secIDs)]
            data = pd.DataFrame(data=data.values, index=data.index.get_level_values('secID'), columns=[data.name])
            ret = pd.concat([ret, data], axis=1)
        return ret


    def getRankIC(self):
        low = {}
        high = {}

        for i in range(len(self.__factor)):
            low[i] = []                    #用于存储low那一组股票的rankIC
            high[i] = []                    #用于存储high那一组股票的rankIC

        for j in range(1, len(self.__tiaoCangDate)):   #对时间做循环，得到每个时间点的rankIC
            date = self.__tiaoCangDate[j]
            prevDate = self.__tiaoCangDate[j-1]
            groupLow, groupHigh = self.getGroup(date)         #分组
            returnsLow = self.getReturn(groupLow, date)
            returnsHigh = self.getReturn(groupHigh, date)     #得到当期收益序列
            factorLow = self.getFactor(groupLow, prevDate)
            factorHigh = self.getFactor(groupHigh, prevDate)      #得到上期因子序列
            tableLow = pd.concat([returnsLow, factorLow], axis=1).dropna() #此处做一个concat,避免因子和收益数据长度不同
            tableHigh = pd.concat([returnsHigh, factorHigh], axis=1).dropna()
            for k in range(len(self.__factor)):
                tmplow,_ = st.spearmanr(tableLow['RETURN'], tableLow[self.__factor[k].name])
                tmphigh,_ = st.spearmanr(tableHigh['RETURN'], tableHigh[self.__factor[k].name])
                low[k].append(tmplow)
                high[k].append(tmphigh)

        return low, high


if __name__ == "__main__":
    factor = FactorLoader('2015-10-05', '2015-12-31', ['CAP', 'ROE','RETURN'])
    factorData = factor.getFactorData()
    analyzer = DCAMAnalyzer(factorData['CAP'], [factorData['ROE']], factorData['RETURN'], factor.getTiaoCangDate())
    #print analyzer.getReturn(['603997.SH','603998.SH'],'2015-12-31')
    #print analyzer.getFactor(['603997.SH','603998.SH'],'2015-12-31')
    print analyzer.getRankIC()



