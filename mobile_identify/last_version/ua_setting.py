"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/19
-------------------------------------------------
   Description:
-------------------------------------------------
"""
import os

# 项目根路径
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
# 资源路径
RESOURCE_PATH = PROJECT_PATH + "/resources/"

# 资源
UA_BRAND_SOURCE = RESOURCE_PATH + "ua_brand.txt"

# ua 库资源

UA2DEVICE_PRECISE = RESOURCE_PATH + "ua/ua2device_precise.txt"
UA2DEVICE_PATTERN = RESOURCE_PATH + "ua/ua2device_pattern.txt"
UA2DEVICE_PATTERN_DATE = RESOURCE_PATH + "ua/ua2device_pattern_20180320.txt"
UA2DEVICE_PRECISE_DATE = RESOURCE_PATH + "ua/ua2device_precise_20180320.txt"

# device_ua
# 原始数据
device_ua_raw = RESOURCE_PATH + "raw_data/ua_brand_20180319.txt"
# 原始数据 -> 过滤原始
device_ua_format = RESOURCE_PATH + "device_ua/device_ua_format.txt"
# 原始数据 -> 整理后 ->RTB
device_ua_output = RESOURCE_PATH + "device_ua/device_ua_output.txt"
# 原始日志brand列表
device_ua_brand = RESOURCE_PATH + "device_ua/device_ua_brand.txt"
device_ua_output_dropout = RESOURCE_PATH + "device_ua/device_ua_output_dropout.txt"
device_ua_repeat = RESOURCE_PATH + "device_ua/device_ua_repeat.txt"

device_ua_combine = RESOURCE_PATH + "device_ua/device_ua_combine.txt"
device_ua_combine_new = RESOURCE_PATH + "device_ua/device_ua_combine_20180321.txt"
device_ua_update = RESOURCE_PATH + "device_ua/device_ua_update_list.txt"
device_ua_precise = RESOURCE_PATH + "device_ua/device_ua_precise.txt"

# vivo
vivo_raw = RESOURCE_PATH + "vivo/vivo_raw.txt"
vivo_build = RESOURCE_PATH + "vivo/vivo_build.txt"
vivo_not_build = RESOURCE_PATH + "vivo/vivo_not_build.txt"
vivo_precise = RESOURCE_PATH + "vivo/vivo_precise.txt"
vivo_format = RESOURCE_PATH + "vivo/vivo_format.txt"
vivo_output = RESOURCE_PATH + "vivo/vivo_output.txt"

# oppo
oppo_raw = RESOURCE_PATH + "oppo/oppo_raw.txt"
oppo_build = RESOURCE_PATH + "oppo/oppo_build.txt"
oppo_not_build = RESOURCE_PATH + "oppo/oppo_not_build.txt"
oppo_precise = RESOURCE_PATH + "oppo/oppo_precise.txt"
oppo_format = RESOURCE_PATH + "oppo/oppo_format.txt"
oppo_output = RESOURCE_PATH + "oppo/oppo_output.txt"

# huawei
huawei_raw = RESOURCE_PATH + "huawei/huawei_raw.txt"
huawei_build = RESOURCE_PATH + "huawei/huawei_build.txt"
huawei_not_build = RESOURCE_PATH + "huawei/huawei_not_build.txt"
huawei_precise = RESOURCE_PATH + "huawei/huawei_precise.txt"
huawei_format = RESOURCE_PATH + "huawei/huawei_format.txt"
huawei_output = RESOURCE_PATH + "huawei/huawei_output.txt"

# xiaomi
xiaomi_raw = RESOURCE_PATH + "xiaomi/xiaomi_raw.txt"
xiaomi_build = RESOURCE_PATH + "xiaomi/xiaomi_build.txt"
xiaomi_not_build = RESOURCE_PATH + "xiaomi/xiaomi_not_build.txt"
xiaomi_precise = RESOURCE_PATH + "xiaomi/xiaomi_precise.txt"
xiaomi_format = RESOURCE_PATH + "xiaomi/xiaomi_format.txt"
xiaomi_output = RESOURCE_PATH + "xiaomi/xiaomi_output.txt"

# samsung
samsung_raw = RESOURCE_PATH + "samsung/samsung_raw.txt"
samsung_build = RESOURCE_PATH + "samsung/samsung_build.txt"
samsung_not_build = RESOURCE_PATH + "samsung/samsung_not_build.txt"
samsung_precise = RESOURCE_PATH + "samsung/samsung_precise.txt"
samsung_format = RESOURCE_PATH + "samsung/samsung_format.txt"
samsung_output = RESOURCE_PATH + "samsung/samsung_output.txt"

# gionee
gionee_raw = RESOURCE_PATH + "gionee/gionee_raw.txt"
gionee_build = RESOURCE_PATH + "gionee/gionee_build.txt"
gionee_not_build = RESOURCE_PATH + "gionee/gionee_not_build.txt"
gionee_precise = RESOURCE_PATH + "gionee/gionee_precise.txt"
gionee_format = RESOURCE_PATH + "gionee/gionee_format.txt"
gionee_output = RESOURCE_PATH + "gionee/gionee_output.txt"
