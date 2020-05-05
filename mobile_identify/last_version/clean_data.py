"""
-------------------------------------------------
   Author :       galen
   date：          2018/2/7
-------------------------------------------------
   Description:清新数据

-------------------------------------------------
"""

from urllib.request import unquote

# DATA_UA_PATH = "/Users/wangchun/PycharmProjects/Analysis/user_agent_identyfy/data/test_data_hadoop"
# DATA_OUTPUT_PATH = "/Users/wangchun/PycharmProjects/Analysis/user_agent_identyfy/data/ua_device"
DATA_UA_PATH = "/home/galen/ua_meishu/meishu_ua.log"
DATA_OUTPUT_PATH = "/home/galen/ua_meishu/ua_device"


def _read_file_lines(path):
    """按照行读取文件"""
    with open(path, "r")as f:
        while True:
            lines = f.readline().strip('\n')
            if not lines:
                break
            yield lines


def _save_file(path, data):
    """按照行读取文件"""
    with open(path, "a")as f:
        for line in data:
            f.write(line + "\n")


def del_specil_character(character):
    """
    unquote，解码 % 号问题
    :param character:
    :return:
    """
    if "%" not in character:
        return character
    return unquote(character)


def get_device_str(ua):
    ua = ua.upper()
    if "BUILD/" in ua:
        return ua.split("BUILD/")[0].split(";")[-1].strip()
    elif "MIUI/" in ua:
        return ua.split("MIUI/")[0].split(";")[-1].strip()
    elif "APHONE" in ua:
        return ua.split("APHONE")[0].split(";")[-1].strip()
    else:
        return None


def start_clean_ua(ua):
    """
    1.替换 % 编码问题
    2.替换 \ /
    3.
    MagicBox^MagicBox1s_Pro^4^MAGICBOX1S_PRO
    str.title() title()方法:返回标题化字符串，即所有的单词以大写开始，其余的为小写
    :param ua:
    :return:
    """
    ua = ua.split("\t")[0].replace("\/", "/")
    ua = del_specil_character(ua)
    ua_list = ua.split("^")
    model = ua_list[0].strip()
    if model == "\"}":
        return None
    brand = ua_list[1].strip()
    type_ua = ua_list[2].strip()
    keyword = get_device_str(ua_list[3])
    if keyword is None:
        return None
    return model + "^" + brand + "^" + keyword + "^" + type_ua


def start_clean():
    data_set = []
    for line in _read_file_lines(DATA_UA_PATH):
        try:
            data = start_clean_ua(line)
            if data is not None:
                data_set.append(data)
        except Exception as e:
            print(e, line)
        if len(data_set) > 5:
            _save_file(DATA_OUTPUT_PATH, data_set)
            data_set = []
    _save_file(DATA_OUTPUT_PATH, data_set)


if __name__ == '__main__':
    start_clean()
    # ua_1 = "\"}^^android^Mozilla\/5.0 (Linux; U; Android 7.1.1; zh-cn; vivo X9i Build\/NMF26	1"
    # ua_2 = "%20OPPO%20R9tmkm^%20OPPO%20R9tmkm^android^Mozilla%2F5.0%20(Linux%3B%20U%3B%20Android%206.0.1%3B%20zh-CN%3B%20OPPO%20R9s%20Build%2FMMB29M%3	1"
    # ua_3 = "ãã^魅蓝 Noto3^android^Dalvik\/2.1.0 &#40;Linux; U; Android 5.1; ãã Build\/LMY47I&#41	1"
    # start_clean_ua(ua_1)
    # start_clean_ua(ua_2)
    # start_clean_ua(ua_3)
