"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/20
-------------------------------------------------
   Description:
   修正规则：
   1. 以特定开头匹配词，修正为后端
        'OPPO '
        'vivo vivo '
        'vivo '
        XIAOMI MI  ->Mi
        XIAOMI HM -> Redmi
        HONOR 3C
        HW HONOR
            Xiaomi^Redmi 2^2^HONOR V8
            Xiaomi^Redmi 2^2^HONOR4
            Huawei^Y6C^2^HW HONOR 3C

   2.品牌关键词,在匹配词，确认品牌
        huawei
        honor  - Huawei^Y6C^2^HW HONOR 3C

-------------------------------------------------
"""
from last_version import ua_utils as utils


class UaFix:
    def __init__(self):
        self.xiaomi_filter_list = ["XIAOCAISHEN", "XIAOMANYAO", "XING_FOURTEEN_V3", "XINDAN", "XINGMI", "xiaolajia",
                                   "xiaoai",
                                   "XIAOXIN", "XIAOPI"]
        self.start_character_list = ["OPPO ", "vivo vivo ", "vivo "]

    def filter_main(self, brand, ua):
        if brand.upper() == "xiaomi":
            return self.xiaomi_filter(ua)

    def xiaomi_filter(self, ua):
        # 在过滤清单 返回True
        for f in self.xiaomi_filter_list:
            if f.lower() in ua.lower():
                return True
        return False


def fix_ua(ua):
    """
    原始数据Vivo^Vivo^V5 (1601)^V5^Android^Mobile Phone^2016^0^vivo vivo x20plus a
       修正规则：
    1. 以特定开头匹配词，修正为后端
        'OPPO '
        'vivo vivo '
        'vivo '
        XIAOMI MI  ->Mi
        XIAOMI HM -> Redmi
        HONOR 3C
    2.品牌关键词,在匹配词，确认品牌
        huawei
        honor  - Huawei^Y6C^2^HW HONOR 3C
        """
    lines = ua.split("^")
    # 修正设备名称
    keywords_lower = lines[8].lower()
    if len(keywords_lower) <= 3:
        return None
    if "ipad" in keywords_lower or "ipad" in lines[5].lower() or "tablet" in keywords_lower or "tablet" in \
            lines[5].lower() or "mi pad" in keywords_lower:
        type_str = "3"
    else:
        if lines[5] == "Mobile Phone":
            type_str = "2"
        elif lines[5] == "Tablet" or lines[5] == "eReader" or lines[5] == "Games Console":
            type_str = "3"
        elif lines[5] == "TV" or lines[5] == "Set Top Box":
            type_str = "4"
        else:
            return None
    # 修正model

    # oppo
    if keywords_lower.startswith("oppo "):
        model = keywords_lower
        brand = "oppo"
    elif keywords_lower.startswith("find7"):
        model = keywords_lower.replace("find7", "find7 ")
        brand = "oppo"
    elif keywords_lower.startswith("vivo vivo "):
        model = keywords_lower.replace("vivo vivo ", "vivo ")
        brand = "vivo"
    elif keywords_lower.startswith("vivo "):
        model = keywords_lower
        brand = "vivo"
    elif keywords_lower.startswith("xiaomi mi"):
        model = keywords_lower.replace("xiaomi mi", "Mi ")
        brand = "Xiaomi"
    elif keywords_lower.startswith("mi "):
        model = keywords_lower
        brand = "Xiaomi"
    elif keywords_lower.startswith("hm note"):
        # Redmi Note
        model = keywords_lower.replace("hm note", "Redmi Note ")
        brand = "Xiaomi"
    elif keywords_lower.startswith("xiaomi hm note"):
        # Redmi Note
        model = keywords_lower.replace("xiaomi hm note", "Redmi Note ")
        brand = "Xiaomi"
    elif keywords_lower.startswith("redmi"):
        # Redmi Note
        model = keywords_lower.replace("redmi", "Redmi ")
        brand = "Xiaomi"
    elif keywords_lower.startswith("mi "):
        model = keywords_lower
        brand = "Xiaomi"
    elif keywords_lower.startswith("xiaomi hm "):
        model = keywords_lower.replace("xiaomi hm ", "Redmi ")
        brand = "Xiaomi"
    elif keywords_lower.startswith("honor"):
        model = keywords_lower.replace("honor", "honor ")
        brand = "Huawei"
    elif keywords_lower.startswith("hw honor"):
        model = keywords_lower.replace("hw honor", "honor ")
        brand = "Huawei"
    # XIAOXYE
    elif keywords_lower.startswith("xiaoxye"):
        model = keywords_lower.replace("xiaoxyer", "xiaoxye ")
        brand = "XIAOXYE"
    # google
    elif keywords_lower.startswith("pixel"):
        model = keywords_lower.replace("pixel", "pixel ")
        brand = "Google"
    # HTC
    elif keywords_lower.startswith("htc butterfly"):
        model = keywords_lower.replace("htc butterfly", "htc butterfly ")
        brand = "HTC"
    elif keywords_lower.startswith("htc desire"):
        model = keywords_lower.replace("htc desire", "htc desire ")
        brand = "HTC"
    elif keywords_lower.startswith("htc "):
        model = keywords_lower
        brand = "HTC"
    # ONEPLUS
    elif keywords_lower.startswith("oneplus"):
        model = keywords_lower.replace("oneplus", "oneplus ")
        brand = "ONEPLUS"
    # Amazon
    elif keywords_lower.startswith("kindle fire hdx 7"):
        model = keywords_lower.replace("kindle fire hdx 7", "kindle fire hdx 7 ")
        brand = "Amazon"
    # huawei
    elif keywords_lower.startswith("nexus"):
        model = keywords_lower.replace("nexus", "nexus ")
        brand = "Huawei"
    else:
        model = lines[3]
        brand = lines[0]
    brand = utils.clean_space(brand).title().strip()
    model = utils.clean_space(model.replace("-", " ")).title().strip()
    keywords = lines[8]
    return utils.format_device_ua(brand + "^" + model + "^" + type_str + "^" + keywords)


def is_key_character(key_str, keywords_List):
    for k in keywords_List:
        if k in key_str:
            return True
    return False


def fix_repeat_data(lines, keywords_list):
    """修正重复值"""
    brand = lines[0].lower()
    model = lines[1].lower()
    keywords = lines[3]
    samsung_list = ["SAMSUNG", "SM-", "GT-"]
    lenovo_list = ["LENOVO"]
    huawei_list = ["HUAWEI", "KIW-", "ATH-", "WAS-", "LLD-"]
    if keywords in keywords_list:
        return False, keywords_list

    if brand == "samsung":
        if "galaxy" in model:
            if is_key_character(keywords, samsung_list):
                keywords_list.append(keywords)
                return True, keywords_list
    if brand == "lenovo":
        if is_key_character(keywords, lenovo_list):
            keywords_list.append(keywords)
            return True, keywords_list
    if brand == "huawei":
        if is_key_character(keywords, huawei_list):
            keywords_list.append(keywords)
            return True, keywords_list
    return False, keywords_list
