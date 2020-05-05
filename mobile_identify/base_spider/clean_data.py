"""
Testin清洗入库
"""

import os
import re
from collections import defaultdict

data_path_smartphone_info = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/smartphone_info.txt"
data_path_tenaa = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/tenaa_brand_device"
data_path_testin = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/testin_20180902.txt"
data_path_testin_tenaa_en = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/testin和tenaa中英文对照.txt"


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
    command = "cat {0}|sort -u|uniq >{1}".format(path, tmp_path)
    command_mv = "mv {0} {1}".format(tmp_path, path)
    print(command)
    os.system(command)
    print(command_mv)
    os.system(command_mv)


def get_brand_device_testin():
    """
    获得brand和device
    e.g.
    努比亚 Z11 miniS^品牌：努比亚^型号：NX549J^系统：Android 6.0.1^分辨率：1080*1920
    :return:
    """
    data_path = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/testin_20180902.txt"
    brand_list = []
    device_list = []
    for line in read_data(data_path):
        line_list = line.split("^")
        brand_list.append(line_list[1].replace("品牌：", ""))
        device_list.append(line_list[0])
    print(device_list)
    save_txt('testin_brand', list(set(brand_list)))


def check_in_tenaa():
    data_path_testin = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/testin_20180902.txt"
    data_path_tenaa = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/tenaa_brand_device"
    tenaa_brand_set = set()
    for ten in read_data(data_path_tenaa):
        # 爱宝隆^ABLOnG BL801,2012
        tenaa_brand_set.add(ten.split("^")[0])
    testin_brand_set = set()
    for line in read_data(data_path_testin):
        line_list = line.split("^")
        testin_brand_set.add(line_list[1].replace("品牌：", ""))
    print(testin_brand_set - (testin_brand_set & tenaa_brand_set))
    # {'谷歌', 'vivo', 'Apple', 'HTC', '奇酷', '宏基', 'Skyworth', 'IUNI', 'OPPO'}


def tenaa_kimovil_common_brand():
    tenaa_keyword_brand = {}
    tenaa_keyword_brand_set = set()
    for ten in read_data(data_path_tenaa):
        # 爱宝隆^ABLOnG BL801,2012
        ten_ = ten.split("^")
        tenaa_keyword_brand[ten_[1].split(",")[0]] = ten_[0]
        tenaa_keyword_brand_set.add(ten_[1].split(",")[0])
    smartphone_keyword_brand = {}
    smartphone_keyword_brand_set = set()
    for line in read_data(data_path_smartphone_info):
        # Leagoo^Leagoo Lead 5^Leagoo Lead 5^October 2014
        line_list = line.split("^")
        keyword_lsit = line_list[2].split("|")
        for keyword in keyword_lsit:
            smartphone_keyword_brand[keyword] = line_list[0]
            smartphone_keyword_brand_set.add(keyword)
    common_list = list(tenaa_keyword_brand_set & smartphone_keyword_brand_set)
    with open("tenaa_kimovil_common_brand", "w")as f:
        for common in common_list:
            smartphone_name = tenaa_keyword_brand[common]
            tenaa_name = smartphone_keyword_brand[common]
            print(common + "^" + smartphone_name + "=" + tenaa_name)
            f.write(smartphone_name + "=" + tenaa_name + "\n")
    unique_file("tenaa_kimovil_common_brand")


def load_testin_ch_en():
    en_cn = {"魅蓝": "Metal", "大神": "QiKu", "畅享": "Changxiang", "荣耀畅玩": "Huawei Honor", "国美": "GOME",
             "红米": "Redmi", "坚果": "Smartisan", "平板": "Tablet", "荣耀": "Honor", "麦芒": "MaiMan", }
    for line in read_data(data_path_testin_tenaa_en):
        # 摩托罗拉 ^ Motorola ^ 摩托罗拉
        line_list = line.split("^")
        en_cn[line_list[0]] = line_list[1]
    return en_cn


def cn_to_ne(en_cn, device):
    if "(" in device:
        device = device.split("(")[0]
    if "（" in device:
        device = device.split("（")[0]
    device = device.replace("联通版", "").replace("全网通", "").replace("电信版", "").replace("移动定制版", "").replace("平板",
                                                                                                          "Tablet").replace(
        "3G版", "").replace("青春版", "").strip()
    for k, v in en_cn.items():
        if k in device:
            return device.replace(k, v)
    return device


def generate_testin_tenaa():
    """
    生成testin数据集
    resources/data/testin和tenaa中英文对照.txt
    testin^smartphone^tenaa
    testin 格式化
    :return:
    """
    en_cn = load_testin_ch_en()
    type_code = "2"
    with open("testin_version_20180905.txt", "w") as f:
        for line in read_data(data_path_testin):
            # 酷派 5891Q^品牌：酷派^型号：Coolpad 5891Q^系统：Android 4.1.2^分辨率：960*540
            line_list = line.split("^")
            brand = line_list[1].replace("品牌：", "")
            brand = en_cn.get(brand, brand)
            # print(line_list[0])
            device = cn_to_ne(en_cn, line_list[0])
            keywords = line_list[2].replace("型号：", "")
            # print([brand, device, keywords])
            #     brand = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", brand)
            device = re.sub(r'[^\x00-\x7f]', "", device).strip()
            keywords = re.sub(r'[^\x00-\x7f]', "", keywords).strip()
            print([brand, device, keywords])
            if "tablet" in device.lower() or "tablet" in keywords.lower():
                type_code = "3"
            data_str = "^".join([brand, device, type_code, keywords])
            f.write(data_str + "\n")


def clean_brackets(device_str):
    if "(" in device_str:
        device_str = device_str.split("(")[0]
    if "（" in device_str:
        device_str = device_str.split("（")[0]
    return device_str


def combine_testin_smartphone():
    """
    testin和smatphone 结合
    :return:
    """
    test_in_dict = {}
    smartphone_dict = {}
    for line in read_data("testin_version_20180905.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3
        line_list = line.split("^")
        test_in_dict[line_list[-1]] = line
    for smart_line in read_data("smartphone_info.txt"):
        # Alcatel^Alcatel A7^Alcatel A7^September 2017
        smart_line_list = smart_line.split("^")
        keyword_lsit = smart_line_list[2].split("|")
        for keyword in keyword_lsit:
            smartphone_dict[keyword] = "^".join([smart_line_list[0], clean_brackets(smart_line_list[1]), "2", keyword])
    test_in_keywords = set(test_in_dict.keys())
    smartphone_keywords = set(smartphone_dict.keys())
    all_keywords = test_in_keywords | smartphone_keywords
    with open("smartphone_and_testin.txt", "w")as f:
        for keyword_a in list(all_keywords):
            data_ = smartphone_dict.get(keyword_a, None)
            if data_ is None:
                data_ = test_in_dict.get(keyword_a, None)
            f.write(data_ + "\n")
    unique_file("smartphone_and_testin.txt")


def combine_testin_tenaa_smartphone():
    """
    testin matphone tenaa 结合
    :return:
    """
    test_in_dict = {}
    tenaa_dict = {}
    for line in read_data("smartphone_and_testin_20180905.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3
        line_list = line.split("^")
        line_list = [x.strip() for x in line_list]
        test_in_dict[line_list[-1]] = "^".join(line_list)
    for smart_line in read_data("tenaa_version_20180905.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3
        smart_line_list = smart_line.split("^")
        smart_line_list = [x.strip() for x in smart_line_list]
        tenaa_dict[smart_line_list[-1]] = "^".join(smart_line_list)
    test_in_keywords = set(test_in_dict.keys())
    smartphone_keywords = set(tenaa_dict.keys())
    all_keywords = test_in_keywords | smartphone_keywords
    with open("tenaa_smartphone_testin_20180905.txt", "w")as f:
        for keyword_a in list(all_keywords):
            data_ = test_in_dict.get(keyword_a, None)
            if data_ is None:
                data_ = tenaa_dict.get(keyword_a, None)
            f.write(data_ + "\n")
    unique_file("tenaa_smartphone_testin_20180905.txt")


def clean_ua_precise():
    """查找是否有1对多合并"""
    tt_dict = {}
    precise_dict = {}
    for line in read_data("tenaa_smartphone_testin_20180905.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3
        line_list = line.split("^")
        line_list = [x.strip() for x in line_list]
        tt_dict[line_list[-1]] = "^".join(line_list)
    for smart_line in read_data("ua2device_precise.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3|
        smart_line_list = smart_line.split("^")
        smart_line_list = [x.strip() for x in smart_line_list]
        keyword_lsit = smart_line_list[3].split("|")
        for keyword in keyword_lsit:
            precise_dict[keyword] = "^".join(
                [smart_line_list[0], clean_brackets(smart_line_list[1]), smart_line_list[2], keyword])
    test_in_keywords = set(tt_dict.keys())
    smartphone_keywords = set(precise_dict.keys())
    all_keywords = test_in_keywords | smartphone_keywords
    # print(all_keywords)
    with open("ttsp_all_20180905.txt", "w")as f:
        for keyword_a in list(all_keywords):
            data_ = precise_dict.get(keyword_a, None)
            if data_ is None:
                data_ = tt_dict.get(keyword_a, None)
            f.write(data_ + "\n")
    unique_file("ttsp_all_20180905.txt")


def reshape_data_all():
    """整理入库数据"""
    tt_dict = {}
    precise_dict = {}
    with open("ttsp_20180905_clean.txt", "w")as f:
        for line in read_data("ttsp_all_20180905.txt"):
            # Xiaomi^Xiaomi 3^2^MI 3
            line_list = line.split("^")
            line_list = [x.strip() for x in line_list]
            if "tablet" in line.lower() or " pad" in line.lower():
                line_list[2] = "3"
            if " TV^" in line or "box" in line.lower():
                line_list[2] = "4"
            line_list[3] = line_list[3].upper()
            f.write("^".join(line_list) + "\n")
    unique_file("ttsp_20180905_clean.txt")


def combine_ua_precise():
    """查找是否有1对多合并"""
    tt_dict = {}
    precise_dict = {}
    for line in read_data("ttsp_20180905_clean.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3
        line_list = line.split("^")
        line_list = [x.strip() for x in line_list]
        tt_dict[line_list[-1]] = "^".join(line_list)
    for smart_line in read_data("ua2device_precise.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3|
        smart_line_list = smart_line.split("^")
        smart_line_list = [x.strip() for x in smart_line_list]
        keyword_lsit = smart_line_list[3].split("|")
        for keyword in keyword_lsit:
            precise_dict[keyword] = "^".join(
                [smart_line_list[0], clean_brackets(smart_line_list[1]), smart_line_list[2], keyword])
    test_in_keywords = set(tt_dict.keys())
    smartphone_keywords = set(precise_dict.keys())
    all_keywords = test_in_keywords | smartphone_keywords
    # print(all_keywords)
    with open("ua_precise_20180906.txt", "w")as f:
        for keyword_a in list(all_keywords):
            data_ = precise_dict.get(keyword_a, None)
            if data_ is None:
                data_ = tt_dict.get(keyword_a, None)
            f.write(data_ + "\n")
    unique_file("ua_precise_20180906.txt")


def load_brand_device():
    """
    :return:
    """
    data_path = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/ua2device_precise.txt"
    brand_list = []
    device_list = []
    for line in read_data(data_path):
        line_list = line.split("^")
        brand_list.append(line_list[0])
        device_list.append(line_list[1].replace("?", "").strip())
    # print(device_list)
    return list(set(brand_list)), list(set(device_list))


def reformat_str(data_list, data_str):
    for data in data_list:
        if data_str.upper() == data.upper():
            return data
    return data_str.upper()


def reformat_keyword_str(brand_str, data_str):
    if "huawei" in data_str.lower() and "huawei" not in brand_str.lower():
        return False
    return True


def format_ua_precise():
    """
    删除脏数据
    GFIVE^Glory^2^HUAWEI H868C
    LG^Stylus 2^2^HUAWEI MT7-TL10
    Motorola^Droid^2^HW-HUAWEI TIT-CL00
    RIM^Curve^2^HUAWEI Y560-CL00
    RIM^Curve^2^HW-HUAWEI Y635-CL00
    Xiaomi^Mi 5^2^XIAOMI HUAWEI_H30_T10
    :return:
    """
    precise_dict = defaultdict(set)
    brand_list = []
    device_list = []
    brand_org, device_org = load_brand_device()
    for smart_line in read_data("ua_precise_20180906.txt"):
        # Xiaomi^Xiaomi 3^2^MI 3|
        smart_line_list = smart_line.split("^")
        smart_line_list[0] = smart_line_list[0]
        # .replace("huawei", "Huawei")
        smart_line_list[0] = reformat_str(brand_org, smart_line_list[0]).strip()
        smart_line_list[1] = reformat_str(device_org, smart_line_list[1]).strip()
        smart_line_list[1] = smart_line_list[1].replace("SAMSUNG GALAXY", "Galaxy")
        tag_c = reformat_keyword_str(smart_line_list[0], smart_line_list[3])
        if not tag_c:
            print(smart_line)
            continue
        brand_device = "^".join(smart_line_list[0:3]).replace("?", "").strip()
        # print(brand_device)
        brand_list.append(smart_line_list[0])
        device_list.append(smart_line_list[1])
        precise_dict[brand_device].add(smart_line_list[-1].upper())
    # print(all_keywords)
    # brand_list = list(set(brand_list))
    # brand_dict = {}
    # for brand in brand_list:
    #     # print(brand)
    #     brand_dict.setdefault(brand.upper(), 0)
    #     brand_dict[brand.upper()] += 1
    # for k, v in brand_dict.items():
    #     if v > 1:
    #         print("brand", k)
    # device_list = list(set(device_list))
    # device_dict = {}
    # for device in device_list:
    #     # print(brand)
    #     device_dict.setdefault(device.upper(), 0)
    #     device_dict[device.upper()] += 1
    # for device_k, device_v in brand_dict.items():
    #     if device_v > 1:
    #         print("device", device_k)
    with open("ua2device_precise_20180906.txt", "w")as f:
        for line_key, line_values in precise_dict.items():
            f.write(line_key + "^" + "|".join(list(line_values)) + "\n")
    unique_file("ua2device_precise_20180906.txt")


def load_ua2device(data_path):
    data_result = []
    for smart_line in read_data(data_path):
        # Xiaomi^Xiaomi 3^2^MI 3|
        smart_line_list = smart_line.split("^")
        keyword_lsit = smart_line_list[3].split("|")
        for keyword in keyword_lsit:
            data_result.append(
                "^".join([smart_line_list[0], smart_line_list[1], smart_line_list[2], keyword]))
    return data_result


def diff_list():
    ole_set = set(load_ua2device("ua2device_precise.txt"))
    new_set = set(load_ua2device("ua2device_precise_20180906.txt"))
    common = ole_set & new_set
    delete_list = ole_set - common
    add_list = new_set - common
    save_txt("delete_list_20180907.txt", delete_list, "w")
    save_txt("add_list_20180907.txt", add_list, "w")


if __name__ == "__main__":
    # check_in_tenaa()
    # generate_testin_tenaa()n
    # combine_testin_smartphone()
    # combine_testin_tenaa_smartphone()
    # clean_ua_precise()
    # reshape_data_all()
    # combine_ua_precise()
    format_ua_precise()
    diff_list()
