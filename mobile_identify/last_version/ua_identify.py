"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/20
-------------------------------------------------
   Description:
-------------------------------------------------
"""
from last_version import ua_utils as utils
import os


class UaIdentify:
    def __init__(self):
        self.precise = {}
        self.pattern = {}
        #  全部
        self.path_precise = "ua2device_precise.txt"
        self.path_pattern = "ua2device_pattern.txt"
        # TV
        # self.path_precise = "ua2device_tv_precise.txt"
        # self.path_pattern = "ua2device_tv_pattern.txt"
        # 项目根路径
        self.RESOURCE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/resources/ua_20180328/"

    def data_to_dict(self, data_dic, name):
        # Zte^yuanhang 4^2^ZTE BA610C|ZTE BA610T|ZTE BLADE A610C
        path = self.RESOURCE_PATH + name
        for line in utils.read_txt(path):
            model_dict = {}
            lines = utils.format_device_ua(line).split("^")
            model_dict["brand"] = lines[0]
            model_dict["model"] = lines[1]
            model_dict["type"] = lines[2]
            model_dict["keywords"] = lines[3]
            keywords = lines[3].split("|")
            for k in keywords:
                if k not in data_dic:
                    data_dic[k] = model_dict
                    # print(self.atlas[k])

    def load_data(self):
        self.data_to_dict(self.precise, self.path_precise)
        self.data_to_dict(self.pattern, self.path_pattern)

    def detect_model(self, device_ua):
        if device_ua is None:
            return None
        if device_ua in self.precise:
            return self.precise[device_ua]
        for k, v in self.pattern.items():
            if k in device_ua:
                return self.pattern[k]
        return None

    @staticmethod
    def get_ua_character(data):
        device = utils.get_device_ua(data)
        if device is not None:
            device_ua = utils.get_keywords(device)
            # print(self.precise)
            if device_ua is not None:
                return device_ua.upper()
        if "NETFLIX" in data.upper():
            return "NETFLIX"
        elif "CIBN SMARTTV" in data.upper():
            return "CIBN SMARTTV"
        elif "YOUKU SMARTTV PLAYERSDK" in data.upper():
            return "YOUKU SMARTTV PLAYERSDK"
        elif "YOUKU HD" in data.upper():
            return "YOUKU HD"
        elif "YOUKU SMARTTV" in data.upper():
            return "YOUKU SMARTTV"
        elif "SMARTHUB" in data.upper():
            return "SMARTHUB"
        elif "BRAVIA 4K 2015" in data.upper():
            return "BRAVIA 4K 2015"
        elif "OPERA TV" in data.upper():
            return "OPERA TV"
        elif "PHILIPSTV" in data.upper():
            return "PHILIPSTV"
        else:
            return None

    def identify(self, data):
        device = utils.get_device_ua(data)
        if "Windows" in device:
            return {"brand": "Windows", "model": "Windows"}
        elif "Macintosh" in device:
            return {"brand": "Apple", "model": "MacBook"}
        # (iPhone; CPU iPhone OS 10_3_2 like Mac OS X)
        # (iPad; CPU iPhone OS 10_3_2 like Mac OS X)
        elif "iphone" in device.lower() and "like Mac OS".lower() in device.lower():
            return {"brand": "Apple", "model": "iPhone"}
        elif "iPad".lower() in device.lower() and "like Mac OS".lower() in device.lower():
            return {"brand": "Apple", "model": "iPad"}
        elif "android" in device.lower():
            device_ua = utils.get_keywords(device)
            # print(self.precise)
            if device_ua is None:
                return {"brand": "", "model": ""}
            device_ua = device_ua.upper()
            if device_ua in self.precise:
                return self.precise[device_ua]
            if device_ua in self.pattern:
                return self.pattern[device_ua]
            return None

    def identify_tv(self, data):
        return self.detect_model(self.get_ua_character(data))


if __name__ == '__main__':
    cu = UaIdentify()
    cu.load_data()
    print(cu.identify(
        "EDalvik/2.1.0 (Linux; U; Android 5.1; vivo V3M A Build/LMY47I)1521071999CN_20180201_MONPARIS_LPD_YSL_FR_PROGRAMMATIC_OTV_PC_MOqqPhone_15sOT"))
