"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/19
-------------------------------------------------
   Description:
-------------------------------------------------
"""
import os
import re


def read_txt(filename, model="r"):
    """读取文件"""
    with open(filename, model, encoding='UTF-8', errors='ignore') as f:
        while True:
            lines = f.readline().strip('\n')
            if not lines:
                break
            yield lines


def save_to_data_file(data, filename, mode="a"):
    """保存文件"""
    with open(filename, mode)as f:
        f.write(data)


def save_to_datas_file(data_list, filename, mode="a"):
    """保存文件"""
    with open(filename, mode)as f:
        for data in data_list:
            f.write(data + "\n")


def deduplication_data(data_path):
    """数据shell命令去重"""
    command = "awk '!a[$0]++' {0}|sort -o {1}".format(data_path, data_path)
    print(command)
    os.system(command)


def delete_existed_file(path):
    """删除已存在文件"""
    if os.path.exists(path):
        print("删除已存在文件夹:{}".format(path))
        os.remove(path)
    else:
        print("不存在文件夹:{}".format(path))


def clean_space(content):
    """多个空格转一个"""
    return re.sub(' +', ' ', content)


def delete_space(content):
    """多个空格转无"""
    return re.sub(' +', '', content)


def whether_repeat(keywords, keyword):
    """匹配词 去重"""
    if keywords.upper() == keyword.upper():
        return True
    models = keywords.split("|")
    for m in models:
        if m.upper() == keyword.upper():
            return True
    return False


def format_device_ua(ua):
    """
    格式如下：Zte^yuanhang 4^2^ZTE BA610C|ZTE BA610T|ZTE BLADE A610C
    格式化规则：
    1.brand  长度小于4 全部大写
    2.model 全部为 title 格式，即每个单词首字母大写
    3.keywords 全部大写
    :param ua:
    :return:
    """
    ua_list = ua.split("^")
    if len(ua_list[0]) >= 4:
        ua_list[0] = ua_list[0].title()
    else:
        ua_list[0] = ua_list[0].upper()
    ua_list[1] = ua_list[1].title()
    ua_list[3] = ua_list[3].upper()
    return "^".join(ua_list)


def get_repeat_keywords(path):
    # 获取重复的keyword list
    keywords_list = []
    keywords_repeat = []
    for line in read_txt(path):
        lines = line.upper().split("^")
        keywords = lines[3].split("|")
        for k in keywords:
            if k not in keywords_list:
                keywords_list.append(k)
            else:
                keywords_repeat.append(k)
    return keywords_repeat


# 以下是识别代码
def get_device_ua(s):
    # m = re.match(".*\((.*)\).*", s)
    # return m.group(1)
    ua_str = re.findall(r'[^()]+', s)
    # print(ua_str)
    if len(ua_str) >= 2:
        return ua_str[1]
    return None


def get_keywords(device):
    device_list = device.split(";")
    for d in device_list:
        if "build/" in d.lower():
            build = d.lower().split("build/")[0].strip()
            if len(build) == 0:
                continue
            return build
        elif "miui/" in d.lower():
            build = d.lower().split("miui/")[0].strip()
            if len(build) == 0:
                continue
            return build
    return None


def get_keywords_build(device):
    device_list = device.split(" ")
    for d in device_list:
        d = d.lower()
        if "build/" in d:
            # print(d)
            build = d.replace("build/", "").strip()
            if len(build) == 0:
                continue
            return build
    return None
