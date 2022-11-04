import json
import shutil
import os
import pandas as pd
import numpy as np
import requests
import time
from shutil import copy
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar,Map,Line

name_map = {'Singapore Rep.': '新加坡',
 'Dominican Rep.': '多米尼加',
 'Palestine': '巴勒斯坦',
 'Bahamas': '巴哈马',
 'Timor-Leste': '东帝汶',
 'Afghanistan': '阿富汗',
 'Guinea-Bissau': '几内亚比绍',
 "Côte d'Ivoire": '科特迪瓦',
 'Siachen Glacier': '锡亚琴冰川',
 'Br. Indian Ocean Ter.': '英属印度洋领土',
 'Angola': '安哥拉',
 'Albania': '阿尔巴尼亚',
 'United Arab Emirates': '阿联酋',
 'Argentina': '阿根廷',
 'Armenia': '亚美尼亚',
 'French Southern and Antarctic Lands': '法属南半球和南极领地',
 'Australia': '澳大利亚',
 'Austria': '奥地利',
 'Azerbaijan': '阿塞拜疆',
 'Burundi': '布隆迪',
 'Belgium': '比利时',
 'Benin': '贝宁',
 'Burkina Faso': '布基纳法索',
 'Bangladesh': '孟加拉国',
 'Bulgaria': '保加利亚',
 'The Bahamas': '巴哈马',
 'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
 'Belarus': '白俄罗斯',
 'Belize': '伯利兹',
 'Bermuda': '百慕大',
 'Bolivia': '玻利维亚',
 'Brazil': '巴西',
 'Brunei': '文莱',
 'Bhutan': '不丹',
 'Botswana': '博茨瓦纳',
 'Central African Rep.': '中非',
 'Canada': '加拿大',
 'Switzerland': '瑞士',
 'Chile': '智利',
 'China': '中国',
 'Ivory Coast': '象牙海岸',
 'Cameroon': '喀麦隆',
 'Dem. Rep. Congo': '刚果民主共和国',
 'Congo': '刚果',
 'Colombia': '哥伦比亚',
 'Costa Rica': '哥斯达黎加',
 'Cuba': '古巴',
 'N. Cyprus': '北塞浦路斯',
 'Cyprus': '塞浦路斯',
 'Czech Rep.': '捷克',
 'Germany': '德国',
 'Djibouti': '吉布提',
 'Denmark': '丹麦',
 'Algeria': '阿尔及利亚',
 'Ecuador': '厄瓜多尔',
 'Egypt': '埃及',
 'Eritrea': '厄立特里亚',
 'Spain': '西班牙',
 'Estonia': '爱沙尼亚',
 'Ethiopia': '埃塞俄比亚',
 'Finland': '芬兰',
 'Fiji': '斐',
 'Falkland Islands': '福克兰群岛',
 'France': '法国',
 'Gabon': '加蓬',
 'United Kingdom': '英国',
 'Georgia': '格鲁吉亚',
 'Ghana': '加纳',
 'Guinea': '几内亚',
 'Gambia': '冈比亚',
 'Guinea Bissau': '几内亚比绍',
 'Eq. Guinea': '赤道几内亚',
 'Greece': '希腊',
 'Greenland': '格陵兰',
 'Guatemala': '危地马拉',
 'French Guiana': '法属圭亚那',
 'Guyana': '圭亚那',
 'Honduras': '洪都拉斯',
 'Croatia': '克罗地亚',
 'Haiti': '海地',
 'Hungary': '匈牙利',
 'Indonesia': '印度尼西亚',
 'India': '印度',
 'Ireland': '爱尔兰',
 'Iran': '伊朗',
 'Iraq': '伊拉克',
 'Iceland': '冰岛',
 'Israel': '以色列',
 'Italy': '意大利',
 'Jamaica': '牙买加',
 'Jordan': '约旦',
 'Japan': '日本',
 'Kazakhstan': '哈萨克斯坦',
 'Kenya': '肯尼亚',
 'Kyrgyzstan': '吉尔吉斯斯坦',
 'Cambodia': '柬埔寨',
 'Korea': '韩国',
 'Kosovo': '科索沃',
 'Kuwait': '科威特',
 'Lao PDR': '老挝',
 'Lebanon': '黎巴嫩',
 'Liberia': '利比里亚',
 'Libya': '利比亚',
 'Sri Lanka': '斯里兰卡',
 'Lesotho': '莱索托',
 'Lithuania': '立陶宛',
 'Luxembourg': '卢森堡',
 'Latvia': '拉脱维亚',
 'Morocco': '摩洛哥',
 'Moldova': '摩尔多瓦',
 'Madagascar': '马达加斯加',
 'Mexico': '墨西哥',
 'Macedonia': '马其顿',
 'Mali': '马里',
 'Myanmar': '缅甸',
 'Montenegro': '黑山',
 'Mongolia': '蒙古',
 'Mozambique': '莫桑比克',
 'Mauritania': '毛里塔尼亚',
 'Malawi': '马拉维',
 'Malaysia': '马来西亚',
 'Namibia': '纳米比亚',
 'New Caledonia': '新喀里多尼亚',
 'Niger': '尼日尔',
 'Nigeria': '尼日利亚',
 'Nicaragua': '尼加拉瓜',
 'Netherlands': '荷兰',
 'Norway': '挪威',
 'Nepal': '尼泊尔',
 'New Zealand': '新西兰',
 'Oman': '阿曼',
 'Pakistan': '巴基斯坦',
 'Panama': '巴拿马',
 'Peru': '秘鲁',
 'Philippines': '菲律宾',
 'Papua New Guinea': '巴布亚新几内亚',
 'Poland': '波兰',
 'Puerto Rico': '波多黎各',
 'Dem. Rep. Korea': '朝鲜',
 'Portugal': '葡萄牙',
 'Paraguay': '巴拉圭',
 'Qatar': '卡塔尔',
 'Romania': '罗马尼亚',
 'Russia': '俄罗斯',
 'Rwanda': '卢旺达',
 'W. Sahara': '西撒哈拉',
 'Saudi Arabia': '沙特阿拉伯',
 'Sudan': '苏丹',
 'S. Sudan': '南苏丹',
 'Senegal': '塞内加尔',
 'Solomon Is.': '所罗门群岛',
 'Sierra Leone': '塞拉利昂',
 'El Salvador': '萨尔瓦多',
 'Somaliland': '索马里兰',
 'Somalia': '索马里',
 'Serbia': '塞尔维亚',
 'Suriname': '苏里南',
 'Slovakia': '斯洛伐克',
 'Slovenia': '斯洛文尼亚',
 'Sweden': '瑞典',
 'Swaziland': '斯威士兰',
 'Syria': '叙利亚',
 'Chad': '乍得',
 'Togo': '多哥',
 'Thailand': '泰国',
 'Tajikistan': '塔吉克斯坦',
 'Turkmenistan': '土库曼斯坦',
 'East Timor': '东帝汶',
 'Trinidad and Tobago': '特里尼达和多巴哥',
 'Tunisia': '突尼斯',
 'Turkey': '土耳其',
 'Tanzania': '坦桑尼亚',
 'Uganda': '乌干达',
 'Ukraine': '乌克兰',
 'Uruguay': '乌拉圭',
 'United States': '美国',
 'Uzbekistan': '乌兹别克斯坦',
 'Venezuela': '委内瑞拉',
 'Vietnam': '越南',
 'Vanuatu': '瓦努阿图',
 'West Bank': '西岸',
 'Yemen': '也门',
 'South Africa': '南非',
 'Zambia': '赞比亚',
 'Zimbabwe': '津巴布韦',
 'Comoros': '科摩罗'}
# 储存为country.json 文件
with open("country.json","w") as f:
     json.dump(name_map,f)

def get_html(Url, header):
    try:
        r = requests.get(url=Url, headers=header)
        r.encoding = r.apparent_encoding
        status = r.status_code
        # 将原始数据类型转换为json类型，方便处理
        data_json = json.loads(r.text)
        print(status)
        return data_json
    except:
        print("爬取失败")


# 将提取34个省数据的方法封装为函数
def get_data(data, info_list):
    # 直接提取["id","name","lastUpdateTime"] 的数据
    info = pd.DataFrame(data)[info_list]

    # 获取today的数据
    today_data = pd.DataFrame([province["today"] for province in data])
    # 修改列名
    today_data.columns = ["today_" + i for i in today_data.columns]

    # 获取total的数据
    total_data = pd.DataFrame([province["total"] for province in data])
    # 修改列名
    total_data.columns = ["total_" + i for i in total_data.columns]

    return pd.concat([info, today_data, total_data], axis=1)


def save_data(data, name):
    """定义保存数据的函数"""
    # 保存的文件名名称
    file_name = name + ".csv"

    data.to_csv(file_name, index=None, encoding="utf_8_sig")

    # 检查是否保存成功，并打印提示文本
    if os.path.exists(file_name):
        print(file_name + " 保存成功")
    else:
        print('保存失败')


if __name__ == "__main__":
    # 访问网易实时疫情播报平台网址
    url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"

    # 设置请求头，伪装为浏览器
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }

    """爬取中国各省的疫情数据"""
    # 1.获取数据（此时的数据未经处理）
    datas = get_html(url, headers)

    # 2.找到储存中国34省的数据所在
    data_province = datas["data"]["areaTree"][2]["children"]

    # 3.提取34个省数据
    all_data = get_data(data_province, ["id", "name", "lastUpdateTime"])

    """爬取世界各国的疫情数据"""
    world_data = datas["data"]["areaTree"]
    worlds_data = get_data(world_data, ["id", "name", "lastUpdateTime"])
    save_data(worlds_data, "today_worlds")

    # 4.持久化保存数据
    save_data(all_data, "today_province")
    shutil.copyfile('/root/today_worlds.csv', '/var/www/html/today_worlds.csv')
    shutil.copyfile('/root/today_province.csv', '/var/www/html/today_province.csv')
    shutil.copyfile('/root/country.json', '/var/www/html/country.json')
    
    #读取国内疫情数据
    data = pd.read_csv("/var/www/html/today_province.csv")
data.head()
# 填充空值
data = data.fillna(0)
#查看填充后数据的最后五行
data.tail()
#将提取的数据进行排序
total_data = data[["name","total_confirm"]].sort_values(by="total_confirm",ascending=False)
total_data[:5]
map = (
    Map()
    .add("省份", [list(z) for z in zip(total_data["name"],total_data["total_confirm"])], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="中国各省新冠确诊人数数据可视化"),
        legend_opts=opts.LegendOpts(is_show=False),
        visualmap_opts=opts.VisualMapOpts(
            type_="color",
            min_=np.min(total_data["total_confirm"].tolist()),
            max_=np.max(total_data["total_confirm"].tolist()),
            range_text=["High","Low"],is_piecewise=True,
#             split_number = 5,
            pieces=[{"min": 0, "max": 100, "label": "< 100"},{"min": 100, "max": 500, "label": "100 - 500"},
                    {"min": 500, "max": 1000, "label": "500 - 1000"},{"min": 1000, "max": 10000, "label": "1000 - 10000"},
                    {"min": 10000, "max": 20000, "label": "10000 - 20000"},{"min": 20000, "label": "> 20000"}]),
    )
)
map.render("cn_map.html")

df = pd.read_csv("/var/www/html/today_worlds.csv")
df = df.fillna(0)
#提取出我们需要的特征列
world_data = df[["name","lastUpdateTime","today_confirm","total_confirm","total_heal","total_dead"]]
world_data.head()
#将其取出后储存为 name_map
with open("/var/www/html/country.json",'r') as f:
    name_map = json.load(f)
type(data)

world_map=(
Map()
.add("累计新冠确诊",
[list(z)for z in zip(world_data["name"].tolist(),world_data["total_confirm"].tolist())],
"world",is_map_symbol_show=False,name_map=name_map)
.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
.set_global_opts(
title_opts=opts.TitleOpts(title="世界各国新冠确诊累计分布图"),
visualmap_opts=opts.VisualMapOpts(
type_="color",
min_=np.min(world_data["total_confirm"]),
max_=np.max(world_data["total_confirm"]),
range_text=["High","Low"],is_piecewise=True,
pieces=[{"min":0,"max":100,"label":"<100"},
{"min":100,"max":1000,"label":"100-1000"},
{"min":1000,"max":10000,"label":"1000-10000"},
{"min":10000,"max":30000,"label":"1万-3万"},
{"min":30000,"max":100000,"label":"3万 - 10万"},
{"min":100000,"max":200000,"label":"10万 - 20万"},
{"min":200000,"max":500000,"label":"20万 - 50万"},
{"min":500000,"max":1000000,"label":"50万 - 100万"},
{"min":1000000,"max":5000000,"label":"100万 - 500万"},
{"min":5000000,"max":20000000,"label":"500万 - 2000万"},
{"min":20000000,"label":">2000万"}]),
)
)
world_map.render("world_map.html")

#对数据进行排序
total_worlds = world_data[["name","total_confirm"]].sort_values(by="total_confirm",ascending=False)

bar = (
    Bar()
    .add_xaxis(total_worlds["name"].tolist())
    .add_yaxis("累计确诊", total_worlds["total_confirm"].tolist())
    .set_global_opts(
        #图形标题的设置
        title_opts=opts.TitleOpts(
            title="世界各国累计新冠肺炎确诊病例",
            pos_left="center",
            pos_top="7%"),
         # 'shadow'：阴影指示器
        tooltip_opts=opts.TooltipOpts(
            is_show=True, 
            trigger="axis", 
            axis_pointer_type="shadow"),
        # 图例的设置
        legend_opts=opts.LegendOpts(pos_top="12%",pos_left="45%"),
        # 视觉映射配置项
        visualmap_opts=opts.VisualMapOpts(
            type_="color",
            min_=np.min(total_data["total_confirm"]),
            max_=np.max(total_data["total_confirm"]),
            range_text=["High","Low"],),
        # x轴坐标配置项
        xaxis_opts=opts.AxisOpts(name="国家",axislabel_opts={"interval":"0"}),
        # y轴配置项
        yaxis_opts=opts.AxisOpts(
            name="总计",min_=0,
            type_="value",axislabel_opts=opts.LabelOpts(formatter="{value} 人"),),
        # 区域缩放配置项
        datazoom_opts=opts.DataZoomOpts(range_start=0,range_end=5),
    )
)
bar.render("world_bar.html")

bar = (
    Bar()
    .add_xaxis(total_data["name"].tolist())
    .add_yaxis("累计确诊", total_data["total_confirm"].tolist())
    .set_global_opts(
        #图形标题的设置
        title_opts=opts.TitleOpts(
            title="中国累计新冠肺炎确诊病例",
            pos_left="center",
            pos_top="7%"),
         # 'shadow'：阴影指示器
        tooltip_opts=opts.TooltipOpts(
            is_show=True, 
            trigger="axis", 
            axis_pointer_type="shadow"),
        # 图例的设置
        legend_opts=opts.LegendOpts(pos_top="12%",pos_left="45%"),
        # 视觉映射配置项
        visualmap_opts=opts.VisualMapOpts(
            type_="color",
            min_=np.min(total_data["total_confirm"]),
            max_=np.max(total_data["total_confirm"]),
            range_text=["High","Low"],),
        # x轴坐标配置项
        xaxis_opts=opts.AxisOpts(name="省份",axislabel_opts={"interval":"0"}),
        # y轴配置项
        yaxis_opts=opts.AxisOpts(
            name="总计",min_=0,
            type_="value",axislabel_opts=opts.LabelOpts(formatter="{value} 人"),),
        # 区域缩放配置项
        datazoom_opts=opts.DataZoomOpts(range_start=5,range_end=50),
    )
)
bar.render("cn_bar.html")

#复制文件
shutil.copyfile('/root/world_bar.html', '/var/www/html/world_bar.html')
shutil.copyfile('/root/cn_bar.html', '/var/www/html/cn_bar.html')
shutil.copyfile('/root/world_map.html', '/var/www/html/world_map.html')
shutil.copyfile('/root/cn_map.html', '/var/www/html/cn_map.html')

