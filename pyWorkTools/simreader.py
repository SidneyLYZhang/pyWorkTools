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
    def __init__(self, data) -> None:
        pass
    def __len__(self) -> int :
        pass
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
    def groupby(self):
        pass
    def head(self):
        pass
    def tail(self):
        pass
    def sort(self):
        pass



class simreader(object):
    """
    快捷读取数据，并根据数据量选择polars或者pandas，
    并提供统一的简介外部接口，方便引用使用。
    """
    def __init__(self, file, **args) -> None:
        if isinstance(file, pd.DataFrame) or isinstance(file, pd.Series):
            self.__data = file if isinstance(file, pd.DataFrame) else pd.DataFrame({file.name:file})
            self.columns = file.columns
        elif os.path.isdir(file):
            files = os.listdir(file)
            tfun, self.__server = getreader(os.path.join(file,x))
            rfun = lambda x: (os.path.join(file,x),**args)
            tmp = list(map(rfun, files))
            self.__data = dict(zip(files,tmp))
            self.columns = files
        else:
            self.__data = getreader(file)(file, **args)
            self.columns = self.__data.columns
        self.shape = self.__data.shape if isinstance(self.__data, pd.DataFrame) else (len(self.__data), list(map(lambda x: x.shape,list(self.__data.values()))))
    def to_dataframe(self):
        return self.__data.values() if isinstance(self.__data, dict) else self.__data
    def __len__(self):
        return self.__data.shape[0]
    def __getitem__(self,key):
        return simreader(self.__data[key])
    def __setitem__(self,key,value):
        self.__data[key] = value
    def __str__(self) -> str:
        return str(self.__data)
    def __repr__(self) -> str:
        return self.__str__()

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