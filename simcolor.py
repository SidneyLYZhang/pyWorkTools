"""

"""



from . import colormaps as ccmap
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pyecharts import options as opts
from pyecharts.charts import Graph
import plotly.express as px
import seaborn as sns
import holoviews as hv
from functools import reduce
from holoviews import opts, dim
from bokeh.sampledata.les_mis import data as testdata
import pathlib as pl
import pandas as pd
import numpy as np
import matplotlib
import textwrap
import re



class pycolors(object):
    '''
    同时提供多种颜色选择。
    接受HEX颜色代码输入；也可以使用基准颜色卡。
    '''
    def __init__(self, name = None, quantities = 20) -> None:
        nname = name if name else "LightSeaGreen"
        if re.match("^#(([A-Fa-f0-9]{3})|([A-Fa-f0-9]{6}))$", nname):
            self.__data = "GivenColor"
            self.__colormap = sns.light_palette(nname, reverse=False,as_cmap=True)
        else:
            self.__data = nname if nname in ccmap.named_palettes() else "LightSeaGreen"
            self.__colormap = ccmap.gen_palette(self.__data)
        self.__quantities = quantities
    def __getitem__(self,key):
        '''
        返回色卡中的一个颜色。直接使用 color[x]的方式提取颜色。
        提取的是minicolor类定义的颜色。为了使用“.hax”方法构建的这个简单minicolor类。
        '''
        return minicolor(self.__colormap(key/self.__quantities))
    def __str__(self):
        return str(self.rgb255_str)
    def __repr__(self) -> str:
        return self.__str__()
    def __mul__(self, other):
        res = self.rgba
        if isinstance(other, pycolors):
            res = res * other.rgba
        else:
            res = list(map(lambda x: (*x[:-1],other), res))
        return res
    def colormaps(self):
        '''提供色卡，matplotlib的色卡方法'''
        return self.__colormap
    def show(self):
        '''展示色卡'''
        sns.palplot(self.__colormap)
        plt.show()
    def set(self,quantities = 20):
        self.__quantities = quantities
    @property
    def hex(self):
        return list(map(matplotlib.colors.to_hex, self.rgba))
    @property
    def rgb(self):
        return list(map(matplotlib.colors.to_rgb, self.rgba))
    @property
    def rgb255(self):
        colors = list(map(matplotlib.colors.to_rgb, self.rgba))
        colors = list(map(px.colors.convert_to_RGB_255, colors))
        return colors
    @property
    def rgb255_str(self):
        colors = self.rgb255
        colors = list(map(lambda x: "RGB{}".format(x), colors))
        return colors
    @property
    def rgba(self):
        return self.__colormap(np.linspace(0,1,self.__quantities))
    @property
    def colorname(self):
        return self.__data.split('.')[-1]
    @property
    def palettename(self):
        return self.__data
    @staticmethod
    def list_names(println=True):
        '''颜色卡系列输出'''
        nameslist = ccmap.named_palettes()
        if println :
            txt = " ".join(nameslist)
            print(textwrap.fill(txt))
        else:
            return nameslist
    @staticmethod
    def searchcolor(name):
        fun = lambda x, y: re.match((x+'.*'),y)
        vfunc = np.vectorize(lambda m: fun(name, m))
        res = vfunc(pycolors.list_names(println=False))
        res = res[res != np.array(None)]
        vfunc = np.vectorize(lambda m: m.group())
        res = vfunc(res).tolist()
        return (res if len(res)!=1 else res[0])


class minicolor(object):
    '''
    纯粹简装颜色类
    为了帮助pycolors提供更丰富的处理、展示方案而存在。
    '''
    def __init__(self, color) -> None:
        self.__color = color
    def __str__(self) -> str:
        return self.hex()
    def __repr__(self) -> str:
        return self.hex()
    @property
    def rgb(self):
        return matplotlib.colors.to_rgb(self.__color)
    @property
    def hex(self):
        return matplotlib.colors.to_hex(self.rgb)
    @property
    def rgb255(self):
        return px.colors.convert_to_RGB_255(self.rgb)
    @property
    def rgba(self):
        return self.__color




