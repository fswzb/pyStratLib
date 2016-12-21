# -*- coding: utf-8 -*-
from utils import dateutils
import cleanData
import pandas as pd

_factorPathDict ={
    'NAV': ['..//..//data//factor//net_asset.csv', True], # 净资产
    'ROE': ['..//..//data//factor//ROE.csv',True], # 净资产收益率
    'PE': ['..//..//data//factor//PE_TTM.csv', True], # 市盈率
    'TTM': ['..//..//data//factor//TTM.csv', True], # 销售毛利率
    'CAP': ['..//..//data//factor//cap.csv', True], # 总市值
    'RETURN': ['..//..//data//return//monthlyReturn.csv', False] #月度收益
}


class FactorLoader(object):
    def __init__(self, startDate, endDate, factorNames, freq='m'):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__factorNames = factorNames
        self.__freq = freq
        self.__tiaocangDate = []
        self.__nbFactor = len(factorNames)

    def getTiaoCangDate(self):
        return dateutils.getPosAdjDate(self.__startDate, self.__endDate, freq=self.__freq)

    def getFactorData(self):
        ret = pd.Series()
        for name in self.__factorNames:
            pathToUse = _factorPathDict[name][0]
            needAdjDate = _factorPathDict[name][1]
            if needAdjDate:
                factorRaw = cleanData.getUniverseSingleFactor(pathToUse)
                factor = cleanData.adjustFactorDate(factorRaw, self.__startDate, self.__endDate)
            else:
                factorRaw = cleanData.getUniverseSingleFactor(pathToUse, IndexName=['tiaoCangDate','secID'])
                factorRaw = factorRaw.loc[factorRaw.index.get_level_values('tiaoCangDate') >= self.__startDate]
                factor = factorRaw.loc[factorRaw.index.get_level_values('tiaoCangDate') <= self.__endDate]
            factor.name = name
            ret[name] = factor
        return ret

if __name__ == "__main__":
    factor = FactorLoader('2015-01-05', '2015-12-30', ['NAV', 'ROE','RETURN'])
    ret = factor.getFactorData()
    print ret['RETURN']