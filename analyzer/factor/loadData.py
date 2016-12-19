# -*- coding: utf-8 -*-
from PyFin.Enums import TimeUnits
from utils import dateutils
import cleanData
import pandas as pd

_factorPathDict ={
    'NAV': 'net_asset.csv',
    'ROE': 'ROE.csv'
}

class FactorLoader(object):
    def __init__(self, startDate, endDate, factorNames, freq=TimeUnits.Months):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__factorNames = factorNames
        self.__freq = freq
        self.__tiaocangDate = []

    def getTiaoCangDate(self):
        return dateutils.getPosAdjDate(self.__startDate, self.__endDate, freq=self.__freq)

    def getFactorData(self):
        path = '..//..//data//factor//'
        ret = pd.Series()
        for name in self.__factorNames:
            path +=  _factorPathDict[name]
            factorRaw = cleanData.getUniverseSingleFactor(path)
            ret = pd.concat([ret, cleanData.adjustFactorDate(factorRaw)], axis=1)
        return ret