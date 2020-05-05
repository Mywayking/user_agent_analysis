"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/20
-------------------------------------------------
   Description: deviceatlas数据提取后制作成RTB库数据
-------------------------------------------------
"""

from last_version import ua_setting as setting, ua_fix, ua_utils as utils


def get_raw_data(path_data):
    """
    原始数据格式：
    brand +"^"+ vendor + "^" + model + "^" +marketingName + "^" + osName + "^" + primaryHardwareType + "^" + yearReleased + "^" + isTablet + "^" + identifierUa;
    保持原数据格式，提取identifierUa。
    Vivo^Y11i T^Y11^Android^Mobile Phone^2013^0^vivo Y11i T Build/KTU84P
    :return:
    """
    data_set = []
    uf = ua_fix.UaFix()
    for line in utils.read_txt(path_data):
        lines = line.split("^")
        # 过滤异常
        if uf.filter_main(lines[0], lines[8]):
            continue
        if "build/" in lines[8].lower():
            build = lines[8].lower().split("build/")[0].strip()
            if len(build) == 0:
                continue
            lines[8] = build
            data_set.append("^".join(lines))
        elif "miui/" in lines[8].lower():
            build = lines[8].lower().split("miui/")[0].strip()
            if len(build) == 0:
                continue
            lines[8] = build
            data_set.append("^".join(lines))
        else:
            pass
    return data_set


def primary_hardware_type_to_precise(path, path_save):
    """
    提取primaryHardwareType字符串作为model
    品牌：huawei
    输入：Vivo^Vivo^V5 (1601)^V5^Android^Mobile Phone^2016^0^vivo vivo x20plus a
    输出：koobee^koobee A3^2^koobee A3
    Tablet Mobile Phone
    :return:
    """
    utils.delete_existed_file(path_save)
    data_set = []
    # type_set = set()
    for line in get_raw_data(path):
        data = ua_fix.fix_ua(line)
        if data is None:
            continue
        # lines = line.split("^")
        # model = lines[3].title().strip()
        # if "ipad" in lines[8].lower() or "ipad" in lines[5].lower() or "tablet" in lines[8].lower() or "tablet" in \
        #         lines[5].lower():
        #     type_str = "3"
        # else:
        #     if lines[5] == "Mobile Phone":
        #         type_str = "2"
        #     elif lines[5] == "Tablet" or lines[5] == "eReader" or lines[5] == "Games Console":
        #         type_str = "3"
        #     elif lines[5] == "TV" or lines[5] == "Set Top Box":
        #         type_str = "4"
        #     else:
        #         continue
        #         # type_str = "what?"
        #         # type_set.add(lines[5])
        # model = utils.clean_space(model.replace("-", " "))
        # keywords = lines[8].upper().strip()
        data_set.append(data)
    # {'eReader', 'Games Console', 'Wireless Hotspot', 'Media Player', 'TV', 'Set Top Box', 'Camera', 'Embedded Network Module', 'Desktop'}
    # print(type_set)
    utils.save_to_datas_file(data_set, path_save)
    utils.deduplication_data(path_save)


def format_precise(path, path_save, path_brand_save):
    """
    输入：koobee^koobee A3^2^koobee A3
    输出：koobee^koobee A3^2^koobee A3|XXXX\
    过滤后拼接
    :return:
    """
    utils.delete_existed_file(path_save)
    data_set = []
    # models_length : length brand model type keywords
    models_length = {}
    for line in utils.read_txt(path):
        model_dict = {}
        lines = line.split("^")
        model = lines[1]
        keyword = lines[3]
        model_l = utils.delete_space(model)
        # 过滤 AA B与AAB 格式数据
        if model_l in models_length:
            old_model_len = models_length[model_l]["length"]
            # print(models_length[model_l])
            if old_model_len >= len(model):
                models_length[model_l]["model"] = model
            if not utils.whether_repeat(models_length[model_l]["keywords"], keyword):
                models_length[model_l]["keywords"] = models_length[model_l]["keywords"] + "|" + keyword
            else:
                models_length[model_l]["keywords"] = keyword
        else:
            model_dict["model"] = model
            model_dict["type"] = lines[2]
            model_dict["brand"] = lines[0]
            model_dict["length"] = len(model_l)
            model_dict["keywords"] = keyword
            models_length[model_l] = model_dict
    brand_set = set()
    for k, v in models_length.items():
        # print(v)
        brand_set.add(v["brand"])
        data_set.append(v["brand"] + "^" + v["model"] + "^" + v["type"] + "^" + v["keywords"])
    utils.save_to_datas_file(data_set, path_save)
    utils.save_to_datas_file(list(brand_set), path_brand_save)
    utils.deduplication_data(path_save)


def dropout_repeat_keywords(path, path_save_data, path_save_repeat):
    # 删除过重复值
    # Zte^yuanhang 4^2^ZTE BA610C|ZTE BA610T|ZTE BLADE A610C UA2DEVICE_PRECISE_DATE setting.device_ua_output
    utils.delete_existed_file(path_save_data)
    utils.delete_existed_file(path_save_repeat)
    keywords_repeat = utils.get_repeat_keywords(path)
    data_set = []
    data_repeat = []
    keywords_list = []
    for line in utils.read_txt(path):
        lines = utils.format_device_ua(line).split("^")
        keywords = lines[3].upper().split("|")
        for k in keywords:
            if k in keywords_repeat:
                lines_fix, keywords_list = ua_fix.fix_repeat_data(lines, keywords_list)
                if lines_fix:
                    # print(keywords_list)
                    data_set.append(lines[0] + "^" + lines[1] + "^" + lines[2] + "^" + k)
                else:
                    data_repeat.append(lines[0] + "^" + lines[1] + "^" + lines[2] + "^" + k)
            else:
                data_set.append(lines[0] + "^" + lines[1] + "^" + lines[2] + "^" + k)
    utils.save_to_datas_file(data_set, path_save_data)
    utils.deduplication_data(path_save_data)
    utils.save_to_datas_file(data_repeat, path_save_repeat)
    utils.deduplication_data(path_save_repeat)


def format_ua_device_pattern(path=setting.UA2DEVICE_PATTERN, path_save=setting.UA2DEVICE_PATTERN_DATE):
    """格式化 ua2device_pattern"""
    utils.delete_existed_file(path_save)
    data_set = []
    for line in utils.read_txt(path):
        line = utils.format_device_ua(line)
        data_set.append(line)
    utils.save_to_datas_file(data_set, path_save)
    utils.deduplication_data(path_save)


def device_ua():
    """zzy19提取数据转 RTB库类型数据 """
    # path, path_save
    # 原始数据提取
    # primary_hardware_type_to_precise(setting.device_ua_raw, setting.device_ua_format)
    # # 删除重复值
    # dropout_repeat_keywords(setting.device_ua_format, setting.device_ua_output_dropout, setting.device_ua_repeat)
    # 格式化成所需要的数据
    format_precise(setting.device_ua_format, setting.device_ua_output, setting.device_ua_brand)
    # 与第一代库合并 结合使用 ua_combine.py生成：device_ua_combine.txt
    # 更改为第一名称 ua_combine_keep_old.py 生成：device_ua_combine_20180321.txt 更新清单为：device_ua_update_list.txt


if __name__ == '__main__':
    device_ua()
