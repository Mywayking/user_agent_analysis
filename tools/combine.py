# -*- coding: utf-8 -*-#
"""
@author:Galen
@file: combine.py
@time: 2019/01/16
@description:
新旧文件结合
"""
import os
import re

from collections import defaultdict
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('--path_new', '-n', type=str,
                   default='/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20190115/need_result.txt')
parse.add_argument('--path_old', '-o', type=str,
                   default='/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20190115/ua2device_precise.txt')
args = parse.parse_args()


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


def unique_file(path):
    file_dir_list = path.split("/")
    del file_dir_list[-1]
    file_dir_list.append("tmp_file.txt")
    tmp_path = "/".join(file_dir_list)
    # command = "cat {0}|awk '!a[$0]++'>{1}".format(path, tmp_path)
    command = "cat {0}|sort -u|uniq >{1}".format(path, tmp_path)
    os.system(command)
    os.remove(path)
    os.rename(tmp_path, path)
    print("Duplicate removal ！")


def clean_space(content):
    """多个空格转一个"""
    return re.sub(' +', ' ', content)


def _load_file(data_path):
    """
    1. key brand以旧为主，新靠拢旧
    # Zte^yuanhang 4^2^ZTE BA610C|ZTE BA610T|ZTE BLADE A610
    :param data_path:
    :return:
    """
    key_dict = {}
    model_dict = {}
    for line in read_data(data_path):
        lines = line.split("^")
        # brand = clean_space(lines[0]).lower()
        # if lines[0] == "1":
        #     print(line, data_path)
        model = clean_space(lines[1]).lower()
        model_dict[model] = lines[1]
        key_list = lines[3].split('|')
        for key in key_list:
            key = clean_space(key).lower()
            key_dict[key] = lines
    return model_dict, key_dict


def combine(path_new, path_old):
    data_result = []
    old_model_dict, old_key_dict = _load_file(path_old)
    new_model_dict, new_key_dict = _load_file(path_new)
    key_all = set(new_key_dict.keys()) | set(old_key_dict.keys())
    for key in key_all:
        data_list = old_key_dict.get(key, None)
        if data_list is not None:
            data_result.append(data_list)
            continue
        data_list = new_key_dict.get(key, None)
        # print(key)
        if data_list is None:
            raise ValueError("error data")
        clean_model = clean_space(data_list[1]).lower()
        if clean_model not in old_model_dict.keys():
            data_result.append(data_list)
            continue
        model = old_model_dict[clean_model]
        data_list[1] = model
        data_result.append(data_list)
    result_dict = defaultdict(set)
    for line in data_result:
        result_key = '^'.join(line[0:3])
        result_dict[result_key].add(line[3].upper())
    with open('result.txt', 'w')as f:
        for k, v in result_dict.items():
            line = '{0}^{1}\n'.format(k, '|'.join(list(v)))
            f.write(line)
    unique_file("result.txt")


if __name__ == "__main__":
    """
    python combine.py -n ../resources/20191220/mobile_youku_20191220.log -o ../resources/20191220/ua2device_precise.txt
    """
    new = args.path_new
    old = args.path_old
    combine(new, old)
