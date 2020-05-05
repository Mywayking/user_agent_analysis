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
            # print(data)
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


class UaCombineDetailsOld:
    def __init__(self, date_str='20191220', data_new='mobile_youku_20191220.log'):
        self.date_str = date_str
        self.data_new = data_new
        self.rtb_ua = {}
        self.atlas = {}
        self.brand_old = {}
        self.model_old = {}
        self.dataset_update_list = []

    def load_old(self, path):
        # Zte^yuanhang 4^2^ZTE BA610C|ZTE BA610T|ZTE BLADE A610C
        for line in read_data(path):
            lines = line.split("^")
            brand = clean_space(lines[0]).lower()
            model = clean_space(lines[1]).lower()
            if not (brand in self.brand_old):
                self.brand_old[brand] = lines[0]
            if not (model in self.model_old):
                self.model_old[model] = lines[1]

    def combine(self):
        data_dir = '../resources/{0}/'.format(self.date_str)
        path_save = '../resources/{0}/{1}'.format(self.date_str, 'ua2device_precise_new.txt')
        self.load_old(data_dir + 'ua2device_precise.txt')
        self.load_old(data_dir + 'ua2device_pattern.txt')
        dataset = []
        dataset_update_list = []
        for line in read_data(data_dir + '{0}'.format(self.data_new)):
            lines = line.split("^")
            brand = clean_space(lines[0]).lower()
            model = clean_space(lines[1]).lower()
            if brand in self.brand_old:
                dataset_update_list.append("brand:" + lines[0] + "<=" + self.brand_old[brand])
                lines[0] = self.brand_old[brand]
            if model in self.model_old:
                dataset_update_list.append("model:" + lines[1] + "<=" + self.model_old[model])
                lines[1] = self.model_old[model]
            else:
                if model.startswith(brand):
                    model = model.replace(brand, "").strip()
                    if len(model) == 0:
                        break
                    if model in self.model_old:
                        # print("model:" + lines[1] + "<=" + self.model_old[model])
                        dataset_update_list.append("model:" + lines[1] + "<=" + self.model_old[model])
                        lines[1] = self.model_old[model]
                        # for k, v in self.model_old.items():
                        #     if model.endswith(k):
                        #         dataset_update_list.append(lines[1] + "<=" + self.model_old[k])
                        #         print(lines[1] + "<=" + self.model_old[k])
                        #         lines[1] = self.model_old[k]
                        #         break
            dataset.append("^".join(lines))
        save_txt(path_save, dataset, 'w')
        save_txt('{0}.log'.format(self.date_str), dataset_update_list, 'a')
        unique_file(path_save)


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


def combine(date_str):
    data_dir = '../resources/{0}/'.format(date_str)
    path_new = "{0}{1}".format(data_dir, 'ua2device_precise_new.txt')
    path_old = "{0}{1}".format(data_dir, 'ua2device_precise.txt')
    path_save = "{0}{1}".format(data_dir, 'ua2device_precise_new.txt'.replace('new', date_str))
    add_save = "{0}{1}".format(data_dir, 'ua2device_precise_add.txt')
    print(path_old, path_new, path_save)
    data_result = []
    add_list = []
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
        print(data_list)
        add_list.append('^'.join(data_list))
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
    with open(path_save, 'w')as f:
        for k, v in result_dict.items():
            line = '{0}^{1}\n'.format(k, '|'.join(list(v)))
            f.write(line)
    unique_file(path_save)
    save_txt(add_save, add_list)
    unique_file(add_save)


if __name__ == "__main__":
    """
    python combine.py -n ../resources/20191220/mobile_youku_20191220.log -o ../resources/20191220/ua2device_precise.txt
    """
    # 整理成rtb数据类
    # cu = UaCombineDetailsOld(date_str="20191220", data_new='mobile_youku_20191220.log')
    # cu.combine()
    # 合并文件
    combine("20191220")
