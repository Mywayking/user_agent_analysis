"""
抓取https://www.kimovil.com/设备信息
"""
import os

import requests
from lxml import etree


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
    print("file_dir_list", file_dir_list)
    tmp_path = "/".join(file_dir_list)
    # tmp_path = "/".join(file_dir_list) + "/tmp_file.txt"
    print(tmp_path)
    command = "cat {0}|awk '!a[$0]++'>{1}".format(path, tmp_path)
    print(command)
    os.system(command)
    os.remove(tmp_path)


def request_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; SM919 Build/WangGuoJun) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36"}
    html = requests.get(url, headers=headers)
    html.encoding == 'utf-8'
    # print(html.headers['content-type'])
    # print("response内容的encoding编码:", html.encoding)
    # print("response headers里设置的apparent_encoding编码:", html.apparent_encoding)
    # print("response返回的html header标签里设置的编码:", requests.utils.get_encodings_from_content(html.text))
    selector = etree.HTML(html.text)
    return selector


def extract_smartphone_detail(url):
    """
    提取 brand, device, aliases
    :param url:
    :return: e.g. LeEco (LeTV)^LeEco Le 3 Pro^X651|Le Pro 3^April 2017
    """
    # url = "https://www.kimovil.com/en/where-to-buy-huawei-nova-3"
    # url = "https://www.kimovil.com/en/where-to-buy-leeco-le-3-pro"
    selector = request_page(url)
    brand = selector.xpath('//*[@id="about"]/div/div[1]/div[2]/dl/dd[1]/text()')[0].strip()
    device = selector.xpath('//*[@id="basics"]/div/div[2]/h1/text()')[1].strip()
    unveiled = selector.xpath('//*[@id="about"]/div/div[2]/div[2]/dl/dd[1]/text()')[0].strip().strip(",")
    aliases_list = selector.xpath('//*[@id="about"]/div/div[1]/div[2]/dl/dd[2]//text()')
    aliases_list = [x.strip().replace("&quot;", "") for x in aliases_list if x.strip().replace("&quot;", "") != ","]
    aliases_list.insert(0, device)
    aliases = '|'.join(aliases_list).replace("\n", "").replace(",", "|")
    # print([brand, device, aliases, unveiled])
    return "^".join([brand, device, aliases, unveiled])


def extract_smartphone_url(url):
    """
    抓取细分设备的url
    :param url:
    :return:
    """
    selector = request_page(url)
    url_list = selector.xpath("//ul[@class='simple-device-list clear']/li[@class='item']/a/@href")
    return url_list


def extract_smartphone_brand_device_info():
    url = "https://www.kimovil.com/en/all-smartphone-brands"
    selector = request_page(url)
    brand_url_list = selector.xpath("//ul[@id='inline-search-list']/li[@class='item']/a/@href")
    for band_url in brand_url_list:
        device_list = extract_smartphone_url(band_url)
        print(band_url)
        with open("smartphone_info.txt", "a")as f:
            for device_url in device_list:
                try:
                    data_info = extract_smartphone_detail(device_url)
                    print(data_info)
                    f.write(data_info + '\n')
                except Exception as e:
                    print(e)
    unique_file("smartphone_info.txt")


def extract_smartphone_brand():
    """
    抓取 品牌的英文名单
    :return:
    """
    url = "https://www.kimovil.com/en/all-smartphone-brands"
    selector = request_page(url)
    name_list = selector.xpath("//ul[@id='inline-search-list']/li[@class='item']/a/div/h3/text()")
    name_list = list(map(lambda x: x.strip(), name_list))
    print(name_list)
    save_txt("english_brand_name", name_list, "w")


if __name__ == "__main__":
    # extract_smartphone_brand()
    extract_smartphone_brand_device_info()
    # print(extract_smartphone_detail("https://www.kimovil.com/en/where-to-buy-alcatel-pixi-4-6"))
