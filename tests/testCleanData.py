# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from analyzer.factor.cleanData import getMultiIndexData


class TestCleanData(unittest.TestCase):
    def testGetMultiIndexData(self):
        index = pd.MultiIndex.from_arrays(
            [['2015-01-01', '2015-01-02', '2015-01-02', '2015-02-04', '2015-02-04'], ['A', 'B', 'C', 'A', 'C']],
            names=['date', 'category'])
        multi = pd.Series([1.0, 2.0, 3.0, 4.0, 3.0], index=index)

        calculated = getMultiIndexData(multi, 'date', '2015-01-02')
        expected = pd.Series([2.0, 3.0], index=pd.MultiIndex(
            levels=[[u'2015-01-01', u'2015-01-02', u'2015-02-04'], [u'A', u'B', u'C']],
            labels=[[1, 1], [1, 2]],
            names=[u'date', u'category']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = getMultiIndexData(multi, 'date', '2015-01-02')
        expected = pd.Series([2.0, 3.0], index=pd.MultiIndex(
            levels=[[u'2015-01-01', u'2015-01-02', u'2015-02-04'], [u'A', u'B', u'C']],
            labels=[[1, 1], [1, 2]],
            names=[u'date', u'category']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = getMultiIndexData(multi, 'date', '2015-01-02', 'category', 'B')
        expected = pd.Series([2.0], index=pd.MultiIndex(
            levels=[[u'2015-01-01', u'2015-01-02', u'2015-02-04'], [u'A', u'B', u'C']],
            labels=[[1], [1]],
            names=[u'date', u'category']))
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = getMultiIndexData(multi, 'date', ['2015-01-02', '2015-02-04'], 'category', 'C')
        expected = pd.Series([3.0, 3.0], index=pd.MultiIndex(
            levels=[[u'2015-01-01', u'2015-01-02', u'2015-02-04'], [u'A', u'B', u'C']],
            labels=[[1, 2], [2, 2]],
            names=[u'date', u'category']))
        pd.util.testing.assert_series_equal(calculated, expected)
