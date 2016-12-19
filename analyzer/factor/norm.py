# -*- coding: utf-8 -*-
# ref: https://uqer.io/community/share/55ff6ce9f9f06c597265ef04


def winsorize(factors, nb_std_or_quantile = 3):
    """
    Args:
        factors: pd.Series, 原始因子
        nb_std_or_quantile: int or list, optional, 如果是int, 则代表number of std, 如果是list[0.025,0.975] 则使用quantile作为极值判断的标准

    Returns: pd.Series, 去极值化后的因子

    """
    factors = factors.copy()
    if isinstance(nb_std_or_quantile,int):
        mean = factors.mean()
        std = factors.std()
        factors[factors<mean - nb_std_or_quantile*std] = mean - nb_std_or_quantile*std
        factors[factors>mean + nb_std_or_quantile*std] = mean + nb_std_or_quantile*std
    elif isinstance(nb_std_or_quantile,list) and len(nb_std_or_quantile)==2:
        q = factors.quantile(nb_std_or_quantile)
        factors[factors<q.iloc[0]] = q.iloc[0]
        factors[factors>q.iloc[1]] = q.iloc[1]
    else:
        raise ValueError('nb_std_or_quantile should be list or int type')
    return factors

def standardize(factors):
    """
    Args:
        factors: pd.Series, 原始因子

    Returns: pd.Series, 标准化后的因子  (x - mean)/std

    """
    factors = factors.copy()
    mean = factors.mean()
    std = factors.std()
    ret = factors.apply(lambda x: (x - mean)/std)
    return ret

