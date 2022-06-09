from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
import namemap
import os


class Draw_map():
    # relativeTime为发布的时间,传入时间戳字符串
    # def get_time(self):
        # relativeTime = int(relativeTime)
        # return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(relativeTime))

# 创建文件夹
    def __init__(self):
        if not os.path.exists('./map/china'):
            os.makedirs('./map/china')

    def get_color(self, r, g, b):
        result = '#' + ''.join(
            map((lambda x: "%02x" % x), (r, g, b)))  # 这里要用到字符串的join()方法，join()当中应该是一个列表，相当于我们以空字符串将这一个列表来进行拼接，这里采用匿名函数
        return result.upper()  # upper()可以将小写字母全部转换成大写字母

    # 可以只在python控制台运行一小段代码，测试每一个函数方法

    def to_map_city(self, area, variate, province, update_time):

        # faker.py文件里面的guangdong_city列表城市有加“市”，而其他地方没有，要实现相同效果的话，其他地方没有加“市”字的要加上“市”
        # 注意：我国有23个省，5个自治区，4个直辖市，2个特别行政区。由于台湾省和香港行政区和澳门行政区他们的subList为空列表，没有详细的数据，因此这3个地区我们无法画出他的图

        pieces = [
            {"max": 99999999, "min": 10000, "label": "≥10000", "color": self.get_color(102, 2, 8)},
            {"max": 9999, "min": 1000, "label": "1000-9999", "color": self.get_color(140, 13, 13)},
            {"max": 999, "min": 500, "label": "500-999", "color": self.get_color(204, 41, 41)},
            {"max": 499, "min": 100, "label": "100-499", "color": self.get_color(255, 123, 105)},
            {"max": 99, "min": 50, "label": "50-99", "color": self.get_color(255, 170, 133)},
            {"max": 49, "min": 10, "label": "10-49", "color": self.get_color(255, 202, 179)},
            {"max": 9, "min": 1, "label": "1-9", "color": self.get_color(255, 228, 217)},
            {"max": 0, "min": 0, "label": "0", "color": self.get_color(255, 255, 255)},
        ]

        c = (
            # 设置地图大小
            Map(init_opts=opts.InitOpts(width='1350px', height='880px'))
                .add("累计确诊人数", [list(z) for z in zip(area, variate)], province, is_map_symbol_show=False)
                # 设置全局变量  is_piecewise设置数据是否连续，split_number设置为分段数，pices可自定义数据分段
                # is_show设置是否显示图例
                .set_global_opts(
                title_opts=opts.TitleOpts(title="%s地区疫情地图分布" % (province),
                                          subtitle='截止%s  %s省疫情分布情况' % (update_time, province), pos_left="center",
                                          pos_top="10px"),
                legend_opts=opts.LegendOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True,
                                                  pieces=pieces,
                                                  ),
            )
                .render("./map/china/{}疫情地图.html".format(province))
        )

    def to_map_china(self, area, variate, update_time):
        # 通过pieces，我们可以进行分段，可以在浏览器F12（进入开发者工具）审查元素的数据
        # 我们需要将元素的RGB数值转换成十六进制的形式，例如下面的'#8A0808'等，可以在前面重新定义一个函数来进行转换
        pieces = [
            {"max": 99999999, 'min': 10000, 'label': '>10000', 'color': '#8A0808'},
            {"max": 9999, 'min': 1000, 'label': '1000-9999', 'color': '#B40404'},
            {"max": 999, 'min': 100, 'label': '100-999', 'color': '#DF0101'},
            {"max": 99, 'min': 10, 'label': '10-99', 'color': '#F5A9A9'},
            {"max": 9, 'min': 1, 'label': '1-9', 'color': '#F5A9A9'},
            {"max": 0, 'min': 0, 'label': '0', 'color': '#FFFFFF'},
        ]

        c = (
            Map(init_opts=opts.InitOpts(width='1350px', height='880px'))  # 在这里传入参数可以初始化地图的大小
                .add("累计确诊人数", [list(z) for z in zip(area, variate)],  # zip()函数是python的一个内置函数，可以实现将列表当中序列相同的项进行对应
                     "china")  # 将Faker.provinces, Faker.values()替换成area和variate，variate变量的意思，china是地图的类别
                .set_global_opts(  # set_global_opts是设置全局变量，我们可以对它进行个性化的设置
                title_opts=opts.TitleOpts(title="中国疫情地图分布", subtitle='截止%s 中国疫情分布情况' % (update_time),
                                          pos_left='center', pos_top='30px'),  # 更改位置信息
                # Map-VisualMap（分段型）更改为 中国疫情地图分布，我们还可以创建副标题subtitle
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True, pieces=pieces),
            )
                .render("./map/中国疫情地图.html")  # 这里是保存的文件名，我们更改一下
        )

    def to_map_world(self, country, variate, update_time):
        c = (
            Map(init_opts=opts.InitOpts(width='1350px', height='880px'))

                # .add("累计确诊人数", [list(z) for z in zip(country, variate)], "world")

                .add(series_name="海外累计确诊地图", data_pair=[(i, j) for i, j in zip(country, variate)],
                     maptype="world",
                     is_map_symbol_show=False,
                     name_map=namemap.nameMap)  # name_map=namemap.nameMap会把英文转为中文，所以在data_more.py运行时，不需要再去用namemap字典转成英文了，但二者都有相同的问题，就是显示世界疫情地图的国家数据，只能显示部分国家数据，不懂怎么回事

                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="世界疫情地图分布", subtitle='截止%s 世界疫情分布情况' % (update_time),
                                          pos_left='center', pos_top='30px'),
                visualmap_opts=opts.VisualMapOpts(max_=100000000),
            )
                .render("./map/世界疫情地图.html")
        )

# map = Draw_map()
# map.to_map_china()
