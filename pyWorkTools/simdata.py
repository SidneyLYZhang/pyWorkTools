"""
     _           ____        _
 ___(_)_ __ ___ |  _ \  __ _| |_ __ _
/ __| | '_ ` _ \| | | |/ _` | __/ _` |
\__ \ | | | | | | |_| | (_| | || (_| |
|___/_|_| |_| |_|____/ \__,_|\__\__,_|

================================================================================

Version: 1.0.0
Update: 2023-12-26
Author: Sidney Zhang<zly@lyzhang.me>

================================================================================

Requirement:

- 
- 

Instruction:


================================================================================

Usage:

- 

================================================================================

# LICENSE

License-[GPL3](https://www.gnu.org/licenses/gpl-3.0.html)

simdata.py
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

from collections.abc import Iterable
from functools import reduce
import os

###################
# Classes
###################

class vecspace(object):
    """
    解决python list的一些计算问题
    """
    def __init__(self, data = None) -> None:
        if data is None :
            self.__data = []
        elif isinstance(data, Iterable):
            self.__data = data
        else:
            self.__data = [data]
        if isinstance(data, str):
            self.__str = True
        else:
            self.__str = False
    def __str__(self) -> str:
        tdt = str(self.__data)
        pstr = "vecSpace!{}" if "[" in tdt else "vecSpace!\n{}"
        return pstr.format(tdt)
    def __repr__(self) -> str:
        return self.__str__()
    def __len__(self) -> int :
        return len(self.__data)
    def __add__(self, y):
        if self.__str :
            tmp = [chr(ord(x)+y) for x in self.__data]
            return vecspace(reduce(lambda x,y: x+y, tmp))
        else:
            if isinstance(self.__data, list):
                tmp = 
                return vecspace()
            else:
                tmp = vecspace(self.__data + y) if len(self) else vecspace(y)
                return tmp
    def __radd__(self, y):
        pass
    def __mul__(self, y):
        pass
    def __rmul__(self, x):
        pass

###################
# Static Data
###################

_curDir = os.path.dirname(__file__)
iris_info = """
测试数据为鸢尾花数据：
1. sepal length in cm 花萼长
2. sepal width in cm 花萼宽
3. petal length in cm 花瓣长
4. petal width in cm 花瓣宽
5. class: 分类
    -- Iris Setosa
    -- Iris Versicolour
    -- Iris Virginica
数据来源： http://archive.ics.uci.edu/ml/datasets/Iris
"""
iris_zip = (
    os.path.join(_curDir, "Data/iris.zip"),
    "iris.data",
    ['sepal_length','sepal_width','petal_length','petal_width','class'],
    iris_info
)

###################
# Functions
###################

'''
定义向量空间的运算:

1. 加法 add
2. 乘法 mul
'''

def sum(x: Iterable) -> Iterable :
    res = reduce(lambda x,y: x+y, x)
    return res

def add(x: Iterable, y: Iterable) -> Iterable :
    try:
        tmp = list(zip(x,y))
        return [sum(i) for i in tmp]
    except:  # noqa: E722
        raise ValueError

###################
# Test - Main
###################

if __name__ == '__main__':
    print(iris_zip)