"""
-------------------------------------------------
   Author :       galen
   date：          2018/4/18
-------------------------------------------------
   Description:
   zzy19
        /sas/bs_history/
-------------------------------------------------
"""

from build_analysis.utils import *
from build_analysis.setting import RESOURCE_PATH, ANDROID_BUILD

build_dict = {}


# build_android = {}


def get_android_build():
    global build_android
    build_list = reads_txt(ANDROID_BUILD)
    build_android = dict.fromkeys(build_list, 0)


def dict2list(dic: dict):
    """将字典转化为列表"""
    keys = dic.keys()
    vals = dic.values()
    lst = [key + "\t" + str(val) for key, val in zip(keys, vals)]
    return lst


def get_build(data):
    device = get_device_ua(data)
    if device is None:
        return
    if "android" not in device.lower():
        return
    device_ua = get_keywords_build(device)
    # print(self.precise)
    if device_ua is not None:
        return device_ua.upper()
    return


def get_data_from_file(path):
    for line in read_txt(path):
        try:
            lines = line.split("\001")
            build = get_build(lines[4])
            if build is None:
                continue
            if build in build_dict:
                build_dict[build] += 1
            else:
                build_dict[build] = 1
            if build in build_android:
                build_android[build] += 1
        except:
            print("error")


def start_work(data_path, save_name, save_android):
    path_save = RESOURCE_PATH + save_name
    path_save_android = RESOURCE_PATH + save_android
    file_list = os.listdir(data_path)
    get_android_build()
    for file_name in file_list:
        if not (file_name.endswith(".log")):
            continue
        if not (file_name.startswith("bs_20180417")):
            continue
        print(file_name)
        get_data_from_file(data_path + file_name)
        if len(build_dict) > 100000:
            save_to_datas_file(dict2list(build_dict), path_save, "w")
            break
    save_to_datas_file(dict2list(build_dict), path_save, "w")
    sort_data(path_save)
    save_to_datas_file(dict2list(build_android), path_save_android, "w")
    sort_data(path_save_android)


if __name__ == '__main__':
    start_work("/sas/bs_history/", "build_list.txt", "android_build.txt")
    # start_work("/Users/wangchun/PycharmProjects/user_agent_analysis/resources/test_data/", "build_list_1.txt",
    #            "android_build.txt")
