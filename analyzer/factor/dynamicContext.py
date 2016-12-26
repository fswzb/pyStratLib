# -*- coding: utf-8 -*-
#ref 动态情景多因子Alpha模型----因子选股系列研究之八
#ref https://uqer.io/community/share/57ff3f9e228e5b3658fac3ed
import numpy as np
import pandas as pd
import scipy.stats as st
from loadData import FactorLoader
from cleanData import getMultiIndexData

class DCAMAnalyzer(object):
    def __init__(self, layerFactor, factor, secReturn, tiaoCangDate, startDate='', endDate=''):
        self.__layerFactor = layerFactor
        self.__factor = factor
        self.__factorNames = [factor.name for factor in self.__factor]
        self.__secReturn = secReturn
        self.__tiaoCangDate = tiaoCangDate
        self.__startDate = startDate
        self.__endDate = endDate

    # 给定某一时间，按分层因子layerFactor把股票分为数量相同的两组（大小）
    def getGroup(self, date):
        data = getMultiIndexData(self.__layerFactor, 'tiaoCangDate', date)
        data.sort_values(ascending=True, inplace=True)     #按分层因子值从小到大排序
        secIDs = data.index.get_level_values('secID').tolist()
        group_low = secIDs[:np.round(len(data))/2]        #分组,因子值小的哪一组股票为low,高的为high
        group_high = secIDs[np.round(len(data))/2:]
        return group_low, group_high

    # 给定某一时间，和股票代码列表，返回收益序列
    def getReturn(self, secIDs, date):
        data = getMultiIndexData(self.__secReturn, 'tiaoCangDate', date, 'secID', secIDs)
        return data

    # 给定某一时间, 和股票代码列表, 返回因子列表
    def getFactor(self, secIDs, date):
        ret = pd.Series()
        for i in range(len(self.__factor)):
            data = getMultiIndexData(self.__factor[i], 'tiaoCangDate', date, 'secID', secIDs)
            ret[data.name] = data
        return ret

    # 对收益数据和因子数据做一个concat,避免因子和收益数据长度不同
    def alignData(self, returnData, factorData):
        returnDataDf = pd.DataFrame(data=returnData.values, index=returnData.index.get_level_values('secID'), columns=[returnData.name])
        factorDataDf = pd.DataFrame()
        for i in factorData.index.values:
            data = pd.DataFrame(data=factorData[i].values, index=factorData[i].index.get_level_values('secID'), columns=[i])
            factorDataDf = pd.concat([data, factorDataDf], axis=1)
        ret = pd.concat([returnDataDf, factorDataDf], axis=1).dropna()
        return ret


    def getRankIC(self):
        low = {}
        high = {}

        for i in self.__factorNames:
            low[i] = []                    #用于存储low那一组股票的rankIC
            high[i] = []                    #用于存储high那一组股票的rankIC

        for j in range(1, len(self.__tiaoCangDate)):   #对时间做循环，得到每个时间点的rankIC
            date = self.__tiaoCangDate[j]
            prevDate = self.__tiaoCangDate[j-1]
            groupLow, groupHigh = self.getGroup(date)         #分组
            returnLow = self.getReturn(groupLow, date)
            returnHigh = self.getReturn(groupHigh, date)     #得到当期收益序列
            factorLow = self.getFactor(groupLow, prevDate)
            factorHigh = self.getFactor(groupHigh, prevDate)      #得到上期因子序列
            tableLow = self.alignData(returnLow, factorLow)
            tableHigh = self.alignData(returnHigh, factorHigh)
            for k in self.__factorNames:
                tmplow, _ = st.spearmanr(tableLow['RETURN'], tableLow[k])
                tmphigh, _ = st.spearmanr(tableHigh['RETURN'], tableHigh[k])
                low[k].append(tmplow)
                high[k].append(tmphigh)

        return low, high, self.__factorNames

    def getAnalysis(self):
        low, high, colNames = self.getRankIC()
        result = pd.DataFrame(columns=colNames, index=np.arange(12))
        for i in colNames:
            meanHigh = np.array(high[i]).mean()
            meanLow = np.array(low[i]).mean()
            stdHigh = np.array(high[i]).std()
            stdLow = np.array(low[i]).std()
            # 均值的t检验, 原假设为两个独立样本的均值相同
            t, p_t = st.ttest_ind(high[i], low[i], equal_var=False)
            # 方差的F检验，原假设为两个独立样本的方差相同
            F, p_F = st.levene(high[i], low[i])
            # 分布的K-S检验，原假设为两个独立样本是否来自同一个连续分布
            ks, p_ks = st.ks_2samp(high[i], low[i])
            result[i] = [meanHigh,meanLow,stdHigh,stdLow,meanHigh/stdHigh,meanLow/stdLow,t,p_t,F,p_F,ks,p_ks]

        result = result.T
        np.arrays = [['mean','mean','std','std','IR','IR','Two sample t test','Two sample t test','levene test','levene test','K-S test',
                      'K-S test'],
                     ['high','low','high','low','high','low','t','p_value','F','p_value','KS','p_value']]
        result.columns = pd.MultiIndex.from_tuples(zip(*np.arrays))
        ret = pd.concat([result], axis=1, keys = [self.__layerFactor.name + '分层后因子表现     时间：' + self.__startDate + '--' + self.__endDate])
        return ret



if __name__ == "__main__":
    factor = FactorLoader('2015-10-05', '2015-12-31', ['CAP', 'ROE','RETURN'])
    factorData = factor.getFactorData()
    analyzer = DCAMAnalyzer(factorData['CAP'],
                            [factorData['ROE']],
                            factorData['RETURN'],
                            factor.getTiaoCangDate(),
                            startDate='2015-10-05',
                            endDate='2015-12-31')
    #print analyzer.getReturn(['603997.SH','603998.SH'],'2015-12-31')
    #print analyzer.getFactor(['603997.SH','603998.SH'],'2015-12-31')
    print analyzer.getAnalysis()



