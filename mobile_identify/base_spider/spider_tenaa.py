"""
抓取工信部手机信息
"""
import os
import re

import requests
from lxml import etree
from urllib.parse import quote


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
    command_mv = "mv {0} {1}".format(tmp_path, path)
    print(command)
    os.system(command)
    print(command_mv)
    os.system(command_mv)


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


def request_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; SM919 Build/WangGuoJun) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36"}
    html = requests.get(url, headers=headers)
    html.encoding == 'gbk'  # gb2312 和 gbk  解决：普达
    # print(html.headers['content-type'])
    # print("response内容的encoding编码:", html.encoding)
    # print("response headers里设置的apparent_encoding编码:", html.apparent_encoding)
    # print("response返回的html header标签里设置的编码:", requests.utils.get_encodings_from_content(html.text))
    selector = etree.HTML(html.text)
    return selector


def extract_device(data_str):
    """
    根据品牌名(data_str)调用设备信息
    e.g.

    extract_device("艾炜特")
    print(extract_device("宏碁"))
    艾炜特
    http://shouji.tenaa.com.cn/JavaScript/WebStation.aspx?DM=%B0%AC%EC%BF%CC%D8&type=4&return=ddlSJXH

    Page Structure:
    e.g.
        <select name="ddlSJXH" id="ddlSJXH">
            <option value="">----2012----</option>
            <option value="I506,2012">I506</option>
            <option value="i3-022W,2012">i3-022W</option>

        </select>

    :param data_str:
    :return: ['I506,2012', 'i3-022W,2012']
    """
    # data_str_quote = quote(data_str, "gb2312")
    data_str_quote = quote(data_str.encode("GBK"))
    url = "http://shouji.tenaa.com.cn/JavaScript/WebStation.aspx?DM={0}&type=4&return=ddlSJXH".format(data_str_quote)
    selector = request_page(url)
    values_list = selector.xpath("//select/option/@value")
    values_list = [x for x in values_list if len(x) > 0]
    # print(values_list)
    return values_list


def extract_brand():
    """
    提取工信部厂家品牌信息
    http://shouji.tenaa.com.cn/index.aspx

    :return:
    """
    url = "http://shouji.tenaa.com.cn/index.aspx"
    selector = request_page(url)
    # values_list = selector.xpath("//select[@id='ddlSCQY']/option/@value")
    values_list = selector.xpath("//select[@id='ddlSCQY_SH']/option/@value")
    values_list = [x for x in values_list if len(x) > 0]
    # print(len(values_list))
    return values_list


def extract_device_os():
    """
    提取工信部厂家设备操作系统
    http://shouji.tenaa.com.cn/index.aspx

    :return:
    """
    url = "http://shouji.tenaa.com.cn/index.aspx"
    selector = request_page(url)
    # values_list = selector.xpath("//select[@id='ddlSCQY']/option/@value")
    values_list = selector.xpath("//select[@id='ddlCZXT_XJZX']/option/@value")
    values_list = [x for x in values_list if len(x) > 0]
    # print(len(values_list))
    save_txt("device_os", values_list, "w")
    unique_file("brand_name")


def extract_shouji_tenaa():
    """

    :return:
    """
    brand_list = extract_brand()
    # brand_list = list(map(lambda x: x.decode("GB2312"), brand_list))
    count = 0
    save_txt("brand_name", brand_list)
    for brand in brand_list:
        count += 1
        try:
            print(brand, count)
            device_list = extract_device(brand)
            save_list = list(map(lambda x: brand + "^" + x, device_list))
            save_txt("tenaa_brand_device", save_list)
        except Exception as e:
            print(e, brand)
    unique_file("brand_name")
    unique_file("tenaa_brand_device")
    # print(brand_list)


def load_brand_cn_en(data_path="/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/tenaa中英文对照.txt"):
    data_dict = {}
    for line in read_data(data_path):
        line_list = line.split("^")
        data_dict[line_list[0]] = line_list[1]
    return data_dict


def filter_2018():
    """
    沃普丰^WellPhone
    青橙^QingCheng
    帷幄^VWAL
    先科^SAST
    宇飞来^YuFly
    百合^BIHEE
    奥洛斯^ALOES
    :return:
    """
    data_path = "/Users/wangchun/PycharmProjects/user_agent_analysis/resources/data/tenaa_brand_device"
    brand_en_dict = {}
    brand_ch_en = load_brand_cn_en()
    # brand_ch_en = {"LG": "LG", "中国移动": "China Mobile", "华硕": "Asus", "诺基亚": "Nokia", "戴尔": "Dell", "联想": "Lenovo",
    #                "维沃": "vivo", "三星": "Samsung", "欧珀": "OPPO", "360": "360", "酷派": "Coolpad", "海信": "Hisense",
    #                "创维": "Skyworth", "乐视": "LeEco", "华为": "Huawei", "艾优尼": "IUNI", "锤子": "Smartisan", "金立": "Gionee",
    #                "宏达": "HTC", "摩托罗拉": "Motorola", "魅族": "Meizu", "努比亚": "Nubia", "索尼": "Sony", "一加": "OnePlus",
    #                "中兴": "ZTE", "谷歌": "Google", "美图": "Meitu", "小米": "Xiaomi", "宏基": "Acer", "沃普丰": "WellPhone",
    #                "青橙": "QingCheng", "帷幄": "VWAL", "先科": "SAST", "宇飞来": "YuFly", "百合": "BIHEE", "奥洛斯": "ALOES",
    #                "贝尔丰": "Bifermobile", "小辣椒": "Xiaolajiao", "詹姆士": "GEMRY"}
    cn_brand_list = set()
    for line in read_data(data_path):
        # 索信^SOXN SD-599,2011
        line_list = line.replace(",", "^").split("^")
        brand_en = brand_ch_en.get(line_list[0], None)
        if brand_en is not None:
            key_str = line_list[0] + "^" + brand_en
            brand_en_dict.setdefault(key_str, 0)
            brand_en_dict[key_str] += 1
            continue
        if int(line_list[2]) > 2015:
            brand_filter = re.sub(r'[^\x00-\x7f]', "", line_list[0]).strip()
            if len(brand_filter) == len(line_list[0]):
                # if line_list[0].isalpha():
                key_str = line_list[0] + "^" + line_list[0]
                # print(key_str)
                brand_en_dict.setdefault(key_str, 0)
                brand_en_dict[key_str] += 1
            elif ' ' in line_list[1]:
                key_brand = line_list[1].split(' ')[0]
                key_brand_filter = re.sub(r'[^\x00-\x7f]', "", key_brand).strip()
                if key_brand_filter != key_brand:
                    # print(line_list)
                    cn_brand_list.add(line_list[0])
                    continue
                if len(key_brand) <= 2:
                    # print(key_brand)
                    print(line_list)
                key_str = line_list[0] + "^" + key_brand
                brand_en_dict.setdefault(key_str, 0)
                brand_en_dict[key_str] += 1
            else:
                # print(line_list)
                cn_brand_list.add(line_list[0])
    data_result = sort_dict(brand_en_dict)
    with open("tenaa_cn_en.txt", "w")as f:
        data_b = set()
        data_d = set()
        for result in data_result:
            # print(result[0], result[1])
            list_data = result[0].split("^")
            data_b.add(list_data[0])
            data_d.add(list_data[1])
            f.write(result[0].replace("vivi", "Vivi") + "\n")
            # f.write(result[0] + "^" + str(result[1]) + "\n")
    # print(cn_brand_list)
    print(len(data_b), len(data_d))
    unique_file("tenaa_cn_en.txt")


def cn_to_ne(en_cn, device):
    if "(" in device:
        device = device.split("(")[0]
    if "（" in device:
        device = device.split("（")[0]
    for k, v in en_cn.items():
        if k in device:
            if v in device:
                return device.replace(k, "")
            return device.replace(k, v)
    return device


def generate_tenaa():
    resource_path = "/Users/wangchun/PycharmProjects/user_agent_analysis/"
    save_path = "tenaa_version_20191217.txt"
    brand_ch_en = load_brand_cn_en()
    with open(save_path, "w")as f:
        for line in read_data(resource_path + "resources/data/tenaa_brand_device"):
            # 索信^SOXN SD-599,2011
            line_list = line.replace(",", "^").split("^")
            brand_en = brand_ch_en.get(line_list[0], None)
            if brand_en is None:
                continue
            device = cn_to_ne(brand_ch_en, line_list[1])
            keywords = line_list[1]
            f.write(clean_space("^".join([brand_en, device, "2", keywords])) + '\n')
    unique_file(save_path)


if __name__ == "__main__":
    # extract_shouji_tenaa()
    # filter_2018()
    generate_tenaa()
