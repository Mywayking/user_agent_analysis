"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/20
-------------------------------------------------
   Description:
-------------------------------------------------
"""
from last_version import ua_setting as setting, ua_utils as utils


class UaCombine:
    def __init__(self):
        self.rtb_ua = {}
        self.atlas = {}

    def load_atlas(self):
        # Zte^yuanhang 4^2^ZTE BA610C|ZTE BA610T|ZTE BLADE A610C
        for line in utils.read_txt(setting.device_ua_output):
            model_dict = {}
            lines = utils.format_device_ua(line).split("^")
            model_dict["brand"] = lines[0]
            model_dict["model"] = lines[1]
            model_dict["type"] = lines[2]
            model_dict["keywords"] = lines[3]
            keywords = lines[3].split("|")
            for k in keywords:
                if k not in self.atlas:
                    self.atlas[k] = model_dict
                    # print(self.atlas[k])

    def combine(self, path_save):
        self.load_atlas()
        utils.delete_existed_file(path_save)
        for line in utils.read_txt(setting.UA2DEVICE_PRECISE_DATE):
            model_dict = {}
            line = utils.format_device_ua(line)
            lines = line.split("^")
            model_dict["brand"] = lines[0]
            model_dict["model"] = lines[1]
            model_dict["type"] = lines[2]
            model_dict["keywords"] = lines[3]
            keywords = lines[3].split("|")
            for k in keywords:
                if k in self.atlas:
                    # 判断品牌 相同品牌以atlas库为准 不同品牌以rtb库为准
                    if lines[0] != self.atlas[k]["brand"]:
                        self.atlas[k] = model_dict
                else:
                    self.rtb_ua[k] = model_dict
        dataset = []
        for k, v in self.atlas.items():
            dataset.append(v["brand"] + "^" + v["model"] + "^" + v["type"] + "^" + v["keywords"])
        for k, v in self.rtb_ua.items():
            dataset.append(v["brand"] + "^" + v["model"] + "^" + v["type"] + "^" + v["keywords"])
        utils.save_to_datas_file(dataset, path_save)
        utils.deduplication_data(path_save)


if __name__ == '__main__':
    cu = UaCombine()
    cu.combine(setting.device_ua_combine)
