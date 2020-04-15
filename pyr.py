import pandas as pd

import rpy2.robjects as ro
R=ro.r

from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

# survey = importr("survey")
descr = importr("descr")

def pyr(object):
    with localconverter(ro.default_converter + pandas2ri.converter):
      return ro.conversion.py2rpy(object)

def rpy(object):
    with localconverter(ro.default_converter + pandas2ri.converter):
      return ro.conversion.rpy2py(object)

def pyr_tab(object, interpret=False):
    cols = rpy(object.names[1])
    index = rpy(object.names[0])
    if interpret:
        df = pd.DataFrame(rpy(object), index=index, columns=cols)
        return interpret(df)
    else:
        return pd.DataFrame(rpy(object), index=index, columns=cols)

def freq(vec, weights):
    f = descr.freq(pyr(vec), pyr(weights))
    return pyr_tab(f)

def crosstab(x, y, **kwargs):
    if kwargs.get('weights'):
        weights = pyr(kwargs['weights'])
    else:
        weights = pd.Series([1 for i in range(len(x))])
        weights = pyr(weights)
    f = descr.crosstab(pyr(x), pyr(y), **kwargs)
    return pyr_tab(f)

def interpret(df):
    df['stars'] = pd.cut(df['Pr(>|t|)'], [0,0.001, 0.01, 0.05, 1], labels=['***', '**', '*', 'NS'])
    return df
