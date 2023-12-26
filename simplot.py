"""
     _           ____  _       _
 ___(_)_ __ ___ |  _ \| | ___ | |_
/ __| | '_ ` _ \| |_) | |/ _ \| __|
\__ \ | | | | | |  __/| | (_) | |_
|___/_|_| |_| |_|_|   |_|\___/ \__|

================================================================================

Version : 1.2.0
Update : 2023-12-26
Author: Sidney Zhang<zly@lyzhang.me>

================================================================================

Under construction ... .. .  .   .    .     .      .

"""

###################
# Packages
###################

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import pandas as pd
import numpy as np
import geopandas as gpd
from iso3166 import countries
from PIL import Image
import os
import win32com.client as wcc  # 安装好 pywin32 后即可
from enum import Enum
import shutil

###################
# Classes
###################

class bullet(object):
    '''
    子弹图的绘制。
    '''
    def __init__(self, data, fitted = False, limits = None, palette = None) -> None:
        '''
        fitted data: 为已经整理好的
        '''
        self.data = data
        self.__fitdata = data if fitted else None
        self.__limits = limits if fitted else None
        self.__pldata = None
        self.__config = {
            'Font':'Simhei',
            'palette': palette if palette else "green",
            'target_color': '#f7f7f7',
            'bar_color': '#252525',
            'label_color': 'black',
            'keep_label': None, #分类数据顺序
            'pass_zero': True,
            'orientations': 'horizontal', #方向：{'vertical', 'horizontal'}
            'figsize': (12,8),
            'labels': None,
            'formatter': None,
            'axis_label' : None,
            'title' : None,
        }
    def datafitting(self, values = None, index = None, columns = None, aggfunc = 'sum'):
        if self.__fitdata is None:
            self.__fitdata = self.data.pivot_table(values=values,index=index,columns=columns,aggfunc=aggfunc)
        if self.__config['keep_label'] :
            self.__fitdata = self.__fitdata[self.__config['keep_label']]
        if self.__config['pass_zero']:
            for i in self.__fitdata.columns.tolist():
                self.__fitdata.loc[self.__fitdata[i]==0,i] = np.nan
        res = self.__fitdata.describe().T
        res = res[['mean','50%']]
        self.__pldata = list(map(lambda x:list([x[0],*x[1]]),res.iterrows()))
        res = res.describe().loc[["min","25%","75%","max"]]
        if self.__limits is None:
            self.__limits = list(map(lambda x: min(x[1]) if x[0]!="max" else np.ceil(max(x[1])*1.1),res.iterrows()))
        if self.__config["labels"] is None:
            self.__config["labels"] = [' ']*len(self.__limits)
    def config(self,**args):
        self.__config.update(args)
    def heatmap(self):
        '''
        直接使用fitted data数据绘制热力图。
        '''
        plt.figure(figsize=self.__config["figsize"])
        sns.heatmap(self.__fitdata.T,cmap=self.__config["palette"])
    def plot(self, save = None):
            # Determine the max value for adjusting the bar height
            # Dividing by 10 seems to work pretty well
            h = self.__limits[-1] / 10
            plt.rcParams['font.sans-serif'] = [self.__config['Font']]
            # Use the green palette as a sensible default
            if isinstance(self.__config["palette"], str):
                tPalette = sns.light_palette(self.__config["palette"], len(self.__limits), reverse=False)
            else:
                tPalette = self.__config["palette"]
            
            # Must be able to handle one or many data sets via multiple subplots
            if len(self.__pldata) == 1:
                RoCo_Nums = {
                    "sharex" if self.__config['orientations']=='horizontal' else "sharey" : True
                }
                fig, ax = plt.subplots(figsize=self.__config["figsize"], **RoCo_Nums)
            else:
                RoCo_Nums = {
                    "nrows" if self.__config['orientations']=='horizontal' else "ncols" : len(self.__pldata),
                    "sharex" if self.__config['orientations']=='horizontal' else "sharey" : True
                }
                fig, axarr = plt.subplots(figsize=self.__config["figsize"], **RoCo_Nums)

            # Add each bullet graph bar to a subplot
            for idx, item in enumerate(self.__pldata):
                
                # Get the axis from the array of axes returned when the plot is created
                if len(self.__pldata) > 1:
                    ax = axarr[idx]

                # Formatting to get rid of extra marking clutter
                ax.set_aspect('equal')
                if self.__config['orientations']=='horizontal':
                    ax.set_yticklabels([item[0]])
                    ax.set_yticks([1])
                else:
                    ax.set_xticklabels([item[0]])
                    ax.set_xticks([1])
                ax.spines['bottom'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)

                prev_limit = 0
                for idx2, lim in enumerate(self.__limits):
                    # Draw the bar
                    if self.__config['orientations']=='horizontal':
                        ax.barh([1], lim - prev_limit, left=prev_limit, height=h,
                                color=tPalette[idx2])
                    else:
                        ax.bar([1],lim - prev_limit, bottom=prev_limit, width=h,
                               color=tPalette[idx2])
                    prev_limit = lim
                rects = ax.patches
                # The last item in the list is the value we're measuring
                # Draw the value we're measuring
                if self.__config['orientations']=='horizontal':
                    ax.barh([1], item[1], height=(h / 3), color=self.__config["bar_color"])
                else:
                    ax.bar([1], item[1], width=(h / 3), color=self.__config["bar_color"])

                # Need the ymin and max in order to make sure the target marker
                # fits
                if self.__config['orientations']=='horizontal':
                    ymin, ymax = ax.get_ylim()
                    ax.vlines(
                        item[2], ymin * .9, ymax * .9, linewidth=1.5, color=self.__config["target_color"])
                else:
                    xmin, xmax = ax.get_xlim()
                    ax.hlines(
                        item[2], xmin*0.9, xmax*0.9, linewidth=1.5, color=self.__config["target_color"])

            # Now make some labels
            if self.__config["labels"] is not None:
                for rect, label in zip(rects, self.__config["labels"]):
                    if self.__config['orientations']=='horizontal':
                        height = rect.get_height()
                        ax.text(
                            rect.get_x() + rect.get_width() / 2,
                            -height * .4,
                            label,
                            ha='center',
                            va='bottom',
                            color=self.__config["label_color"])
                    else:
                        width = rect.get_width()
                        ax.text(
                            -width * .4,
                            rect.get_y() + rect.get_height() / 2,
                            label,
                            ha='left',
                            va='center',
                            color=self.__config["label_color"])
            if self.__config["formatter"]:
                if self.__config['orientations']=='horizontal':
                    ax.xaxis.set_major_formatter(self.__config["formatter"])
                else:
                    ax.yaxis.set_major_formatter(self.__config["formatter"])
            if self.__config["axis_label"]:
                if self.__config['orientations']=='horizontal':
                    ax.set_xlabel(self.__config["axis_label"])
                else:
                    ax.set_ylabel(self.__config["axis_label"])
            if self.__config["title"]:
                fig.suptitle(self.__config["title"], fontsize=14)
            WHspace = {"hspace" if self.__config['orientations']=='horizontal' else "wspace":0}
            fig.subplots_adjust(**WHspace)

class geoploting(object):
    '''
    基于index设计，请注意resample之后reset_index。
    快速对国家/省份数据可视化。
    使用 scheme 控制分类绘图能力，在不使用时，为连续分布展示。
    可使用的绘图控制变量有：
        column -> 针对那列进行绘图
        scheme -> 分类方案
        cmap -> 使用的颜色
        figsize -> 画布尺寸
        legend -> 是否画图例
        legend_kwds -> 图里配置（location{'left', 'right', 'top', 'bottom'},orientation{'vertical', 'horizontal'},label,fmt,labels<分类名>,interval）
        k -> scheme条件下，需要的分类个数
        missing_kwds -> 缺失数据的绘制情况(color,edgecolor,hatch(https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html),label)
        categories -> 类别绘图指引
        classification_kwds -> scheme函数的参数调节（https://pysal.org/mapclassify/api.html）
        ax -> 用于叠加数据图层
    '''
    def __init__(self, data:pd.DataFrame, locations = None, keydata = None, gtype = 'global') -> None:
        self.__data = data
        self.__pconfig = {
            "column": keydata if keydata else list(data.columns)[1],
            "cmap": 'YlOrRd',
            "figsize": (14,10),
            "missing_kwds":{"color":"gainsboro"}
        }
        if locations in data.columns :
            self.__locations = locations
        elif locations is None :
            self.__locations = list(data.columns)[0]
        else:
            raise ValueError("地点数据有误。")
        self.__data = self.__trans(type = gtype)
    def __trans(self, type):
        if type == "global":
            underdata = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        elif type == "china":
            underdata = gpd.read_file("./Data/mapinfo/china.json")
        else:
            raise ValueError("Error type!")
        tmp = pd.DataFrame({'country':list(map(lambda x:countries.get(x).alpha3,self.__data[self.__locations]))},index=list(range(1,len(self.__data)+1)))
        tmp = pd.concat([self.__data,tmp],axis=1)
        tmp = underdata.iso_a3.apply(lambda x: tmp[tmp.country==x.upper()][self.__pconfig["column"]].to_list()[0] if x.upper() in tmp.country.unique() else None)
        tmp.name = self.__pconfig["column"]
        res = pd.concat([underdata,tmp],axis=1)
        return res
    def __str__(self) -> str:
        return str(self.__data)
    def __repr__(self) -> str:
        return self.__str__()
    def show(self) -> None:
        ax = self.__data.plot(**self.__pconfig)
        ax.set_axis_off()
    def save(self, fname, **kwgs):
        """
        保存图片。之际使用matploylib.pyplot的保存方法。
        在jupyter中，建议使用show()来查看后保存。
        """
        self.__data.plot(**self.__pconfig)
        plt.savefig(fname, **kwgs)
    def update_setting(self, **arge) -> None:
        self.__pconfig.update(arge)
    @staticmethod
    def scheme_list(println = False):
        tc = {"BoxPlot": "BoxPlot Map Classification.",
              "EqualInterval":"Equal Interval Classification.",
              "FisherJenks":"Fisher Jenks optimal classifier - mean based.",
              "FisherJenksSampled":"Fisher Jenks optimal classifier - mean based using random sample.",
              "HeadTailBreaks":"Head/tail Breaks Map Classification for Heavy-tailed Distributions.",
              "JenksCaspall":"Jenks Caspall Map Classification.",
              "JenksCaspallForced":"Jenks Caspall Map Classification with forced movements.",
              "JenksCaspallSampled":"Jenks Caspall Map Classification using a random sample.",
              "MaxP":"MaxP Map Classification.",
              "MaximumBreaks":"Maximum Breaks Map Classification.",
              "NaturalBreaks":"Natural Breaks Map Classification.",
              "Percentiles":"Percentiles Map Classification",
              "Quantiles":"Quantile Map Classification.",
              "StdMean":"Standard Deviation and Mean Map Classification.",
              "UserDefined":"User Specified Binning."}
        if println :
            for i in tc.keys():
                print("{:22}:->\t{}".format(i,tc[i]))
        else:
            return(list(tc.keys()))

class saveType(Enum):
    '''
    win32com使用VBA的API，可从官方教程中看到：
    https://learn.microsoft.com/en-us/office/vba/api/PowerPoint.Presentation.SaveAs
    编码来源：https://my.oschina.net/zxcholmes/blog/484789
    '''
    PDF = 32
    JPG = 17
    PNG = 18

class ppTrans(object):
    def __init__(self,file, to = None) -> None:
        self.__ofile = file
        self.__to = to
    def saveas(self, savetype = saveType.JPG):
        '''
        savetype : 默认保存为JPG格式。具体可选格式见saveType。
        '''
        if os.path.exists(self.__ofile): # 判断文件是否存在
            ppt_app = wcc.Dispatch('PowerPoint.Application')
            ppt = ppt_app.Presentations.Open(os.path.abspath(self.__ofile))  # 打开 ppt
            ppt.SaveAs(os.path.abspath(self.__ofile), savetype.value)
            ppt_app.Quit()
        else:
            raise Exception("请检查文件是否存在!")
    def trans(self, width = 700, intermediate = False):
        '''
        width : 画幅宽度，可以直接指定宽度像素，也可以使用字符串数据输入百分比。（700； "22.1%"）
                指定为None的时候，不进行图像缩放。
        intermediate : 是否保留中间过程，如果需要保留转换的中间图片数据，则设置为True，默认不保留。
        '''
        self.saveas()
        picPath = os.path.splitext(self.__ofile)[0]
        todir = self.__to if self.__to else os.path.dirname(self.__ofile)
        picList = os.listdir(picPath)
        ims = Image.open(os.path.join(picPath, "幻灯片1.JPG")) # 获取单个图片
        # 确定压缩后的图片大小
        if isinstance(width, str):
            qw = float(width[:-1])/100.0
            nwidth, nheight = (int(ims.width*qw), int(ims.height*qw))
        elif width is None:
            nwidth, nheight = ims.size
        else:
            nwidth, nheight = (width, int(ims.height*width/ims.width))
        lcanvas = Image.new(ims.mode, (nwidth, nheight * len(picList)))  # 创建长图底板
        ims.close()
        for i in range(1,len(picList)+1):
            img = Image.open(os.path.join(picPath, "幻灯片{}.JPG".format(i)))
            nim = img.resize((nwidth,nheight), resample=Image.Resampling.LANCZOS)
            lcanvas.paste(nim, box=(0, (i-1) * nheight))
            img.close()
        # 保存长图
        lcanvas.save(os.path.join(todir, '{}.png'.format(os.path.basename(picPath))))
        # 对中间数据进行保留，默认不保留
        if not intermediate :
            shutil.rmtree(picPath)
        else:
            # 把导出的ppt图片移动到指定目录下。
            shutil.move(picPath, todir)
            print("PPT导出的图片在： \n{}".format(todir))


############
# FUNCTIONS
############