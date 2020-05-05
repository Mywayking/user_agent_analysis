"""
清洗bidlog日志
"""

import os
import re


def clean_space(content):
    """多个空格转一个"""
    return re.sub(' +', ' ', content)


def read_data(path):
    with open(path, "r") as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            yield line


def save_txt(filename, data_list, model="a"):
    with open(filename, model, encoding='UTF-8', errors='ignore') as f:
        for data in data_list:
            f.write(data + '\n')


def load_data(path):
    with open(path, "r")as f:
        return f.read().splitlines()


def unique_file(path):
    file_dir_list = path.split("/")
    del file_dir_list[-1]
    file_dir_list.append("tmp_file.txt")
    print("file_dir_list", file_dir_list)
    tmp_path = "/".join(file_dir_list)
    # tmp_path = "/".join(file_dir_list) + "/tmp_file.txt"
    print(tmp_path)
    command = "cat {0}|awk '!a[$0]++'>{1}".format(path, tmp_path)
    print(command)
    os.system(command)
    os.remove(tmp_path)


def sort_dict(dict_words, reverse=True):
    """
    字典排序
    :param reverse:
    :param dict_words:
    :return:
    """
    keys = dict_words.keys()
    values = dict_words.values()

    list_one = [(key, val) for key, val in zip(keys, values)]
    list_sort = sorted(list_one, key=lambda x: x[1], reverse=reverse)

    return list_sort


def parse_brand_device_keywords(data_str):
    """
    unknown^Haier_HT-I710=HAIER_HT-I710
    :param data_str:
    :return:
    """
    data_info = {}
    data_list = data_str.split("=")
    # print(data_str)
    brand, device = data_list[0].split("^")
    data_info["brand"] = clean_space(brand.strip())
    data_info["device"] = clean_space(device.strip())
    data_info["keywords_list"] = data_list[1].split("#")
    keywords_str = "#".join(data_info["keywords_list"])
    data_info["save"] = brand + "^" + device + "=" + keywords_str
    return data_info


def filter_brand_device(data_str):
    """
    过滤与整理规则
        剔除空白字符串，多个空白字符串转为一个
        brand含有非数字、字母、中文、,、.以外的字符
        含有\\x字段
        keyword == brand 剔除
        keyword对应多个品牌 剔除
        brand device in ["unknown","APPLE","Android"]
        brand长度小于 1 剔除
        剔除特殊字符串后比较brand 和 device是否有重复
        构建品牌确定清单，在清单内确定放行

    :param data_str:
    :return:
    """
    if "\\x".upper() in data_str.lower():
        return
    data_info = parse_brand_device_keywords(data_str)
    brand_lower = data_info["brand"].lower()
    if 1 >= len(brand_lower):
        return
    if brand_lower in ["unknown", "apple", "android"]:
        return
    return data_info


def clean_bidlog_20180831():
    """

    :return:
    """
    DATA_PATH = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20180831/mobile_bidlog.log"
    keywords_full_set = set()
    data_save = []
    for line in read_data(DATA_PATH):
        # line = b"{0}".format(line).decode("utf-8")
        line = line.encode('utf-8', 'ignore').decode('utf-8')
        try:
            data_info = filter_brand_device(line)
            if data_info is None:
                continue
            # print(set(data_info["keywords_list"]))
            keywords_full_set = keywords_full_set | set(data_info["keywords_list"])
            data_save.append(data_info)
        except Exception as e:
            print(e, line)
    with open("/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20180831/brand_clean.log", "w")as f:
        for data in data_save:
            if data["brand"] in keywords_full_set:
                continue
            f.write(data["save"] + "\n")


def check_brand():
    data_path_bidlog = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20180831/brand_clean.log"
    data_path_ua2precise = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/ua2device_precise.txt"
    tenaa_brand_set = set()
    for ten in read_data(data_path_bidlog):
        tenaa_brand_set.add(ten.split("^")[0].lower())
    testin_brand_set = set()
    for line in read_data(data_path_ua2precise):
        line_list = line.split("^")
        testin_brand_set.add(line_list[0].lower())
    print(len(tenaa_brand_set))
    print(len(testin_brand_set))
    save_txt('commom', list(testin_brand_set & tenaa_brand_set), "w")
    # {'谷歌', 'vivo', 'Apple', 'HTC', '奇酷', '宏基', 'Skyworth', 'IUNI', 'OPPO'}


if __name__ == "__main__":
    # parse_brand_device_keywords("unknown^Haier_HT-I710=HAIER_HT-I710")
    clean_bidlog_20180831()
    # check_brand()
