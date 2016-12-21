# -*- coding: utf-8 -*-
#ref 动态情景多因子Alpha模型----因子选股系列研究之八
#ref https://uqer.io/community/share/57ff3f9e228e5b3658fac3ed
import numpy as np
from loadData import FactorLoader


class DCAMAnalyzer(object):
    def __init__(self, layerFactor, factor, secReturn, startDate='', endDate=''):
        self.__layerFactor = layerFactor
        self.__factor = factor
        self.__secReturn = secReturn
        self.__startDate = startDate
        self.__endDate = endDate

    # 给定某一时间，按分层因子layerFactor把股票分为数量相同的两组（大小）
    def getGroup(self, date):
        try:
            data = self.__layerFactor.loc[self.__layerFactor.index.get_level_values('tiaoCangDate') == date]
        except:
            raise ValueError("Failed to retrieve layer factor data")
        data.sort(ascending=True,inplace=True)     #按分层因子值从小到大排序
        secIDs = data.index.get_level_values('secID').tolist()
        group_low = secIDs[:np.round(len(data))/2]        #分组,因子值小的哪一组股票为low,高的为high
        group_high = secIDs[np.round(len(data))/2:]
        return group_low, group_high

    # 给定某一时间，和股票代码列表，返回收益序列
    def getReturn(self, secIDs, date):
        data = self.__secReturn[date]
        data = data[data.index.isin(secIDs)]
        return data

    # 给定某一时间, 股票代码列表, 返回因子列表
    def getFactor(self, secIDs, date):
        data = self.__factorData[date].ix[secIDs]
        data.set_index('secID', inplace=True)


        return data


    def getRankIC(self):
        low = {}
        high = {}

        return low, high


if __name__ == "__main__":
    factor = FactorLoader('2015-01-05', '2015-12-30', ['CAP', 'ROE','RETURN'])
    factorData = factor.getFactorData()
    analyzer = DCAMAnalyzer(factorData['CAP'], factorData['ROE'], factorData['RETURN'])
    print factorData['RETURN']
    print analyzer.getReturn(['000818.SZ','000819.SZ'],'2015-12-31')



