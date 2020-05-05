"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/28
-------------------------------------------------
   Description:
-------------------------------------------------
"""
from last_version import ua_utils as utils, ua_identify as identify
from urllib.parse import unquote


def check_ua_tv():
    # /sas/tk_history/box_ua_0327.log  zzy19
    # path_input = "/Users/wangchun/PycharmProjects/Analysis/mobile_identify/data/tv_ua_text.txt"
    path_input = "/sas/tk_history/box_ua_0327.log"
    # print(path_input)
    identify_ua = identify.UaIdentify()
    identify_ua.load_data()
    count_brand = {}
    count = 0
    for line in utils.read_txt(path_input):
        # print(line)
        count += 1
        data_result = identify_ua.identify_tv(line)
        if data_result is None:
            continue
        if data_result["brand"] in count_brand:
            count_brand[data_result["brand"]] += 1
        else:
            count_brand[data_result["brand"]] = 1
    count_brand = sorted(count_brand.items(), key=lambda e: e[1], reverse=True)
    data_set = []
    sum_brand = 0
    for k, v in count_brand:
        sum_brand += v
        data_set.append(k + "\t" + str(v) + "\t" + str(v / count))
    data_set.append("总数:" + str(count) + "\t" + "识别数:" + str(sum_brand) + "\t" + "识别率:" + str(sum_brand / count))
    utils.save_to_datas_file(data_set, "count_result.txt")


def get_not_match_ua_tv():
    # /sas/tk_history/box_ua_0327.log  zzy19
    # path_input = "/Users/wangchun/PycharmProjects/Analysis/mobile_identify/data/tv_ua_text.txt"
    path_input = "/sas/tk_history/box_ua_0327.log"
    # print(path_input)
    identify_ua = identify.UaIdentify()
    identify_ua.load_data()
    data_set = []
    count = 0
    for line in utils.read_txt(path_input):
        # print(line)
        count += 1
        data_result = identify_ua.identify_tv(line)
        if data_result is None:
            data_set.append(line)
        if len(data_set) >= 500:
            print(count)
            utils.save_to_datas_file(data_set, "not_in_list_ua_3.txt")
            data_set = []
    utils.save_to_datas_file(data_set, "not_in_list_ua_3.txt")


def clean_character(character):
    if "%" in character:
        return unquote(character).strip().upper()
    return character.strip().upper()


def check_tong_not_match_ua_tv():
    data_path = "/home/galen/ua_keywords/"
    log_name_list = ["baidu_model_0328.log", "miaozhen_model_0328.log", "youku_model_0328.log"]
    identify_ua = identify.UaIdentify()
    identify_ua.load_data()
    data_set = []
    count = 0
    count_type = {}
    path_result = data_path + "count_result.txt"
    utils.delete_existed_file(path_result)
    for name in log_name_list:
        path_input = data_path + name
        ua_not_in_path = data_path + name.replace(".log", "_output.log")
        utils.delete_existed_file(ua_not_in_path)
        print(path_input)
        for line in utils.read_txt(path_input):
            # print(line)
            count += 1
            data_result = identify_ua.detect_model(clean_character(line))
            if data_result is None:
                data_set.append(line)
            else:
                if data_result["type"] in count_type:
                    count_type[data_result["type"]] += 1
                else:
                    count_type[data_result["type"]] = 1
            if len(data_set) >= 500:
                utils.save_to_datas_file(data_set, ua_not_in_path)
                data_set = []
            if count % 100000 == 0:
                print(count)
        utils.save_to_datas_file(data_set, ua_not_in_path)
        sum_type = 0
        data_set_count = []
        for k, v in count_type.items():
            sum_type += v
            data_set_count.append(k + "\t" + str(v) + "\t" + str(v / count))
        data_set_count.append(
            "总数:" + str(count) + "\t" + "识别数:" + str(sum_type) + "\t" + "识别率:" + str(sum_type / count))
        utils.save_to_datas_file(data_set_count, path_result)


def check_tong_not_match_ua_tv_():
    data_path = "/home/galen/ua_keywords/"
    log_name_list = ["baidu_model_0328.log", "miaozhen_model_0328.log", "youku_model_0328.log"]
    identify_ua = identify.UaIdentify()
    identify_ua.load_data()
    data_set = []
    count = 0
    count_type = {}
    path_result = data_path + "count_result.txt"
    utils.delete_existed_file(path_result)
    for name in log_name_list:
        path_input = data_path + name
        ua_not_in_path = data_path + name.replace(".log", "_output.log")
        utils.delete_existed_file(ua_not_in_path)
        print(path_input)
        for line in utils.read_txt(path_input):
            # print(line)
            count += 1
            data_result = identify_ua.detect_model(clean_character(line))
            if data_result is None:
                data_set.append(line)
            else:
                if data_result["type"] in count_type:
                    count_type[data_result["type"]] += 1
                else:
                    count_type[data_result["type"]] = 1
            if len(data_set) >= 500:
                utils.save_to_datas_file(data_set, ua_not_in_path)
                data_set = []
            if count % 100000 == 0:
                print(count)
        utils.save_to_datas_file(data_set, ua_not_in_path)
        sum_type = 0
        data_set_count = []
        tv_unkown_sum = count
        for k, v in count_type.items():
            sum_type += v
            if k != "4":
                tv_unkown_sum = tv_unkown_sum - v
            data_set_count.append(k + "\t" + str(v) + "\t" + str(v / count))
        data_set_count.append(
            "总数:" + str(tv_unkown_sum) + "\t" + "识别数:" + str(sum_type) + "\t" + "识别率:" + str())
        utils.save_to_datas_file(data_set_count, path_result)


if __name__ == "__main__":
    # check_ua_tv()
    # get_not_match_ua_tv()
    check_tong_not_match_ua_tv()
