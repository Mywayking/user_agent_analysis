"""
-------------------------------------------------
   Author :       galen
   date：          2018/3/15
-------------------------------------------------
   Description:
-------------------------------------------------
"""
from deviceatlas import DeviceAtlas

# DA = DeviceAtlas('/Users/johnboxall/git/device/DeviceAtlas.json')
DA = DeviceAtlas('/Users/wangchun/PycharmProjects/Analysis/user_agent_identyfy/resources/device_detection.json')
ua = 'Mozilla/5.0 (Linux; Android 5.1; vivo X6Plus D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.5.1280(0x26060533) NetType/4G Language/zh_CN'
# ua = 'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95/11.0.026; Profile MIDP-2.0 Configuration/CLDC-1.1) AppleWebKit/413 (KHTML, like Gecko) Safari/413'
n95 = DA.device(ua)
# n95.model
# print(n95.values())
print(n95)