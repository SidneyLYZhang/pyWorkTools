"""
     _                              _
 ___(_)_ __ ___  _ __ ___  __ _  __| | ___ _ __
/ __| | '_ ` _ \| '__/ _ \/ _` |/ _` |/ _ \ '__|
\__ \ | | | | | | | |  __/ (_| | (_| |  __/ |
|___/_|_| |_| |_|_|  \___|\__,_|\__,_|\___|_|

================================================================================

Version: 2.0.0
Update: 2023-12-26
Author: Sidney Zhang<zly@lyzhang.me>

================================================================================

Requirement:

- pandas
- polars
- dask
- veax
- numpy

Instruction:

This package is used for quickly generating commonly used time series data.
快速处理常用时间序列数据。

================================================================================

Usage:

- simDataFrame:class
- function: getreader, simreader, readZipData

================================================================================

# LICENSE

License-[GPL3](https://www.gnu.org/licenses/gpl-3.0.html)

simreader.py
Copyright (C) 2023 SidneyZhang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

###################
# Packages
###################

import polars as pl
import pandas as pd
import dask.dataframe as dd
import numpy as np
import zipfile as zf
import simdate as sdt
import simdata as sdd
import vaex
import os
import re
import shutil

###################
# Classes
###################

class simDataFrame(object):
    '''
    尽量转换为polars进行处理；
    对于dask、veax不进行转换，使用原始类型处理；
    统一提供以下运算：
    - 指定列数据
    - 按规则选择
    - 聚集计算或透视表计算
    - 取数据的头尾数据
    - 添加/合并数据
    - 排序
    '''
    def __init__(self, data) -> None:
        x = str(type(oData))
        self.__lazy = True if "LazyFrame" in x else False
        if "polars" in x :
            oData = data
            self.__type = "polars.DataFrame"
        elif "pandas" in x :
            oData = pl.from_pandas(data)
            self.__type = "polars.DataFrame"
        elif "dask" in x :
            oData = data
            self.__type = "dask.DataFrame"
            self.__lazy = True
        elif "vaex" in x :
            oData = data
            self.__type = "vaex.DataFrame"
            self.__lazy = True
        elif "ndarray" in x :
            oData = pl.from_numpy(data)
            self.__type = "polars.DataFrame"
        elif "<class 'dict'>" == x:
            oData = pl.from_dict(data)
            self.__type = "polars.DataFrame"
        else:
            raise ValueError("使用了不支持的数据!")
        self.__data = oData
    def __len__(self) -> int|None:
        if self.__lazy :
            print("Currently in Lazy-Mode, so the data length cannot be provided!")
            return None
        else:
            return len(self.__data)
    def __getitem__(self, key):
        if "polars" in self.__type :
            res = self.__data.select(pl.col(*key if isinstance(key,list) else key))
        else:
            res = self.__data[key]
        return res
    def col(self, key) :
        if "polars" in self.__type :
            return pl.col(key)
        else : # for veax or dask
            return self.__data[key]
    def __setitem__(self,key,value) -> None:
        pass
    def __str__(self) -> str:
        rstr = str(self.__data)
        print(rstr)
    def __repr__(self) -> str:
        txt = "{}\ndata sample view:\n{}".format(self.type, self.__str__())
        return txt
    def to_type(self, atype = "pandas") :
        flist = dir(self.__data)
        tfun = sdd.exclude_x("^_.*",sdd.x_in_self(atype,flist))
        if tfun :
            return getattr(self.__data, tfun[0], None)
        else:
            return None
    def select(self, questing):
        if "polars" in self.__type :
            return simDataFrame(self.__data.select(questing))
        else :
            return simDataFrame(self.__data[questing])
    @property
    def shape(self):
        return self.__data.shape
    @property
    def type(self) -> str:
        lzsrt = "Lazy Mode" if self.__lazy else "Normal Mode"
        tysrt = "<type {} in {}>".format(self.__type,lzsrt)
        return tysrt
    @property
    def columns(self):
        if "vaex" in self.__type :
            return self.__data.column_names
        elif "dask" in self.__type :
            return self.__data.columns.tolist()
        else:
            return self.__data.columns
    def append(self):
        pass
    def join(self):
        pass
    def groupby(self):
        pass
    def pivot(self):
        pass
    def head(self, key = 5):
        return simDataFrame(self.__data.head(key))
    def tail(self, key = 5):
        return simDataFrame(self.__data.tail(key))
    def sort(self, by, replace = False):
        if replace :
            self.__data.sort()
        pass


###################
# Static Data
###################

_MAXPDDATASIZE = 1024 * 1024 * 1024 * 0.5

_DATPDLIST = ['clipboard', 'csv', 'excel', 'feather',
               'fwf', 'gbq', 'hdf', 'html', 'json', 
               'orc', 'parquet', 'pickle', 'sas', 'spss', 
               'sql', 'sql', 'sql', 'stata', 'table', 'xml']

###################
# Functions
###################

def getreader(dirfile, just_use = None):
    '''
    快速反馈一个读取函数。
    20240103:   大幅优化了代码结构
                just_use是指定pandas处理读取，推荐数据量较小时使用
    '''
    if just_use is None :
        fna = re.sub(r'[0-9]+', '', dirfile.split(".")[-1])
        if fna == "orc":
            return dd.read_orc
        elif fna in ["xls","xlsx"]:
            return pl.read_excel
        elif fna == "hdf":
            return vaex.open
        elif os.path.getsize(dirfile) > (_MAXPDDATASIZE * 2):
            return vaex.open
        elif os.path.getsize(dirfile) > _MAXPDDATASIZE:
            return getattr(pl, "scan_{}".format(fna), vaex.open)
        else:
            return getattr(pl, "read_{}".format(fna), pl.read_csv)
    else:
        if just_use in _DATPDLIST:
            return getattr(pd, "read_{}".format(just_use))
        else :
            raise ValueError("You are referencing unsupported data types.")


def simreader(files, justuse = None, **args) -> simDataFrame|dict|None :
    if os.path.isfile(files) :
        temdata = getreader(files,just_use=justuse)(files, **args)
        return simDataFrame(temdata)
    elif os.path.isdir(files) :
        res = {}
        for item in os.scandir(files):
            if item.is_file() :
                tFun = getreader(item.path, just_use=justuse)
                res[item.name.split('.')[0]] = simDataFrame(tFun(item.path, **args))
        if len(res) > 0 :
            return res
        else:
            print("There is NO loadable data !!")
            return None
    else:
        raise ValueError("Data does NOT exist !!")

def readZipData(dirfile, dname, tmpRoot = None, **args):
    '''
    读取zip中的数据，返回simreader类型。
    '''
    dataPath = "{}/TMP{}/".format(tmpRoot if tmpRoot else "D:",
                                  sdt.now(sformat = "YYYYMMDDHHmmss"))
    with zf.ZipFile(dirfile) as f:
        f.extractall(path = dataPath)
    result = simreader(dataPath+dname,**args)
    shutil.rmtree(dataPath)
    return result

############
# MAINS
############

if __name__ == '__main__':
    from simdata import iris_zip
    data = readZipData(iris_zip[0],iris_zip[1],
                       header = None, names = iris_zip[2])
    print(iris_zip[3])
    print(data)