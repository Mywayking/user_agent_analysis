"""
-------------------------------------------------
   Author :       galen
   date：          2018/4/19
-------------------------------------------------
   Description:
   抓取：https://source.android.com/setup/start/build-numbers
-------------------------------------------------
"""
from build_analysis.setting import *
from build_analysis.utils import *

import random
import requests
from lxml import etree


def request_url(url):
    """
    网页抓取数据
    """
    UserAgent = random.choice(USER_AGENT)
    headers = {
        'User-Agent': UserAgent,
    }
    html = ""
    try:
        r = requests.get(url, headers=headers, timeout=20)
        # 解决乱码问题
        r.encoding = r.apparent_encoding
        html = r.text
    except Exception as e:
        print(e)
    return html


def extract_table_data(table):
    data_list = []
    thead = table.xpath("thead//th/text()")
    thead = list(map(lambda x: x.strip().strip("\n"), thead))
    data_list.append("^".join(thead))
    tbody = table.xpath("tbody//tr")
    for th in tbody:
        th_text = th.xpath("td//text()")
        # print(th_text)
        th_text = list(map(lambda x: x.strip().strip("\n"), th_text))
        data_list.append("^".join(th_text))
    return data_list


def craw_build(url="https://source.android.com/setup/start/build-numbers"):
    html = request_url(url)
    if html == "":
        print("no data get", url)
        return
    selector = etree.HTML(html)
    tables = selector.xpath('//table')
    tables_data_0 = extract_table_data(tables[0])
    tables_data_1 = extract_table_data(tables[1])
    tables_data_2 = extract_table_data(tables[2])
    tables_data_0 = [x for x in tables_data_0 if len(x) != 0]
    tables_data_1 = [x for x in tables_data_1 if len(x) != 0]
    tables_data_2 = [x for x in tables_data_2 if len(x) != 0]
    build_list = list(map(lambda x: x.split("^")[0], tables_data_1)) + list(
        map(lambda x: x.split("^")[0], tables_data_2))
    build_list = [x for x in build_list if x != "Build" and len(x) != 0]
    save_to_datas_file(build_list, ANDROID_BUILD, "w")
    save_to_datas_file(tables_data_0, ANDROID_PLATFORM, "w")
    save_to_datas_file(tables_data_1, ANDROID_BUILD_TAGS, "w")
    save_to_datas_file(tables_data_2, ANDROID_HONEYCOMB_BUILDS, "w")


if __name__ == '__main__':
    craw_build()
