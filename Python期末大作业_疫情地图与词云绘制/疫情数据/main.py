# 绘制词云
import get_data

get_data.wordcloud_data()

import word_cloud

word_cloud.generate_pic(word_cloud.frequency_in, '国内疫情词云图')
word_cloud.generate_pic(word_cloud.frequency_out, '国外疫情词云图')


# 绘制地图
import get_data
from 疫情数据.data_get import Get_data

data = Get_data()
data.get_data()
data.get_time()
data.parse_data_in()
data.parse_data_out()

import data_more

data_more.china_map()
data_more.province_map()
data_more.world_map()