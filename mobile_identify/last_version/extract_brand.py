"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/19
-------------------------------------------------
   Description:

-------------------------------------------------
"""

from last_version import ua_setting as setting, ua_utils as utils

import re


def get_info_form_ua(path, path_save, keyword):
    # 提取原有库数据
    data_set = []
    utils.delete_existed_file(path_save)
    for line in utils.read_txt(path):
        lines = line.split("^")
        if lines[0].upper() != keyword.upper():
            continue
        data_set.append(line)
    utils.save_to_datas_file(data_set, path_save)


def filter_xiaomi(ua):
    # 在过滤清单 返回True
    filter_list = ["XIAOCAISHEN", "XIAOMANYAO", "XING_FOURTEEN_V3", "XINDAN", "XINGMI", "xiaolajia", "xiaoai",
                   "XIAOXIN", "XIAOPI"]
    for f in filter_list:
        if f.lower() in ua.lower():
            return True
    return False


def extract_band(brand, keyword, path_data, path_raw, path_build, path_not_build):
    """
    原始数据格式
    vendor + "^" + model + "^" +marketingName + "^" + osName + "^" + primaryHardwareType + "^" + yearReleased + "^" + isTablet + "^" + identifierUa;
    Vivo^Y11i T^Y11^Android^Mobile Phone^2013^0^vivo Y11i T Build/KTU84P
    :return:
    """
    utils.delete_existed_file(path_raw)
    utils.delete_existed_file(path_build)
    utils.delete_existed_file(path_not_build)
    for line in utils.read_txt(path_data):
        if brand.lower() == "xiaomi":
            # XIAOCAISHEN XIAOMANYAO XING_FOURTEEN_V3 XINDAN XINGMI
            if filter_xiaomi(line):
                continue
        lines = line.split("^")
        if brand.lower() != lines[0].lower():
            continue
        if '(' in lines[7] or ')' in lines[7]:
            if keyword.lower() not in lines[7].lower():
                continue
            utils.save_to_data_file(line + "\n", path_raw)
        else:
            if "build/" in lines[7].lower():
                build = lines[7].lower().split("build")[0].strip()
                if len(build) == 0:
                    continue
                lines[7] = build
                utils.save_to_data_file("^".join(lines) + "\n", path_build)
            elif "miui/" in lines[7].lower():
                build = lines[7].lower().split("miui")[0].strip()
                if len(build) == 0:
                    continue
                lines[7] = build
                utils.save_to_data_file("^".join(lines) + "\n", path_build)
            else:
                utils.save_to_data_file(line + "\n", path_not_build)
    utils.deduplication_data(path_build)


def whether_repeat(model, keyword):
    if model == keyword:
        return True
    models = model.split("|")
    for m in models:
        if m == keyword:
            return True
    return False


def clean_space(content):
    """多个空格转一个"""
    return re.sub(' +', ' ', content)


def delete_space(content):
    """多个空格转无"""
    return re.sub(' +', '', content)


def identifier_ua_to_precise(path, path_precise, path_save, brand="Vivo"):
    """
    提取本身字符串作为model
    品牌：vivo oppo
    输入：Vivo^V5 (1601)^V5^Android^Mobile Phone^2016^0^vivo vivo x20plus a
    输出：koobee^koobee A3^2^koobee A3
    Tablet Mobile Phone
    :return:
    """
    utils.delete_existed_file(path_save)
    data_set = []
    for line in utils.read_txt(path):
        lines = line.split("^")
        if "VIVO VIVO" in lines[7].upper():
            model = lines[7].upper().replace("VIVO VIVO", "VIVO").title().strip()
        else:
            model = lines[7].title().strip()
        if lines[4] == "Mobile Phone":
            type_str = "2"
        else:
            type_str = "3"
        model = clean_space(model)
        keywords = lines[7].upper().strip()
        data_set.append(brand + "^" + model + "^" + type_str + "^" + keywords)
    for data in utils.read_txt(path_precise):
        datas = data.split("^")
        datas_keywords = datas[3].split("|")
        for k in datas_keywords:
            data_set.append(brand + "^" + datas[1].title() + "^" + datas[2] + "^" + k)
    utils.save_to_datas_file(data_set, path_save)
    utils.deduplication_data(path_save)


def primary_hardware_type_to_precise(path, path_precise, path_save, brand="Vivo"):
    """
    提取primaryHardwareType字符串作为model
    品牌：huawei
    输入：Vivo^V5 (1601)^V5^Android^Mobile Phone^2016^0^vivo vivo x20plus a
    输出：koobee^koobee A3^2^koobee A3
    Tablet Mobile Phone
    :return:
    """
    utils.delete_existed_file(path_save)
    data_set = []
    for line in utils.read_txt(path):
        lines = line.split("^")
        model = lines[2].title().strip()
        if lines[4] == "Mobile Phone":
            type_str = "2"
        else:
            type_str = "3"
        model = clean_space(model.replace("-", " ").replace("-", " "))
        keywords = lines[7].upper().strip()
        data_set.append(brand + "^" + model + "^" + type_str + "^" + keywords)
    for data in utils.read_txt(path_precise):
        datas = data.split("^")
        datas_keywords = datas[3].split("|")
        for k in datas_keywords:
            data_set.append(brand + "^" + datas[1].title() + "^" + datas[2] + "^" + k)
    utils.save_to_datas_file(data_set, path_save)
    utils.deduplication_data(path_save)


def combine_precise_format(path, path_save, brand="Vivo"):
    """
    输入：Vivo^V5 (1601)^V5^Android^Mobile Phone^2016^0^vivo vivo x20plus a
    输出：koobee^koobee A3^2^koobee A3
    :return:
    """
    utils.delete_existed_file(path_save)
    data_set = []
    models = {}
    models_length = {}
    for line in utils.read_txt(path):
        lines = line.split("^")
        model = lines[1].lower()
        if brand not in ["huawei", "xiaomi", "samsung", "gionee"]:
            if brand.lower() in model:
                model = brand + " " + model.replace(brand.lower(), "").strip()
            else:
                model = brand.lower() + " " + model
        model_l = delete_space(model.replace("-", " "))
        if model_l in models_length:
            old_model_len = int(models_length[model_l].split("^")[0])
            old_model = models_length[model_l].split("^")[-1]
            if old_model_len > len(model):
                model = old_model
        else:
            models_length[model_l] = str(len(model)) + "^" + model
        # model+type
        model = clean_space(model).strip().title() + "^" + lines[2]
        keywords = lines[3].upper()
        if model in models:
            if not whether_repeat(models[model], keywords):
                models[model] = models[model] + "|" + keywords
        else:
            models[model] = keywords
    for k, v in models.items():
        data_set.append(brand.title() + "^" + k + "^" + v)
    utils.save_to_datas_file(data_set, path_save)
    utils.deduplication_data(path_save)


def vivo():
    # brand, path_data, path_raw, path_build, path_not_build
    extract_band("vivo", "vivo", setting.UA_BRAND_SOURCE, setting.vivo_raw, setting.vivo_build, setting.vivo_not_build)
    get_info_form_ua(setting.UA2DEVICE_PRECISE, setting.vivo_precise, "vivo")
    identifier_ua_to_precise(setting.vivo_build, setting.vivo_precise, setting.vivo_format)
    combine_precise_format(setting.vivo_format, setting.vivo_output)


def oppo():
    # brand, path_data, path_raw, path_build, path_not_build
    extract_band("oppo", "oppo", setting.UA_BRAND_SOURCE, setting.oppo_raw, setting.oppo_build, setting.oppo_not_build)
    get_info_form_ua(setting.UA2DEVICE_PRECISE, setting.oppo_precise, "oppo")
    identifier_ua_to_precise(setting.oppo_build, setting.oppo_precise, setting.oppo_format, "oppo")
    combine_precise_format(setting.oppo_format, setting.oppo_output, "oppo")


def huawei():
    # brand, path_data, path_raw, path_build, path_not_build
    extract_band("huawei", "huawei", setting.UA_BRAND_SOURCE, setting.huawei_raw, setting.huawei_build,
                 setting.huawei_not_build)
    # get_info_form_ua(setting.UA2DEVICE_PRECISE, setting.huawei_precise, "huawei")
    primary_hardware_type_to_precise(setting.huawei_build, setting.huawei_precise, setting.huawei_format, "huawei")
    combine_precise_format(setting.huawei_format, setting.huawei_output, "huawei")


def xiaomi():
    # brand, path_data, path_raw, path_build, path_not_build
    extract_band("xiaomi", "xiaomi", setting.UA_BRAND_SOURCE, setting.xiaomi_raw, setting.xiaomi_build,
                 setting.xiaomi_not_build)
    get_info_form_ua(setting.UA2DEVICE_PRECISE, setting.xiaomi_precise, "xiaomi")
    primary_hardware_type_to_precise(setting.xiaomi_build, setting.xiaomi_precise, setting.xiaomi_format, "xiaomi")
    combine_precise_format(setting.xiaomi_format, setting.xiaomi_output, "xiaomi")


def gionee():
    # brand, path_data, path_raw, path_build, path_not_build
    # extract_band("gionee", "gionee", setting.UA_BRAND_SOURCE, setting.gionee_raw, setting.gionee_build,
    #              setting.gionee_not_build)
    get_info_form_ua(setting.UA2DEVICE_PRECISE, setting.gionee_precise, "gionee")
    # primary_hardware_type_to_precise(setting.gionee_build, setting.gionee_precise, setting.gionee_format, "gionee")
    # combine_precise_format(setting.gionee_format, setting.gionee_output, "gionee")


if __name__ == '__main__':
    gionee()
