"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/21
-------------------------------------------------
   Description:两个库结合，提供跟新清单。
-------------------------------------------------
"""
from last_version import ua_setting as setting, ua_utils as utils


class UaCombineDetailsOld:
    def __init__(self):
        self.rtb_ua = {}
        self.atlas = {}
        self.brand_old = {}
        self.model_old = {}
        self.dataset_update_list = []

    def load_old(self, path):
        # Zte^yuanhang 4^2^ZTE BA610C|ZTE BA610T|ZTE BLADE A610C
        for line in utils.read_txt(path):
            lines = line.split("^")
            brand = utils.clean_space(lines[0]).lower()
            model = utils.clean_space(lines[1]).lower()
            if not (brand in self.brand_old):
                self.brand_old[brand] = lines[0]
            if not (model in self.model_old):
                self.model_old[model] = lines[1]

    def combine(self, path_save, path_update):
        self.load_old(setting.UA2DEVICE_PRECISE)
        self.load_old(setting.UA2DEVICE_PATTERN)
        utils.delete_existed_file(path_save)
        utils.delete_existed_file(path_update)
        dataset = []
        dataset_update_list = []
        # setting.UA2DEVICE_PRECISE_DATE 是device_ua_combine.txt复制过来的
        for line in utils.read_txt(setting.UA2DEVICE_PRECISE_DATE):
            lines = line.split("^")
            brand = utils.clean_space(lines[0]).lower()
            model = utils.clean_space(lines[1]).lower()
            if brand in self.brand_old:
                dataset_update_list.append("brand:" + lines[0] + "<=" + self.brand_old[brand])
                lines[0] = self.brand_old[brand]
            if model in self.model_old:
                dataset_update_list.append("model:" + lines[1] + "<=" + self.model_old[model])
                lines[1] = self.model_old[model]
            else:
                if model.startswith(brand):
                    model = model.replace(brand, "").strip()
                    if model in self.model_old:
                        print("model:" + lines[1] + "<=" + self.model_old[model])
                        dataset_update_list.append("model:" + lines[1] + "<=" + self.model_old[model])
                        lines[1] = self.model_old[model]
                        # for k, v in self.model_old.items():
                        #     if model.endswith(k):
                        #         dataset_update_list.append(lines[1] + "<=" + self.model_old[k])
                        #         print(lines[1] + "<=" + self.model_old[k])
                        #         lines[1] = self.model_old[k]
                        #         break
            dataset.append("^".join(lines))
        utils.save_to_datas_file(dataset, path_save)
        utils.deduplication_data(path_save)
        utils.save_to_datas_file(dataset_update_list, path_update)
        utils.deduplication_data(path_update)


if __name__ == '__main__':
    cu = UaCombineDetailsOld()
    cu.combine(setting.device_ua_combine_new, setting.device_ua_update)
