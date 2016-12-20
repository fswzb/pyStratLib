# -*- coding: utf-8 -*-
from utils import dateutils
import cleanData
import pandas as pd

_factorPathDict ={
    'NAV': 'net_asset.csv', # 净资产
    'ROE': 'ROE.csv', # 净资产收益率
    'PE': 'PE_TTM.csv', # 市盈率
    'TTM': 'TTM.csv', # 销售毛利率
    'CAP': 'cap.csv' # 总市值
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
        path = '..//..//data//factor//'
        ret = pd.Series()
        for name in self.__factorNames:
            pathToUse = path +  _factorPathDict[name]
            factorRaw = cleanData.getUniverseSingleFactor(pathToUse)
            factor = cleanData.adjustFactorDate(factorRaw,self.__startDate, self.__endDate)
            ret[name] = factor
        return ret

if __name__ == "__main__":
    factor = FactorLoader('2015-01-05', '2015-12-30', ['NAV', 'ROE'])
    ret = factor.getFactorData()
    print ret['NAV']