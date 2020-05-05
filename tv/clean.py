# -*- coding: utf-8 -*-#
"""
@author:Galen
@file: clean.py
@time: 2019/01/15
@description:
"""
import os
import re

from collections import defaultdict

origin_data = '/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20190115/non-ott-ua-20190103.txt'
resource_path = '/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20190115/'


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
    command = "cat {0}|awk '!a[$0]++'>{1}".format(path, tmp_path)
    # command = "cat {0}|sort -u|uniq >{1}".format(path, tmp_path)
    os.system(command)
    os.remove(path)
    os.rename(tmp_path, path)
    print("Duplicate removal ！")


def path_join(file_name):
    return os.path.join(resource_path, file_name)


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


def get_device_ua(s):
    # m = re.match(".*\((.*)\).*", s)
    # return m.group(1)
    ua_str = re.findall(r'[^()]+', s)
    # print(ua_str)
    if len(ua_str) >= 2:
        return ua_str[1]
    return None


def filter_log_eui():
    """
    android EUI tvEUI
    android/4.0.4 (EUI;S40-c80e77266534-) tvEUI/3.0.050S.1009/aps_tm_03_3.0.8.4
    LeEco^Letv X3-40^4^LETV X3-40
    :return:
    """
    eui_list = []
    other_list = []
    for data in read_data(origin_data):
        if "EUI" in data and "tvEUI" in data:
            eui_list.append(data)
        else:
            other_list.append(data)

    save_txt(resource_path + 'tvEUI.txt', eui_list)
    save_txt(resource_path + 'other_1.txt', other_list)


def filter_log_normal():
    """
    Dalvik/2.1.0 (Linux; U; Android 7.0; V3C Build/HMD-2.0.5)
    Mozilla/5.0 (Linux; Android 2.1.0-R-20170818.1715; CVTM638_768_PC821_W Build/d4ced523_20170818_165546) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36

    CVTE
    Mozilla/5.0 (Linux; Android 2.1.0-R-20170819.2158; CVTE_HV320_512M_PC821_W Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36
    https://www.znds.com/tv-620628-1-1.html
    http://browser.geekbench.com/geekbench3/8419757

    :return:
    """
    eui_list = []
    other_list = []
    for data in read_data(resource_path + 'other_1.txt'):
        if data.startswith('Dalvik') or data.startswith('Mozilla'):
            eui_list.append(data)
        else:
            other_list.append(data)
    save_txt(resource_path + 'normal.txt', eui_list)
    save_txt(resource_path + 'other_2.txt', other_list)


def result_eui():
    """
    android/4.0.4 (EUI;S50-c80e7720c85d-) tvEUI/3.0.052S.1220/aps_tm_03_3.0.8.4
    LeEco^Letv X3-40^4^LETV X3-40
    :return:
    """
    data_path = '/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20190115/tvEUI.txt'
    data_dict = defaultdict(set)
    for data in read_data(data_path):
        if "EUI" in data and "tvEUI" in data:
            key_str = get_device_ua(data).split(';')[-1].strip()
            if len(key_str) <= 2:
                continue
            # key_str = data.split('tvEUI')[0].split("EUI")[-1].split(';')[-1]  # .split('-')[0].strip().upper()
            brand = key_str.split('-')[0].strip().upper()
            # print(key_str)
            data_dict[brand].add(key_str)
    with open(resource_path + 'result_tvEUI_20190115.txt', 'w')as f:
        for k, v in data_dict.items():
            # LeEco^Letv X3-40^4^LETV X3-40
            # print(k, v)
            if 'Letv' in k:
                print(k)
                continue
            f.write('LeEco^Letv {0}^4^{1}\n'.format(k, k))
            # f.write('LeEco^Letv {0}^4^{1}\n'.format(k, '|'.join(v)))


def result_normal():
    """
    android/4.0.4 (EUI;S50-c80e7720c85d-) tvEUI/3.0.052S.1220/aps_tm_03_3.0.8.4
    LeEco^Letv X3-40^4^LETV X3-40

    Dalvik/1.6.0 (Linux; U; Android 4.0.3 Build/BesTV_OS_AHYD_2.3.0.11)
    :return:
    """
    data_path = '/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20190115/normal.txt'
    data_list = []
    for data in read_data(data_path):
        data_key_str = get_device_str(data)
        if data_key_str is None:
            continue
        data_list.append(data_key_str)
    save_txt(path_join('normal_key_str.txt'), data_list)


def clean_normal_1():
    """
    1. 10MNNOS_D8   10moons Box^10MOONS_T2U^4^10MOONS_T2U
    2. Philips
        32PFD5022_30 32PHF5212_T3_2NDP Philips TV^32PHF5361_T3^4^32PHF5361_T3
        Philips TV^32PHF5000^4^32PHF500
        ALIFUNUI_PHILIPS_48PFF5081T3_MT5507_S08
    3. 43D2F
        WHALEY TV^WTV43K1G^4^WTV43K1G
    4. Hisense TV^IP808H-B^4^IP808H-B
        IP508H(13U0)
        IP508H(13U1)
        IP508H(13U1)
        IP508H(13U1)
        IP508H(13U1)
        IP508H(13U1)
        IP508H(13U2)
        IP508H(13U2)
        IP508H(13U2)
        IP508H(13U2)
        IP508H(13U2)
        IP508H(13U9)
        IP508H(88T1)
    5. CVTE CVTE_RISONG_RTD2984D_AA0001
        Hisense TV^CVTE_MSD338_512M_PC821^4^CVTE_MSD338_512M_PC821
    6 Sony TV^CVTM638_768_PC821^4^CVTM638_768_PC821
       CVTM CVTM628
    7. WASU TV^WASU_MagicBox_SHC^4^WASU_MAGICBOX_SHC
        WASU_MAGICBOX_SXU
    8.  YMB0300-CW
        YMB0300-HX
        YMB0300-HX????QQ45853991
        YMB0310-CW
    :return:
    """
    data_path = '/Users/wangchun/PycharmProjects/user_agent_analysis/resources/20190115/normal_sort.txt'
    with open(path_join('normal_result.txt'), 'w')as f:
        for data in read_data(data_path):
            # print(data)
            # if data.startswith('10MOONS'):
                # brand = data.strip().replace('/', '_').replace('-', '_').split("_")
                # brand_str = '_'.join(brand[0:2])
                # f.write("10moons Box^{0}^4^{1}\n".format(brand_str, data))
                # continue
            # if len(data) >= 9:
                # print(data[2:5])
                # if data[2:5] in ['PFD', "PHF", "HFF", "PUF", "POD"]:
                #     brand = data.strip().replace('/', '_').replace('-', '_').split("_")
                #     brand_str = '_'.join(brand[0:2])
                #     f.write("Philips TV^{0}^4^{1}\n".format(brand_str, data))
                # continue
            # if data.startswith('43D2F'):
            #     brand_str = data.strip().replace('/', '_').replace('-', '_')
            #     f.write("WHALEY TV^{0}^4^{1}\n".format(brand_str, data))
            # if data.startswith('IP508H'):
            #     brand_str = data.strip().split('(')[0]
            #     f.write("Hisense TV^{0}^4^{1}\n".format(brand_str, data))
            # if "ALIFUNUI_PHILIPS" in data:
            #     # ALIFUNUI_PHILIPS_48PFF5081T3_MT5507_S08
            #     brand_str = data.strip()
            #     f.write("Philips TV^{0}^4^{1}\n".format(brand_str, data))
            # if data.startswith('CVTE'):
            #     brand_str = data.strip().replace('/', '_').replace('-', '_')
            #     f.write("Hisense TV^{0}^4^{1}\n".format(brand_str, data))
            # if data.startswith('CVTM'):
            #     brand_str = data.strip().replace('/', '_').replace('-', '_')
            #     f.write("Sony TV^{0}^4^{1}\n".format(brand_str, data))
            if data.startswith('WASU'):
                brand_str = data.strip()#.replace('/', '_').replace('-', '_')
                f.write("WASU TV^{0}^4^{1}\n".format(brand_str, data))

if __name__ == "__main__":
    # filter_log_eui()
    # filter_log_normal()
    # result_eui()
    # result_normal()
    clean_normal_1()
