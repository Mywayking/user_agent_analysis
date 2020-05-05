# -*- coding: utf-8 -*-#
"""
@author:Galen
@file: clean_youku.py
@time: 2019/12/20
@description:

剔除
\xE6\x99\xBA\xE8\x83\xBD\xE9\xA9\xBC,ZHINENGTUO,ZHINENGTUO,2364
\xE5\x8E\x98\xE7\xB1\xB3,CM CM5S,CM CM5S,2400
unknown,unknown,UNKNOWN,2029
"""
import re
from urllib.parse import unquote

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', '-d', type=str, default='../resources/20191220/mobile_youku_2019.log')
parser.add_argument('--save_path', '-s', type=str, default='../resources/20191220/mobile_youku_20191220.log')
args = parser.parse_args()
data_path = args.data_path
save_path = args.save_path


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


def del_specil_character(character):
    """
    unquote，解码 % 号问题
    :param character:
    :return:
    """
    if "%" not in character:
        return character
    return unquote(character)


def clean_space(content):
    """多个空格转一个"""
    return re.sub(' +', ' ', content)


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def clean_youku():
    data_list = []
    for line in read_data(data_path):
        line = del_specil_character(line)
        if "\\x" in line:
            continue
        # OPPO R9s Plus,1607-A01,1607-A01,26
        lines = line.split(',')
        if len(lines) != 4:
            continue
        if int(lines[3]) < 2000:
            continue
        lines_null = [i for i in lines[0:3] if len(i) <= 1]
        if len(lines_null) >= 1:
            print(lines)
            continue
        if is_contain_chinese(line):
            print(lines)
            continue
        if lines[0].lower() == "honor":
            lines[0] = "Huawei"
        # print(lines)         if Huawei
        # Iview^Suprapad^3^9300-M9|9300|9300+|930A|S7-721U|S7-PRO|107
        data_list.append("{0}^{1}^2^{2}".format(clean_space(lines[0]), clean_space(lines[1]), lines[2]))
    save_txt(save_path, data_list, 'w')


clean_youku()
