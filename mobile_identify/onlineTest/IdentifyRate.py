# coding=utf-8
import re
import os
from collections import OrderedDict
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_data(filepath):
    with open(filepath, 'rU') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            lines = lines.strip('\n')
            if not lines:
                break
            yield lines


def load_dict_precise():
    # 读入数据ua2deviceprecise.txt
    filepath_precise = "ua2device_precise.txt"
    data_dict_precise = {}
    for data in get_data(filepath_precise):
        device = ()
        PRECISE_data = data.split('^')
        # device = (PRECISE_data[0],PRECISE_data[1],PRECISE_data[2])
        if PRECISE_data[3] is not None:
            preciseKeywords = PRECISE_data[3].split('|')
            for kw in preciseKeywords:
                data_dict_precise[kw.upper()] = 0
    return data_dict_precise


def dict_order(dict_data):
    data_dict_order = OrderedDict()
    dict_data = sorted(dict_data.iteritems(), key=lambda asd: asd[1], reverse=True)
    for data in dict_data:
        data_dict_order[data[0]] = data[1]
    return data_dict_order


def detect_many_ua():
    # filepath = "/home/galen/nht_pixel_2017071000.log"
    # filepath ="100.txt"
    filepath = os.path.dirname(os.path.abspath(
        __file__)) + "/admaster.log"
    # filename= raw_input_A = raw_input("filename: ")
    # filepath =os.path.dirname(os.path.dirname(os.path.abspath("identifyUaDevice.py")))+"/"+filename
    print
    filepath
    data_dict_precise = load_dict_precise()
    count = 0
    count_match = 0
    # not_match_ua = []
    for data in get_data(filepath):
        # print data_dict_precise
        count += 1
        # print count
        ua = data.upper()
        if "BUILD" in data or "LINUX" in data or "ANDROID" or "IPHONE" or "IPAD" in ua:
            # print ua
            for prk in data_dict_precise.keys():
                if prk in ua:
                    # print ua
                    data_dict_precise[prk] += 1
                    count_match += 1
                    break
                    # else:
                    # not_match_ua.append(data)
                    # break
        if count % 10000 == 0:
            print
            "占总匹配率：", float(count_match) / float(count)
            print
            "匹配个数{0}；总ua数{1}".format(count_match, count)
            # data_dict_precise= dict_order(data_dict_precise)
            # out_put_data(data_dict_precise)
        if count % 1000000 == 0:
            data_dict_precise = dict_order(data_dict_precise)
            out_put_data(data_dict_precise)
            # out_put_datass(not_match_ua)
            # not_match_ua = []
    print
    "占总匹配率：", float(count_match) / float(count)
    print
    "匹配个数{0}；总ua数{1}".format(count_match, count)
    out_put_data(data_dict_precise)
    return


def out_put_data(data):
    fout = open("ua_device_count_1.0.txt", "w")
    for key, value in data.items():
        if value != 0:
            fout.write("{0}^{1}".format(key, value) + "\n")
    fout.close()
    return


def main():
    detect_many_ua()
    return


if __name__ == '__main__':
    main()
