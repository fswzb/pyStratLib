#coding=utf-8


from numpy import mean
from numpy import cov
from numpy.linalg import eig
from numpy import mat


def eigValPct(eigVals, pct):
    """
    :param eigVals: list, 所有特征值组成的向量
    :param pct: 阈值
    :return: 给定百分比阈值,返回需要降低到多少维度
    """

    sortEigVals = sorted(eigVals)
    sortEigVals = sortEigVals[-1:1] # 特征值从大到小排列
    eigValsSum = sum(sortEigVals)
    acumEigVals = reduce(lambda x,y: x + y, sortEigVals)
    print acumEigVals
    return


def pcaDecomp(dataMat, pct=0.9):
    """
    :param dataMat:
    :param pct:
    :return:
    """

    meanVals = mean(dataMat, axis=0) # 对每一列求均值
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved, rowvar=0)
    eigVals, eigVects = eig(mat(covMat))



if __name__ == "__main__":
    eigValPct([1,2,3])




