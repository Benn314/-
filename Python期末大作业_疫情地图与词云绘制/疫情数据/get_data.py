import requests
# from lxml import etree    低版本才能这么导包
import lxml
import json
import openpyxl
from lxml import html

etree = html.etree

def wordcloud_data():
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
    response = requests.get(url)
    # print(response.text)

    # 生成html对象
    html = etree.HTML(response.text)
    result = html.xpath('//script[@type="application/json"]/text()')  # xpath()
    # print(type(result)) #打印结果：<class 'list'> , 是一个列表，查看它当中的内容可以查看列表的第一项
    result = result[0]  # 获取列表的第一项，也就是全部的内容
    # print(result[0]['component'])   #这里报错：形式上的字典，实际是一个字符串类型，要把它变成字典才能提取内容，这里要用到json模块当中的一个方法

    # json.loads()方法可以将一个字符串类型转变为python数据类型（字典）
    result = json.loads(result)
    # print(type(result)) #打印结果：<class 'dict'>
    print(result)   # 国内外疫情信息

    # 首先创建工作簿
    wb = openpyxl.Workbook()
    # 创建工作表,每一个工作表代表一个area
    ws = wb.active  # 创建的工作簿给到工作表
    ws.title = "国内疫情"
    ws.append(['省份', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量'])  # 第一行要写入数据的含义
    # 获取字典中的值，直接访问它的键就可以得到值
    # print(result['component'][0]['caseList'])   #所得到的值是各个省下各个市的数据，将该值继续赋值给result
    # 可以在这里做一个区分，用result_in代表国内的情况，result_out代表国外的情况
    result_in = result['component'][0]['caseList']
    result_out = result['component'][0]['globalList']
    # print(result_out)  # 运行可以看到结果，列表只有一项，也就是result_out[0]就可以看到全部内容
    for each in result_in:
        # print(each)
        # print('*' * 50 + '\n')  # 便于观察
        temp_list = [each['area'], each['confirmed'], each['died'], each['crued'], each['curConfirm'],
                     each['confirmedRelative'],
                     each['diedRelative'], each['curedRelative'], each['curConfirmRelative']]  # 为了好看一点，我们用一个变量来装列表
        # 因为up的视频是2020的，那时候没有确诊，也就是数值为0的话，是NULL值，需要填充，现在不需要了,所以把嵌套的for语句注释了
        # for i in range(temp_list):
        #     if temp_list[i] == '':
        #         temp_list[i] = '0'  #而这里如果单纯是0（int）的话，它是右对齐的，因为爬取的数据是字符串类型，所以要改成’0‘
        ws.append(temp_list)

    for each in result_out:
        print(each)
        print('*' * 50 + '\n')  # 便于观察
        # 我们可以将不同的项写入不同的表中
        sheet_title = each['area']  # 用字典获取值的方法来获取亚洲这个字段
        # 创建新的工作表
        ws_out = wb.create_sheet(sheet_title)
        ws_out.append(['国家', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量'])
        for country in each['subList']:
            temp_list = [country['country'], country['confirmed'], country['died'], country['crued'], country['curConfirm'],
                         country['confirmedRelative']]  # 为了好看一点，我们用一个变量来装列表
            # for i in range(temp_list):
            #     if temp_list[i] == '':
            #         temp_list[i] = '0'  #而这里如果单纯是0（int）的话，它是右对齐的，因为爬取的数据是字符串类型，所以要改成’0‘
            ws_out.append(temp_list)  # 先将列表赋值给一个变量再将列表写入excel表格当中，防止列表当中有一些项是空的

    # 这里我们需要将我们的工作簿和工作表保存才能得到我们的excel文件，这里用save()方法
    wb.save('./data.xlsx')

# 完成数据采集工作后，新建 word_cloud.py 来绘制词云

'''
做个小结：
area --> 省份/直辖市/特别行政区
city --> 城市
confirmed --> 累计确诊人数
died --> 死亡人数
crued --> 治愈人数
confirmedRelative --> 累计确诊的增量
cruedRealative --> 治愈的增量
curConfirm --> 现有确诊人数
curConfirmRelative --> 现有确诊的增量
diedRelative --> 死亡的增量  
'''

# 规律----遍历列表的每一项,可以发现,每一项(type:字典)均代表一个省份等区域,这个字典的前11项是该省份的疫情数据,
# 当key = 'subList'时,其结果为只有一项的列表,提取出列表的第一项,得到一系列的字典,字典中包含该城市的疫情数据.
