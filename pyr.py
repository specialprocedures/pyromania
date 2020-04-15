import pandas as pd

import rpy2.robjects as ro
R = ro.r

from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

from rpy2.robjects.conversion import localconverter

def pyr(object):
    with localconverter(ro.default_converter + pandas2ri.converter):
        return ro.conversion.py2rpy(object)

def rpy(object):
    with localconverter(ro.default_converter + pandas2ri.converter):
        return ro.conversion.rpy2py(object)

def py_tab(object):
    cols = rpy(object.names[1])
    index = rpy(object.names[0])
    return pd.DataFrame(rpy(object), index=index, colums=cols)
