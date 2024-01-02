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

- simreader:class
- 

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
import numpy as np
import zipfile as zf
import simdate as sdt
import os
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
            self.__type = "Ori"
        elif "pandas" in x :
            oData = pl.from_pandas(data)
            self.__type = "Ori"
        elif "dask" in x :
            oData = data
            self.__type = "dask"
            self.__lazy = True
        elif "veax" in x :
            oData = data
            self.__type = "veax"
            self.__lazy = True
        elif "ndarray" in x :
            oData = pl.from_numpy(data)
            self.__type = "Ori"
        elif "<class 'dict'>" == x:
            oData = pl.from_dict(data)
            self.__type = "Ori"
        else:
            raise ValueError("使用了不支持的数据!")
        self.__data = oData
    def __len__(self) -> int|None:
        if self.__lazy :
            print("Currently in Lazy mode, so the data length cannot be provided!")
            return None
        else:
            return len(self.__data)
    def __getitem__(self, key):
        pass
    def __setitem__(self,key,value) -> None:
        pass
    def __str__(self) -> str:
        pass
    def __repr__(self) -> str:
        pass
    def to_pandas(self) -> pd.DataFrame :
        pass
    def to_polars(self) -> pl.dataframe.frame.DataFrame :
        pass
    def transtype(self) -> None :
        pass
    def select(self, questing):
        pass
    @property
    def shape(self):
        pass
    @property
    def type(self):
        pass
    @property
    def columns(self):
        pass
    def append(self):
        pass
    def join(self):
        pass
    def groupby(self):
        pass
    def head(self):
        pass
    def tail(self):
        pass
    def sort(self):
        pass


###################
# Static Data
###################

_MAXPDDATASIZE = 1024 * 1024 * 1024 * 0.5

###################
# Functions
###################

def getreader(dirfile):
    '''
    快速反馈一个读取函数。
    '''
    is_simple = "PL" if os.path.getsize(dirfile) > _MAXPDDATASIZE else "PD"
    LFUN = {
        "PD" : {
            "csv":pd.read_csv,
            "xlsx":pd.read_excel,
            "xls":pd.read_excel,
            "txt":pd.read_csv,
            "data":pd.read_csv,
            "json":pd.read_json
        },
        "PL" : {
            "csv":pl.scan_csv,
            "data":pl.scan_csv,
            "xlsx":pl.read_excel,
            "xls":pl.read_excel,
            "json":pl.read_json,
            "txt":pl.scan_csv
        }
    }
    fna = dirfile.split(".")[-1]
    return (LFUN[is_simple][fna], is_simple)

def simreader(files, **args) -> simDataFrame :
    pass

def readZipData(dirfile, dname, tmpRoot = None, **args) -> simreader:
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