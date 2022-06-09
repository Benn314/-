'''
本文件基于data_get文件做更精细化的提取
'''

import json
import map_draw
import data_get
import namemap

with open('data_in.json', 'r') as file_in:
    data_in = file_in.read()
    data_in = json.loads(data_in)

with open('data_out.json', 'r') as file_out:
    data_out = file_out.read()
    data_out = json.loads(data_out)

# print(type(data))  # <class 'list'> 是一个列表
# print(data)   # 而我们要在这些数据当中做更精细的提取

map = map_draw.Draw_map()  # 实例化一个类
datas = data_get.Get_data()  # 实例化一个类
datas.get_data()
update_time = datas.get_time()
datas.parse_data_in()
datas.parse_data_out()

# 接下来我们需要将地区和数据一一对应
# 中国疫情地图
def china_map():
    # 从print的结果看，一个列表即一个省份
    area = []
    confirmed = []
    for each in data_in:
        print(each)
        print('*' * 50 + '\n')  # 这里只是起到区分目的
        area.append(each['area'])
        confirmed.append(each['confirmed'])
        # print(area)
        # print(confirmed)
    map.to_map_china(area, confirmed, update_time)  # 参数area, variate,update_time,这里的地图只生成一个，所以无所谓是否缩进到for里面


# 23个省、5个自治区、4个直辖市、2个特别行政区 香港、澳门和台湾的subList为空列表，未有详情数据

# 省、直辖市疫情地图
def province_map():
    # for each in data_in:
    #     city = []
    #     confirmeds = []  # 为了上面省份的confirmed做区分，所以结尾加了s
    #     province = each['area']  # 地区所在的省份
    #     for each_city in each['subList']:
    #         city.append(each_city['city'])
    #         confirmeds.append(each_city['confirmed'])
    #     # print(city)
    #     # print(confirmeds)

    for each in data_in:
        city = []
        confirmeds = []
        province = each['area']
        for each_city in each['subList']:
            city.append(each_city['city']+"市")
            confirmeds.append(each_city['confirmed'])
            map.to_map_city(city,confirmeds,province,update_time)
        if province == '上海' or '北京' or '天津' or '重庆':
            for each_city in each['subList']:
                city.append(each_city['city'])
                confirmeds.append(each_city['confirmed'])
                map.to_map_city(city,confirmeds,province,update_time)

# pyecharts 世界地图国家中英文对照
def read_country_code():
    """
    获取国家中英文字典
    :return:
    """
    country_dict = {}
    for key, val in namemap.nameMap.items():  # 将 nameMap 列表里面键值互换
        country_dict[val] = key
    return country_dict

country_dict = read_country_code()


# 因为爬取的世界疫情地图信息并不包括中国（无数据），中国的数据被单独拿出来放到了国内疫情模块当中，所以自己写了一个函数封装中国疫情累计确诊人数，并贴到了世界疫情地图上
# 可以直观的进行国内外疫情的分析
def China_confirmed_In_World():

    China_sum_confirmed = 0 # 要指明China_sum_confirmed变量的类型，所以要先初始化，不然会报错
    for each in data_in:
        China_sum_confirmed = China_sum_confirmed + int(each['confirmed'])

    # print('\n')
    # print(China_sum_confirmed)

    return China_sum_confirmed



# 世界疫情地图
def world_map():
    country = ['中国']
    # 获取中国的累计确诊人数，在世界地图上面显现
    China_confirmed_Count = str(China_confirmed_In_World())
    confirmed = [China_confirmed_Count]

    # print(China_confirmed_Count)
    # print(type(China_confirmed_Count))
    # print('\n')

    for each in data_out:   # ['globalList']
        # country = ['中国']
        # confirmed = ['1314']  #第87行和88行的代码不能放在90、91行代码这，因为不然country和confirmed会一直会初始化，导致最后生成地图只有部分数据的情况

        for each_country in each['subList']:
            # if each_country['country'] in country_dict.keys():
            country.append(each_country['country'])
            confirmed.append(each_country['confirmed'])
            map.to_map_world(country, confirmed, update_time)  # 参数area, variate,update_time,这里的地图只生成一个，所以无所谓是否缩进到for里面
            # country.append(country_dict[each_country['country']])
            # confirmed.append(each_country['confirmed'])

        # print(country)
        # print(confirmed)





# china_map()
# province_map()  # 获取到空列表的原因：例如香港台湾在网站上面并没有非常详细的，每一个地区的数据，因此这里我们不将它包含在内，在绘制地图的时候我们也不用管他

# 到这里我们就已经在数据进行精细化并一一对应，下一步我们就来绘制地图，再建python文件（map_draw.py）

china_map()
province_map()
world_map()
# China_confirmed_In_World()

