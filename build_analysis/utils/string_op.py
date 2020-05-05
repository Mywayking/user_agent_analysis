"""
-------------------------------------------------
   Author :       galen
   date：          2018/4/19
-------------------------------------------------
   Description:
-------------------------------------------------
"""
import re


def clean_space(content):
    """多个空格转一个"""
    return re.sub(' +', ' ', content)


def delete_space(content):
    """多个空格转无"""
    return re.sub(' +', '', content)


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
            build = d.replace("build/", "").strip(";").strip(",").strip()
            if len(build) == 0:
                continue
            return build
    return None
