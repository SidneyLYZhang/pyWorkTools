"""
     _               _       _
 ___(_)_ __ ___   __| | __ _| |_ ___
/ __| | '_ ` _ \ / _` |/ _` | __/ _ \
\__ \ | | | | | | (_| | (_| | ||  __/
|___/_|_| |_| |_|\__,_|\__,_|\__\___|

================================================================================

Version : 2.0.1
Update : 2023-12-26
Author: Sidney Zhang<zly@lyzhang.me>

================================================================================

Requirement:

- pendulum
- numpy

Instruction:

The Python script, simdate, leverages the pendulum library for simplified date 
and time zone handling. It provides convenient classes like tzones for predefined
time zones and simdate for easy date manipulations. The script also offers 
functions to parse dates, retrieve current or previous dates, and calculate date 
ranges for specific intervals.

simdate 提供了一套方便的工具，用于处理日期和时区，使得在不同时区和日期操作中更加方便。
这包括了对时区的枚举定义、日期的快速处理和一些相关的辅助函数。

================================================================================

Usage:

- yesterday | lastmonth | parser : function
- simdate:class

================================================================================

# LICENSE

License-[GPL3](https://www.gnu.org/licenses/gpl-3.0.html)

simdate.py
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

import pendulum as pdm
import numpy as np
import datetime as dt
from enum import Enum

###################
# Classes
###################

class tzones(Enum):
    '''
    时区枚举数据：
    1. 北京时间         Beijing
    2. 美国东部时间     USAE
    3. 美国太平洋时间   USAP
    4. 伦敦时间         London
    5. 日本时间         Japan
    6. 印度时间         Indian
    7. 德国时间         Germany
    8. UTC标准时间      UTC

    Data Definition: 
    https://github.com/sdispater/pendulum/blob/master/pendulum/tz/data/windows.py
    '''

    Beijing = "Asia/Shanghai"
    USAE = "America/New_York"
    USAP = "America/Los_Angeles"
    London = "Europe/London"
    Japan = "Asia/Tokyo"
    Germany = "Europe/Berlin"
    India = "Asia/Calcutta"
    UTC = "Etc/GMT"
    __data__ = {
        "Asia/Shanghai": "China Standard Time 中国标准时间",
        "America/New_York": "US Eastern Standard Time 美国东部标准时间",
        "America/Los_Angeles": "US Pacific Standard Time 美国太平洋标准时间",
        "Europe/London": "GMT Standard Time 英联邦标准时间",
        "Asia/Tokyo": "Tokyo Standard Time 东京标准时间|日本时间",
        "Europe/Berlin": "W. Europe Standard Time 西欧标准时间|德国时间",
        "Asia/Calcutta": "India Standard Time 印度标准时间",
        "Etc/GMT": "UTC 协调世界时"
    }
    def describe(self):
        return self.name, self.value, tzones.__data__[self.value]
    def __str__(self):
        return "{}({}): {}".format(*self.describe())
    def __call__(self):
        return self.value

class simdate(object):
    '''
    快速时间类
    '''
    def __init__(self, datestr = None, tz = tzones.Beijing()) -> None:
        if isinstance(datestr, dt.datetime):
            self.__data = datestr
        else:
            self.__data = pdm.parse(datestr, tz = tz) if datestr else pdm.now()
    def __call__(self, beSTR = True) -> None:
        if beSTR :
            return self.__data.to_date_string()
        else:
            return self.__data
    def __str__(self) -> None:
        return self.__data.to_date_string()
    def __repr__(self) -> None:
        return self.__data.to_date_string()
    def toString(self, sformat="YYYY-MM-DD"):
        return self.__data.format(sformat)
    @property
    def Day(self) -> None:
        return int(self.toString("D"))
    @property
    def Month(self) -> None:
        return int(self.toString("M"))
    @property
    def Year(self) -> None:
        return self.toString("YYYY")
    @property
    def Hour(self) -> None:
        return int(self.toString("H"))
    @property
    def Time(self) -> None:
        return self.toString("HH:mm:ss")
    def end_of(self, interval, sformat = None):
        '''
        * week: date to last day of the week
        * month: date to last day of the month
        * year: date to last day of the year
        * decade: date to last day of the decade
        * century: date to last day of century
        '''
        if sformat:
            return self.__data.end_of(interval).format(sformat)
        else:
            return self.__data.end_of(interval)
    def start_of(self, interval, sformat = None):
        '''
        * day: time to 00:00:00
        * week: date to first day of the week and time to 00:00:00
        * month: date to first day of the month and time to 00:00:00
        * year: date to first day of the year and time to 00:00:00
        * decade: date to first day of the decade and time to 00:00:00
        * century: date to first day of century and time to 00:00:00
        '''
        if sformat:
            return self.__data.start_of(interval).format(sformat)
        else:
            return self.__data.start_of(interval)
    def add(self, **args):
        '''
        根据正负进行加减法操作。
        years, months, weeks, days, hours, minutes, seconds
        '''
        return self.__data.add(**args)
    def next(self, interval = "1 days", to_str = False):
        '''
        interval : days(defauls)|years|months|weeks|hours|minutes|seconds 间隔方式，
                    空格分割步长和单位，步长只为整数
        '''
        gaps = interval.split(" ")
        self.__data = self.__data.add(**{gaps[1]:int(gaps[0])})
        if to_str:
            return self.__call__()
    def period(self, direction = "backward", 
               including = False, 
               lenght = 7, interval = "1 days"):
        '''
        基准点为self.__data
        direction: backward(default)|forward 方向
        including: False(default)|True 是否包含基准点
        lenght: 7(default)|int 序列长度
        interval : days(defauls)|years|months|weeks|hours|minutes|seconds 间隔方式，空格分割步长和单位，步长只为整数
        '''
        gaps = interval.split(" ")
        basline = list(range(0 if including else 1, lenght*int(gaps[0]) if including else (lenght*int(gaps[0])+1), int(gaps[0])))
        lfun = self.__data.add if direction =="forward" else self.__data.subtract
        vfunc = np.vectorize(lambda x : lfun(**{gaps[1]:(int(x))}).start_of('day'))
        return vfunc(basline)
    def intz(self, tz:tzones|str) -> None:
        self.__data = self.__data.in_tz(tz if isinstance(tz,str) else tz())
    def disparity(self, other = None, abs = True, humans = None) :
        '''
        humans: cs,da,de,en,en_gb,en_us,es,fa,fo,fr,he,id,it,ja,ko,lt,nb,nl,nn,pl,pt_br,ru,sk,sv,tr,zh
        not for human , continue using:
            in_weeks()
            in_days()
            in_hours()
            in_minutes()
            in_seconds()
            years,months,weeks,days,hours,minutes,seconds,microseconds
        '''
        if humans:
            if humans in ["cs","da","de","en","en_gb","en_us","es","fa","fo","fr",
                          "he","id","it","ja","ko","lt","nb","nl","nn","pl","pt_br",
                          "ru","sk","sv","tr","zh"]:
                self.__data.diff_for_humans(dt=other,abs=abs,locale=humans)
            else:
                self.__data.diff_for_humans(dt=other,abs=abs,locale="en")
        else:
            self.__data.diff(dt=other,abs=abs)

###################
# Static Data
###################

'''
快速引用时区数据
'''

BEIJING = tzones.Beijing
CHINA = tzones.Beijing
TOKYO = tzones.Japan
TOKIO = tzones.Japan
EUROPE = tzones.Germany
USA = tzones.USAE
UTC = tzones.UTC

###################
# Functions
###################

def parse(tdt, tformat = None) -> simdate:
    if tformat is None:
        data = pdm.parse(tdt, tz = CHINA())
    else:
        data = pdm.from_format(tdt, tformat, tz = BEIJING())
    return simdate(datestr=data)

def now(sformat = None) -> simdate|str:
    tdt = simdate()
    if sformat is None:
        return tdt
    else :
        return tdt.toString(sformat)

def yesterday(by = None, sformat = None) -> simdate|str:
    if by is None:
        tdt = pdm.yesterday()
    else:
        tdt = pdm.parse(by, tz=tzones.Beijing())
        tdt = tdt.subtract(days = 1)
    if sformat is None:
        return simdate(datestr=tdt)
    else :
        return tdt.format(sformat)

def gap_youtube(keydate = None, interval = "1 month"):
    '''
    获取上一个整周期的YouTube格式数据。
    interval : day|year|month(defauls)|week|hour|minute|second 间隔方式，空格分割步长和单位，步长只为整数
    例如：
    - 最近7天， `gap_youtube(interval = "1 weeks")`；
    - 上个月： `gap_youtube()`。
    '''
    if keydate :
        tdt = pdm.parse(keydate, tz=tzones.Beijing())
    else:
        tdt = pdm.now()
    ointerval = interval.split(' ') if "s" in interval else (interval+"s").split(' ')
    bgp = ointerval[-1][:-1]
    res = [
                tdt.subtract(**{ointerval[1]:(int(ointerval[0]))}).start_of(bgp).format('YYYY-MM-DD'),
                tdt.start_of(bgp).format('YYYY-MM-DD')
    ]
    return res

def lastmonth(by = None, sformat = "YYYY-MM"):
    if by is None :
        tdt = pdm.now()
        tdt = tdt.subtract(months = 1).start_of('month')
    else:
        tdt = pdm.parse(by, tz=tzones.Beijing())
        tdt = tdt.subtract(months = 1)
    if sformat is None:
        return parse(tdt)
    else:
        return tdt.format(sformat)

def parser(datestr, tz = tzones.Beijing(), tformat = None):
    if tformat is None:
        fup = np.vectorize(lambda x: parse(x, tz = tz))
    else:
        fup = np.vectorize(lambda x: parse(pdm.from_format(x, tformat)))
    if np.iterable(datestr) :
        return fup(datestr)
    else:
        raise(ValueError("数据不支持迭代！"))

###################
# Main
###################

if __name__ == '__main__' :
    tdt = simdate()
    tdt.next()
    print(tdt.toString())
    print(tdt.period())
    print(yesterday().toString())