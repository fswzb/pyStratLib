# -*- coding: utf-8 -*-
from PyFin.DateUtilities import Date
from PyFin.Enums import TimeUnits
import pandas as pd
from utils import dateutils


def getReportDate(actDate):
    """
    Args:
        act_date: str/datetime, 任意日期

    Returns: str, 对应应使用的报告日期， 从wind数据库中爬取
    此函数的目的是要找到，任意时刻可使用最新的季报数据的日期，比如2-20日可使用的最新季报是去年的三季报（对应日期为9-30），

    """

    if isinstance(actDate, str):
        actDate = dateutils.stringToDatetime(actDate)
    actMonth = actDate.month
    actYear = actDate.year
    if 1 <= actMonth <= 3:# 第一季度使用去年三季报的数据
        year = actYear - 1
        month = 9
        day = 30
    elif 4 <= actMonth <= 7: #第二季度使用当年一季报
        year = actYear
        month = 3
        day = 31
    elif 8<= actMonth <=9: # 第三季度使用当年中报
        year = actYear
        month = 6
        day = 30
    else:
        year = actYear # 第四季度使用当年三季报
        month = 9
        day = 30
    ret = Date(year, month, day)
    return str(ret)


def getUniverseSingleFactor(path):
    """
    Args:
        path:  str, path of csv file, col =[datetime, secid, factor]

    Returns: pd.Series, multiindex =[datetime, secid] value = factor

    """
    factor = pd.read_csv(path)
    factor.columns = ['tradeDate', 'secID','factor']
    factor['tradeDate'] = pd.to_datetime(factor['tradeDate'], format='%Y%m%d')
    factor = factor.dropna()
    factor = factor[factor['secID'].str.contains(r'^[^<A>]+$$')] #去除类似AXXXX的代码(IPO终止)
    index = pd.MultiIndex.from_arrays([factor['tradeDate'].values, factor['secID'].values], names=['tradeDate','secID'])
    ret = pd.Series(factor['factor'].values, index=index, name='factor')
    return ret

def adjustFactorDate(factorRaw, startDate, endDate, freq=TimeUnits.Months):
    """
    Args:
        factorRaw: pd.DataFrame, multiindex =['tradeDate','secID']
        startDate: str, start date of factor data
        endDate:  str, end date of factor data
        freq: str, optional

    Returns: pd.Series, multiindex =[datetime, secid]
    此函数的主要目的是 把原始以报告日为对应日期的因子数据 改成 调仓日为日期（读取对应报告日数据）
    """

    # 获取调仓日日期
    tiaocangDate = dateutils.getPosAdjDate(startDate, endDate, freq=freq)
    reportDate = [getReportDate(date) for date in tiaocangDate]
    ret = pd.Series()
    for i in range(len(tiaocangDate)):
        query = factorRaw.loc[factorRaw.index.get_level_values('tradeDate') == reportDate[i]]
        query = query.reset_index().drop('tradeDate',axis=1)
        query['tiaoCangDate'] = [tiaocangDate[i]] * query['secID'].count()
        ret = pd.concat([ret, query], axis=0)

    # 清理列
    ret = ret[['tiaoCangDate', 'secID','factor']]
    index = pd.MultiIndex.from_arrays([ret['tiaoCangDate'].values, ret['secID'].values], names=['tiaoCangDate','secID'])
    ret = pd.Series(ret['factor'].values, index=index, name='factor')
    return ret

if __name__ == "__main__":
    path = '..//..//data//net_asset.csv'
    factorRaw = getUniverseSingleFactor(path)
    print adjustFactorDate(factorRaw, '2015-01-05','2015-12-01')