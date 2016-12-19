# -*- coding: utf-8 -*-
from PyFin.DateUtilities import Date
from utils import date

def get_report_date(actDate):
    """
    Args:
        act_date: str/datetime, 任意日期

    Returns: str, 对应应使用的报告日期， 从wind数据库中爬取
    此函数的目的是要找到，任意时刻可使用最新的季报数据的日期，比如2-20日可使用的最新季报是去年的三季报（对应日期为9-30），

    """

    if isinstance(actDate, str):
        actDate = date.stringToDatetime(actDate)
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