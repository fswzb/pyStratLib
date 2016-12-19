# coding=utf-8
from PyFin.DateUtilities import Date
from PyFin.DateUtilities import Calendar
from PyFin.DateUtilities import Schedule
from PyFin.DateUtilities import Period
from PyFin.Enums import TimeUnits
from PyFin.Enums import BizDayConventions
import datetime as dt


def stringToDatetime(strDate, format="%Y-%m-%d"):
    """
    Args:
        strDate: str, some date,
        format: str, optional, format of the string date

    Returns: datetime type of the date

    """
    return dt.datetime.strptime(strDate, format)

def getPosAdjDate(startDate, endDate, format="%Y-%m-%d", calendar='China.SSE'):
    """
    Args:
        startDate: str, start date of strategy
        endDate: str, end date of strategy
        format: str, optional, time format of the date
        calendar: str, optional, name of the calendar to use in dates math


    Returns: list of str, pos adjust dates

    """
    dtStartDate = stringToDatetime(startDate, format)
    dtEndDate = stringToDatetime(endDate, format)

    dStartDate = Date(dtStartDate.year, dtStartDate.month, dtStartDate.day)
    dEndDate = Date(dtEndDate.year, dtEndDate.month, dtEndDate.day)

    cal = Calendar(calendar)
    posAdjustDate = Schedule(dStartDate,
                     dEndDate,
                     Period(1, TimeUnits.Months),
                     cal,
                     BizDayConventions.Preceding)
    # it fails if setting dStartDate to be first adjustment date, then use Schedule to compute the others
    # so i first compute dates list in each period, then compute the last date of each period
    # last day of that period(month) is the pos adjustment date
    strPosAdjustDate = [str(cal.endOfMonth(date)) for date in posAdjustDate]

    return strPosAdjustDate



if __name__ == "__main__":
    print getPosAdjDate('2016-5-20','2016-12-20')