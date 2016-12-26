# -*- coding: utf-8 -*-
import unittest
import pandas as pd
from analyzer.factor.cleanData import adjustFactorDate
from analyzer.factor.cleanData import getMultiIndexData
from analyzer.factor.cleanData import getReportDate


class TestCleanData(unittest.TestCase):
    def testGetReportDate(self):
        actDate = ['2015-01-01', '2015-03-30', '2015-06-20', '2016-09-01', '2016-12-05']
        calculated = [getReportDate(date) for date in actDate]
        expected = ['2014-09-30', '2014-09-30', '2015-03-31', '2016-06-30', '2016-09-30']
        for i in range(len(expected)):
            self.assertEqual(calculated[i], expected[i], "Expected report date of {0} is not equal to expected {1}"
                             .format(actDate[i], expected[i]))

    def testAdjustFactorDate(self):
        factorRaw = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], name='factor', index=pd.MultiIndex.from_arrays(
            [['2015-03-31', '2015-03-31', '2015-12-31', '2016-06-30', '2016-09-30'],
             ['000691.SZ', '002118.SZ', '000691.SZ', '600312.SH', '300518.SZ']], names=['tradeDate', 'secID']))

        calculated = adjustFactorDate(factorRaw, '2015-01-01', '2016-09-30', freq='m')
        expected = pd.Series([1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 4.0, 4.0], name='factor',
                             index=pd.MultiIndex.from_arrays(
                                 [['2015-04-30', '2015-04-30', '2015-05-29', '2015-05-29', '2015-06-30',
                                   '2015-06-30', '2015-07-31', '2015-07-31', '2016-08-31', '2016-09-30'],
                                  ['000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ', '000691.SZ',
                                   '002118.SZ', '000691.SZ', '002118.SZ', '600312.SH', '600312.SH']],
                                 names=['tiaoCangDate', 'secID']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = adjustFactorDate(factorRaw, '2015-01-01', '2016-01-30', freq='m')
        expected = pd.Series([1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0], name='factor',
                             index=pd.MultiIndex.from_arrays(
                                 [['2015-04-30', '2015-04-30', '2015-05-29', '2015-05-29', '2015-06-30',
                                   '2015-06-30', '2015-07-31', '2015-07-31'],
                                  ['000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ', '000691.SZ',
                                   '002118.SZ', '000691.SZ', '002118.SZ']],
                                 names=['tiaoCangDate', 'secID']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = adjustFactorDate(factorRaw, '2015-05-01', '2015-06-30', freq='w')
        expected = pd.Series([1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0],
                             name='factor',
                             index=pd.MultiIndex.from_arrays(
                                 [['2015-05-01', '2015-05-01', '2015-05-08', '2015-05-08', '2015-05-15', '2015-05-15',
                                   '2015-05-22', '2015-05-22', '2015-05-29', '2015-05-29', '2015-06-05', '2015-06-05',
                                   '2015-06-12', '2015-06-12', '2015-06-19', '2015-06-19', '2015-06-26', '2015-06-26'],
                                  ['000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ',
                                   '000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ',
                                   '000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ', '000691.SZ', '002118.SZ']],
                                 names=['tiaoCangDate', 'secID']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = adjustFactorDate(factorRaw, '2015-05-01', '2016-06-30', freq='y')
        expected = pd.Series([5.0], name='factor', index=pd.MultiIndex.from_arrays([['2016-12-31'], ['300518.SZ']],
                                                                                   names=['tiaoCangDate', 'secID']))
        pd.util.testing.assert_series_equal(calculated, expected)

    def testGetMultiIndexData(self):
        index = pd.MultiIndex.from_arrays(
            [['2015-01-01', '2015-01-02', '2015-01-02', '2015-02-04', '2015-02-04'], ['A', 'B', 'C', 'A', 'C']],
            names=['date', 'category'])
        multi = pd.Series([1.0, 2.0, 3.0, 4.0, 3.0], index=index)

        calculated = getMultiIndexData(multi, 'date', '2015-01-02')
        expected = pd.Series([2.0, 3.0], index=pd.MultiIndex.from_arrays(
            [['2015-01-02', '2015-01-02'], ['B', 'C']],
            names=['date', 'category']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = getMultiIndexData(multi, 'date', ['2015-01-02'])
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = getMultiIndexData(multi, 'date', '2015-01-02', 'category', 'B')
        expected = pd.Series([2.0], index=pd.MultiIndex.from_tuples([('2015-01-02', 'B')],
                                                                    names=['date', 'category']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = getMultiIndexData(multi, 'date', ['2015-01-02', '2015-02-04'], 'category', 'C')
        expected = pd.Series([3.0, 3.0], index=pd.MultiIndex.from_product(
            [['2015-01-02', '2015-02-04'], ['C']],
            names=['date', 'category']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = getMultiIndexData(multi, 'date', ['2015-01-02', '2015-02-04'], 'category', ['B', 'C'])
        expected = pd.Series([2.0, 3.0, 3.0], index=pd.MultiIndex.from_arrays(
            [['2015-01-02', '2015-01-02', '2015-02-04'], ['B', 'C', 'C']],
            names=['date', 'category']))
        pd.util.testing.assert_series_equal(calculated, expected)
