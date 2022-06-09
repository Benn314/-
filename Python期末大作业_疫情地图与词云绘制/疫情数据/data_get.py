import requests
from lxml import html
import re
import json
import namemap

etree = html.etree



class Get_data():

    # 获取数据
    def get_data(self):
        response = requests.get('https://voice.baidu.com/act/newpneumonia/newpneumonia')
        with open('html.txt', 'w') as file:
            file.write(response.text)
            # print(response.text)

    '如果爬取不了数据可以用伪装头请求'
    # 目标url
    # url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"
    #
    # 伪装请求头
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/80.0.3987.149 Safari/537.36 '
    # }
    #
    # # 发出get请求
    # response = requests.get(url, headers=headers)

    # 提取更新时间
    def get_time(self):
        with open('html.txt', 'r') as file:
            text = file.read()
        time = re.findall('"mapLastUpdatedTime":"(.*?)"', text)[0]
        # print(time)
        return time

    # 解析数据
    def parse_data_in(self):

        '''
        result代表国内的数据
        result1代表海外的数据
        '''

        with open('html.txt', 'r') as file:
            text = file.read()
        html = etree.HTML(text)

        result = html.xpath('//script[@type="application/json"]/text()')
        # print(result)   # 返回一个列表，分析可得列表只有一项，因此我们要将列表转换成字符串类型
        result = result[0]  # 但我们这里得到的还是一个字符串，我们不能用字典的方式来提取内容，因此要将字符串转换成字典，这里用到json模块
        result = json.loads(result)  # json.loads() 这个方法可以将字符串转换为python数据类型，也就是字典

        # print(type(result1))
        # print(type(result))  # <class 'dict'>
        # print(result)
        # print(result['component'][0]['caseList'])   # 这样我们就得到了中国各个省份各个市的信息汇总，下面我们将数据写入文本文件
        # 而我们现在的打印内容并非字符串，需要将其转换为字符串才能写入文本文件

        result = result['component'][0]['caseList']
        result = json.dumps(result)  # json.dumps()这个方法可以将python数据类型转换成字符串

        with open('data_in.json', 'w') as file_in:
            file_in.write(result)
            print('国内数据已写入data_in.json文件...')  # 友好提示

    # 解析数据
    def parse_data_out(self):
        '''
        result代表国内的数据
        result1代表海外的数据
        '''

        with open('html.txt', 'r') as file:
            text = file.read()
        html = etree.HTML(text)

        result1 = html.xpath('//script[@type="application/json"]/text()')
        # print(result1)   # 返回一个列表，分析可得列表只有一项，因此我们要将列表转换成字符串类型
        result1 = result1[0]  # 但我们这里得到的还是一个字符串，我们不能用字典的方式来提取内容，因此要将字符串转换成字典，这里用到json模块
        result1 = json.loads(result1)   # json.loads() 这个方法可以将字符串转换为python数据类型，也就是字典

        # print(type(result))  # <class 'dict'>
        result1 = result1['component'][0]['globalList'] # 这样我们就得到了世界各个国家的疫情信息汇总，下面我们将数据写入文本文件
        # 而我们现在的打印内容并非字符串，需要将其转换为字符串才能写入文本文件
        result1 = json.dumps(result1)  # json.dumps()这个方法可以将python数据类型转换成字符串

        with open('data_out.json', 'w') as file_out:
            file_out.write(result1)
            print('海外数据已写入data_out.json文件...')  # 友好提示

# 在这里执行一次就ok，后面都在data_more.py,data_more.py相当于main.py
# data = Get_data()
# data.get_data()
# data.get_time()
# data.parse_data_in()
# data.parse_data_out()

# 下一步我们要将数据做进一步的精细分工作，新建data_more.py
