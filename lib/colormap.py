import pandas as pd
import numpy as np
import plotly.express as px
from functools import reduce
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap,Colormap

_KEYCOLORS = pd.DataFrame(
    {
        "color": ['LightPink', 'Pink', 'Crimson', 'LavenderBlush', 'PaleVioletRed', 'HotPink', 
                'DeepPink', 'MediumVioletRed', 'Orchid', 'Thistle', 'plum', 'Violet', 'Magenta', 
                'Fuchsia', 'DarkMagenta', 'Purple', 'MediumOrchid', 'DarkVoilet', 'DarkOrchid', 
                'Indigo', 'BlueViolet', 'MediumPurple', 'MediumSlateBlue', 'SlateBlue', 
                'DarkSlateBlue', 'Lavender', 'GhostWhite', 'Blue', 'MediumBlue', 'MidnightBlue', 
                'DarkBlue', 'Navy', 'RoyalBlue', 'CornflowerBlue', 'LightSteelBlue', 
                'LightSlateGray', 'SlateGray', 'DoderBlue', 'AliceBlue', 'SteelBlue', 
                'LightSkyBlue', 'SkyBlue', 'DeepSkyBlue', 'LightBLue', 'PowDerBlue', 'CadetBlue',
                'Azure', 'LightCyan', 'PaleTurquoise', 'Cyan', 'Aqua', 'DarkTurquoise', 
                'DarkSlateGray', 'DarkCyan', 'Teal', 'MediumTurquoise', 'LightSeaGreen', 
                'Turquoise', 'Auqamarin', 'MediumAquamarine', 'MediumSpringGreen', 'MintCream', 
                'SpringGreen', 'SeaGreen', 'Honeydew', 'LightGreen', 'PaleGreen', 'DarkSeaGreen', 
                'LimeGreen', 'Lime', 'ForestGreen', 'Green', 'DarkGreen', 'Chartreuse', 
                'LawnGreen', 'GreenYellow', 'OliveDrab', 'Beige', 'LightGoldenrodYellow', 'Ivory',
                'LightYellow', 'Yellow', 'Olive', 'DarkKhaki', 'LemonChiffon', 'PaleGodenrod', 
                'Khaki', 'Gold', 'Cornislk', 'GoldEnrod', 'FloralWhite', 'OldLace', 'Wheat', 
                'Moccasin', 'Orange', 'PapayaWhip', 'BlanchedAlmond', 'NavajoWhite', 
                'AntiqueWhite', 'Tan', 'BrulyWood', 'Bisque', 'DarkOrange', 'Linen', 'Peru', 
                'PeachPuff', 'SandyBrown', 'Chocolate', 'SaddleBrown', 'SeaShell', 'Sienna', 
                'LightSalmon', 'Coral', 'OrangeRed', 'DarkSalmon', 'Tomato', 'MistyRose', 'Salmon',
                'Snow', 'LightCoral', 'RosyBrown', 'IndianRed', 'Red', 'Brown', 'FireBrick', 
                'DarkRed', 'Maroon', 'White', 'WhiteSmoke', 'Gainsboro', 'LightGrey', 'Silver', 
                'DarkGray', 'Gray', 'DimGray'],
        "cname": ['浅粉红', '粉红', '猩红', '脸红的淡紫色', '苍白的紫罗兰红色', '热情的粉红', '深粉色', '适中的紫罗兰红色', 
                '兰花的紫色', '蓟', '李子', '紫罗兰', '洋红', '灯笼海棠(紫红色)', '深洋红色', '紫色', '适中的兰花紫', 
                '深紫罗兰色', '深兰花紫', '靛青', '深紫罗兰的蓝色', '适中的紫色', '适中的板岩暗蓝灰色', '板岩暗蓝灰色',
                '深岩暗蓝灰色', '熏衣草花的淡紫色', '幽灵的白色', '纯蓝', '适中的蓝色', '午夜的蓝色', '深蓝色', '海军蓝', 
                '皇军蓝', '矢车菊的蓝色', '淡钢蓝', '浅石板灰', '石板灰', '道奇蓝', '爱丽丝蓝', '钢蓝', '淡蓝色', 
                '天蓝色', '深天蓝', '淡蓝', '火药蓝', '军校蓝', '蔚蓝色', '淡青色', '苍白的绿宝石', '青色', '水绿色', 
                '深绿宝石', '深石板灰', '深青色', '水鸭色', '适中的绿宝石', '浅海洋绿', '绿宝石', '绿玉/碧绿色', 
                '适中的碧绿色', '适中的春天的绿色', '薄荷奶油', '春天的绿色', '海洋绿', '蜂蜜', '淡绿色', '苍白的绿色', 
                '深海洋绿', '酸橙绿', '酸橙色', '森林绿', '纯绿', '深绿色', '查特酒绿', '草坪绿', '绿黄色', '橄榄土褐色', 
                '米色(浅褐色)', '浅秋麒麟黄', '象牙', '浅黄色', '纯黄', '橄榄', '深卡其布', '柠檬薄纱', '灰秋麒麟', 
                '卡其布', '金', '玉米色', '秋麒麟', '花的白色', '老饰带', '小麦色', '鹿皮鞋', '橙色', '番木瓜', '漂白的杏仁', 
                'Navajo白', '古代的白色', '晒黑', '结实的树', '(浓汤)乳脂,番茄 等', '深橙色', '亚麻布', '秘鲁', '桃色', 
                '沙棕色', '巧克力', '马鞍棕色', '海贝壳', '黄土赭色', '浅鲜肉(鲑鱼)色', '珊瑚', '橙红色', '深鲜肉(鲑鱼)色', 
                '番茄', '薄雾玫瑰', '鲜肉(鲑鱼)色', '雪', '淡珊瑚色', '玫瑰棕色', '印度红', '纯红', '棕色', '耐火砖', 
                '深红色', '栗色', '纯白', '白烟', 'Gainsboro', '浅灰色', '银白色', '深灰色', '灰色', '暗淡的灰色'],
        "hex": ['#FFB6C1', '#FFC0CB', '#DC143C', '#FFF0F5', '#DB7093', '#FF69B4', '#FF1493', '#C71585', '#DA70D6', 
                '#D8BFD8', '#DDA0DD', '#EE82EE', '#FF00FF', '#FF00FF', '#8B008B', '#800080', '#BA55D3', '#9400D3', 
                '#9932CC', '#4B0082', '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#E6E6FA', '#F8F8FF', 
                '#0000FF', '#0000CD', '#191970', '#00008B', '#000080', '#4169E1', '#6495ED', '#B0C4DE', '#778899', 
                '#708090', '#1E90FF', '#F0F8FF', '#4682B4', '#87CEFA', '#87CEEB', '#00BFFF', '#ADD8E6', '#B0E0E6', 
                '#5F9EA0', '#F0FFFF', '#E1FFFF', '#AFEEEE', '#00FFFF', '#00FFFF', '#00CED1', '#2F4F4F', '#008B8B', 
                '#008080', '#48D1CC', '#20B2AA', '#40E0D0', '#7FFFAA', '#00FA9A', '#F5FFFA', '#00FF7F', '#3CB371', 
                '#2E8B57', '#F0FFF0', '#90EE90', '#98FB98', '#8FBC8F', '#32CD32', '#00FF00', '#228B22', '#008000', 
                '#006400', '#7FFF00', '#7CFC00', '#ADFF2F', '#556B2F', '#6B8E23', '#FAFAD2', '#FFFFF0', '#FFFFE0', 
                '#FFFF00', '#808000', '#BDB76B', '#FFFACD', '#EEE8AA', '#F0E68C', '#FFD700', '#FFF8DC', '#DAA520', 
                '#FFFAF0', '#FDF5E6', '#F5DEB3', '#FFE4B5', '#FFA500', '#FFEFD5', '#FFEBCD', '#FFDEAD', '#FAEBD7', 
                '#D2B48C', '#DEB887', '#FFE4C4', '#FF8C00', '#FAF0E6', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', 
                '#8B4513', '#FFF5EE', '#A0522D', '#FFA07A', '#FF7F50', '#FF4500', '#E9967A', '#FF6347', '#FFE4E1', 
                '#FA8072', '#FFFAFA', '#F08080', '#BC8F8F', '#CD5C5C', '#FF0000', '#A52A2A', '#B22222', '#8B0000', 
                '#800000', '#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', '#C0C0C0', '#A9A9A9', '#808080', '#696969'],
        "rgb": ['(255,182,193)', '(255,192,203)', '(220,20,60)', '(255,240,245)', '(219,112,147)', '(255,105,180)', 
                '(255,20,147)', '(199,21,133)', '(218,112,214)', '(216,191,216)', '(221,160,221)', '(238,130,238)', 
                '(255,0,255)', '(255,0,255)', '(139,0,139)', '(128,0,128)', '(186,85,211)', '(148,0,211)', 
                '(153,50,204)', '(75,0,130)', '(138,43,226)', '(147,112,219)', '(123,104,238)', '(106,90,205)', 
                '(72,61,139)', '(230,230,250)', '(248,248,255)', '(0,0,255)', '(0,0,205)', '(25,25,112)', '(0,0,139)', 
                '(0,0,128)', '(65,105,225)', '(100,149,237)', '(176,196,222)', '(119,136,153)', '(112,128,144)', 
                '(30,144,255)', '(240,248,255)', '(70,130,180)', '(135,206,250)', '(135,206,235)', '(0,191,255)', 
                '(173,216,230)', '(176,224,230)', '(95,158,160)', '(240,255,255)', '(225,255,255)', '(175,238,238)', 
                '(0,255,255)', '(0,255,255)', '(0,206,209)', '(47,79,79)', '(0,139,139)', '(0,128,128)', 
                '(72,209,204)', '(32,178,170)', '(64,224,208)', '(127,255,170)', '(0,250,154)', '(245,255,250)', 
                '(0,255,127)', '(60,179,113)', '(46,139,87)', '(240,255,240)', '(144,238,144)', '(152,251,152)', 
                '(143,188,143)', '(50,205,50)', '(0,255,0)', '(34,139,34)', '(0,128,0)', '(0,100,0)', '(127,255,0)', 
                '(124,252,0)', '(173,255,47)', '(85,107,47)', '(107,142,35)', '(250,250,210)', '(255,255,240)', 
                '(255,255,224)', '(255,255,0)', '(128,128,0)', '(189,183,107)', '(255,250,205)', '(238,232,170)', 
                '(240,230,140)', '(255,215,0)', '(255,248,220)', '(218,165,32)', '(255,250,240)', '(253,245,230)', 
                '(245,222,179)', '(255,228,181)', '(255,165,0)', '(255,239,213)', '(255,235,205)', '(255,222,173)', 
                '(250,235,215)', '(210,180,140)', '(222,184,135)', '(255,228,196)', '(255,140,0)', '(250,240,230)', 
                '(205,133,63)', '(255,218,185)', '(244,164,96)', '(210,105,30)', '(139,69,19)', '(255,245,238)', 
                '(160,82,45)', '(255,160,122)', '(255,127,80)', '(255,69,0)', '(233,150,122)', '(255,99,71)', 
                '(255,228,225)', '(250,128,114)', '(255,250,250)', '(240,128,128)', '(188,143,143)', '(205,92,92)', 
                '(255,0,0)', '(165,42,42)', '(178,34,34)', '(139,0,0)', '(128,0,0)', '(255,255,255)', '(245,245,245)', 
                '(220,220,220)', '(211,211,211)', '(192,192,192)', '(169,169,169)', '(128,128,128)', '(105,105,105)']
    }
)

_PALETTENAMES = {
    "namel": ["cartocolors.diverging", "cartocolors.qualitative", "cartocolors.sequential",
             "cmocean.diverging", "cmocean.sequential", 
             "colorbrewer.diverging", "colorbrewer.qualitative", "colorbrewer.sequential",
             "lightbartlein.diverging", "lightbartlein.sequential",
             "matplotlib", "mycarta", 
             "scientific.diverging", "scientific.sequential","tableau","wesanderson"],
    "keywords": [["ArmyRose","Earth","Fall","Geuser","TealRose","Temps","Tropic"],
                 ["Antique","Bold","Pastel","Prism","Safe","Vivid"],
                 ["BluGrn","BluYl","BrwnYl","Burg","BurgYl","DarkMint","Emrld","Magenta","Mint","OrYel","Peach",
                  "PinkYl","Purp","PurpOr","RedOr","Sunset","SunsetDark","Teal","TealGrn","agGrnYl","agSunset"],
                 ["Balance","Curl","Delta"],["Algae","Amp","Deep","Dense","Gray","Haline","Ice","Matter","Oxy",
                  "Phase","Solar","Speed","Tempo","Thermal","Turbid"],
                 ["BrBG","PRGn","PiYG","PuOr","RdBu","RdGy","RdYlBu","RdYlGn","Spectral"],
                 ["Accent","Dark2","Paired[13","Pastel1[10","Pastel2","Set1[10","Set2","Set3[13"],
                 ["Blues","BuGn","BuPu","GnBu","Greens","Greys","OrRd","Oranges","PuBu","PuBuGn","PuRd","Purples",
                  "RdPu","Reds","YlGn","YlGnBu","YlOrBr","YlOrRd"],
                 ["BlueDarkOrange12","BlueDarkOrange18[19","BlueDarkRed12","BlueDarkRed18[19","BlueGreen[15","BlueGrey[9",
                  "BlueOrange10[10","BlueOrange12","BlueOrange8[9","BlueOrangeRed[15","BrownBlue10[11","BrownBlue12",
                  "GreenMagenta[17","RedYellowBlue[12"],["Blues10","Blues7[8"],
                 ["Inferno","Magma","Plasma","Viridis"],["Cube1","CubeYF","LinearL"],["Berlin","Broc","Cork","Lisbon","Roma","Tofino","Vik"],
                 ["Acton","Bamako","Batlow","Bilbao","Buda","Davos","Devon","GrayC","Hawaii","Imola","LaJolla","LaPaz",
                  "Nuuk","Oleron","Oslo","Tokyo","Turku"],["BlueRed_6","BlueRed_12","ColorBlind_10","Gray_5","GreenOrange_6",
                  "GreenOrange_12","PurpleGray_6","PurpleGray_12","Tableau_10","Tableau_20","TableauLight_10","TableauMedium_10","TrafficLight_9"],
                 ["Aquatic1_5","Aquatic2_5","Aquatic3_5","Cavalcanti_5","Chevalier_4","Darjeeling1_4","Darjeeling2_5","Darjeeling3_5",
                  "Darjeeling4_5","FantasticFox1_5","FantasticFox2_5","GrandBudapest1_4","GrandBudapest2_4","GrandBudapest3_6","GrandBudapest4_5",
                  "GrandBudapest5_5","IsleOfDogs1_5","IsleOfDogs2_6","IsleOfDogs3_4","Margot1_5","Margot2_4","Margot3_4","Mendl_4","Moonrise1_5",
                  "Moonrise2_4","Moonrise3_4","Moonrise4_5","Moonrise5_6","Moonrise6_5","Moonrise7_5","Royal1_4","Royal2_5","Royal3_5","Zissou_5"]
                ],
    "colors": [list(range(2,8)),list(range(2,11)),list(range(2,8)),list(range(3,21)),
               list(range(3,21)),list(range(3,12)),list(range(3,9)),list(range(2,10)),
               list(range(2,13)),list(range(3,11)),list(range(3,21)),list(range(3,21)),
               list(range(2,21)),list(range(2,21)),[],[]]
}

_PXPALETTE = {
    "colorscale": px.colors.named_colorscales(),
    "qualitative": ['Alphabet', 'Antique', 'Bold', 'D3', 'Dark2', 'Dark24', 'G10', 'Light24', 'Pastel', 'Pastel1',
                    'Pastel2', 'Plotly', 'Prism', 'Safe', 'Set1', 'Set2', 'Set3', 'T10', 'Vivid'],
    "sequential": ['Aggrnyl', 'Agsunset', 'Blackbody', 'Bluered', 'Blues', 'Blugrn', 'Bluyl', 'Brwnyl', 'BuGn', 'BuPu', 
                   'Burg', 'Burgyl', 'Cividis', 'Darkmint', 'Electric', 'Emrld', 'GnBu', 'Greens', 'Greys', 'Hot', 
                   'Inferno', 'Jet', 'Magenta', 'Magma', 'Mint', 'OrRd', 'Oranges', 'Oryel', 'Peach', 'Pinkyl', 'Plasma', 
                   'Plotly3', 'PuBu', 'PuBuGn', 'PuRd', 'Purp', 'Purples', 'Purpor', 'Rainbow', 'RdBu', 'RdPu', 'Redor', 
                   'Reds', 'Sunset', 'Sunsetdark', 'Teal', 'Tealgrn', 'Turbo', 'Viridis', 'YlGn', 'YlGnBu', 'YlOrBr', 
                   'YlOrRd', 'algae', 'amp', 'deep', 'dense', 'gray', 'haline', 'ice', 'matter', 'solar', 'speed', 'tempo', 'thermal', 'turbid'],
    "cyclical":['Edge', 'HSV', 'IceFire', 'Phase', 'Twilight', 'mrybm', 'mygbm'],
    "diverging":['Armyrose', 'BrBG', 'Earth', 'Fall', 'Geyser', 'PRGn', 'PiYG', 'Picnic', 'Portland', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 
                 'RdYlGn', 'Spectral', 'Tealrose', 'Temps', 'Tropic', 'balance', 'curl', 'delta', 'oxy']
}

_MPLPALETTE = {
            'Perceptually_Uniform_Sequential':
                ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
            'Sequential':[
                'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
                'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
                'hot', 'afmhot', 'gist_heat', 'copper'],
            'Diverging': [
                'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
                'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'],
            'Cyclic':['twilight', 'twilight_shifted', 'hsv'],
            'Qualitative': [
                'Pastel1', 'Pastel2', 'Paired', 'Accent',
                'Dark2', 'Set1', 'Set2', 'Set3',
                'tab10', 'tab20', 'tab20b', 'tab20c'],
            'Miscellaneous':[
                'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
                'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
                'gist_ncar']}

def _con_palettable(name, key, color):
    if '[' in key:
        tx,i = key.split('[')
        co = list(range(color[0],int(i)))
    else:
        tx = key
        co = color
    nlist = name.split('.')
    colors = list(map(lambda x: "{}_{}".format(tx,x), co)) if co else [tx]
    rnl = list(map(lambda x:'.'.join(nlist+[x]), colors))
    return rnl

def _cov_palettable():
    data = pd.DataFrame(_PALETTENAMES)
    blist = list(map(lambda x: data.iloc[x],range(0,len(data))))
    data = list(map(lambda x: list(map(lambda y: [x.namel,y,x.colors],x.keywords)), blist))
    data = reduce(lambda x,y: x+y, data)
    res = list(map(lambda x: _con_palettable(*x), data))
    res = reduce(lambda x,y: x+y, res)
    return(res)

def _cov_pxcolors():
    res = _PXPALETTE.keys()
    res = list(map(lambda y: list(map(lambda x: "{}.{}".format(y,x),_PXPALETTE[y])), res))
    res = reduce(lambda x,y: x+y, res)
    return res

def _cov_mplcolors():
    res = _MPLPALETTE.keys()
    res = list(map(lambda y: list(map(lambda x: "matplotlib.colors.{}.{}".format(y,x),_MPLPALETTE[y])),res))
    res = reduce(lambda x,y: x+y, res)
    return res

def named_palettes():
    res = _KEYCOLORS.color.tolist()
    res = res + _cov_palettable()
    res = res + _cov_pxcolors()
    res = res + _cov_mplcolors()
    return res

def _to_rgb(nstr):
    data = eval(nstr[3:])
    data = list(map(lambda x: x/255,data))
    return data

def gen_palette(tnamed):
    """整合读取不同palette的颜色数据"""
    if tnamed[-2:] == '_r':
        named = tnamed[:-2]
        rsetr = True
    else:
        named = tnamed
        rsetr = False
    # https://stackoverflow.com/a/6677505
    if named in _KEYCOLORS.color.tolist():
        res = sns.light_palette(_KEYCOLORS.query("color=='{}'".format(named)).hex.values[0], reverse=rsetr,as_cmap=True)
    elif named in _cov_palettable() :
        palette_split = named.split(".")
        palette_name = palette_split[-1]
        palette_func = getattr(
            __import__(
            "palettable.{}".format(".".join(palette_split[:-1])),
            fromlist=[palette_name],
            ),
            palette_name,
        )
        res = palette_func.get_mpl_colormap()
    elif named in _cov_pxcolors() :
        palette_split = tnamed.split(".")
        palette_name = palette_split[-1]
        palette_func = getattr(
            __import__(
            "plotly.express.colors",
            fromlist=[palette_split[0]],
            ),
        palette_split[0]
        )
        res = list(map(_to_rgb,eval("palette_func.{}".format(palette_name))))
        res = LinearSegmentedColormap.from_list(palette_name,res)
    elif named in _cov_mplcolors():
        palette_split = tnamed.split(".")
        palette_name = palette_split[-1]
        palette_func = getattr(
            __import__(
            "matplotlib.cm",
            fromlist=[palette_name],
            ),
        palette_name,
        )
        res = palette_func
    else:
        np.random.seed(73)
        ags = dict(zip(['h','l','s'],np.random.rand(3)))
        res = sns.hls_palette(**ags,as_cmap=True)
    return res
