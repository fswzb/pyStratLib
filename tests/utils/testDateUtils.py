# -*- coding: utf-8 -*-
import unittest

from utils.dateutils import getPosAdjDate


class TestDateUtils(unittest.TestCase):
    def testGetPosAdjDate(self):
        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.SSE', freq='m')
        expected = ['2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-30', '2015-11-30', '2015-12-31',
                    '2016-01-29', '2016-02-29', '2016-03-31', '2016-04-29', '2016-05-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015/06/01', '2016/06/01', format="%Y/%m/%d", calendar='China.SSE', freq='m')
        expected = ['2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-30', '2015-11-30', '2015-12-31',
                    '2016-01-29', '2016-02-29', '2016-03-31', '2016-04-29', '2016-05-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01')
        expected = ['2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-30', '2015-11-30', '2015-12-31',
                    '2016-01-29', '2016-02-29', '2016-03-31', '2016-04-29', '2016-05-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.SSE', freq='w')
        expected = ['2015-06-05', '2015-06-12', '2015-06-19', '2015-06-26', '2015-07-03', '2015-07-10', '2015-07-17',
                    '2015-07-24', '2015-07-31', '2015-08-07', '2015-08-14', '2015-08-21', '2015-08-28', '2015-09-04',
                    '2015-09-11', '2015-09-18', '2015-09-25', '2015-10-02', '2015-10-09', '2015-10-16', '2015-10-23',
                    '2015-10-30', '2015-11-06', '2015-11-13', '2015-11-20', '2015-11-27', '2015-12-04', '2015-12-11',
                    '2015-12-18', '2015-12-25', '2016-01-01', '2016-01-08', '2016-01-15', '2016-01-22', '2016-01-29',
                    '2016-02-05', '2016-02-12', '2016-02-19', '2016-02-26', '2016-03-04', '2016-03-11', '2016-03-18',
                    '2016-03-25', '2016-04-01', '2016-04-08', '2016-04-15', '2016-04-22', '2016-04-29', '2016-05-06',
                    '2016-05-13', '2016-05-20', '2016-05-27', '2016-06-03']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015/06/01', '2016/06/01', format="%Y/%m/%d", calendar='China.SSE', freq='y')
        expected = ['2015-12-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.IB', freq='m')
        expected = ['2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-30', '2015-11-30', '2015-12-31',
                    '2016-01-29', '2016-02-29', '2016-03-31', '2016-04-29', '2016-05-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='Target', freq='m')
        expected = ['2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-30', '2015-11-30', '2015-12-31',
                    '2016-01-29', '2016-02-29', '2016-03-31', '2016-04-29', '2016-05-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='Null', freq='m')
        expected = ['2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-31', '2015-11-30', '2015-12-31',
                    '2016-01-31', '2016-02-29', '2016-03-31', '2016-04-30', '2016-05-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='NullCalendar', freq='m')
        expected = ['2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-31', '2015-11-30', '2015-12-31',
                    '2016-01-31', '2016-02-29', '2016-03-31', '2016-04-30', '2016-05-31']
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")
