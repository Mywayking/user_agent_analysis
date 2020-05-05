# User Agent 识别手机型号
提取user agent有效字段对应的品牌和设备信息，整理后入库。

- [规范化](#规范化)
- [数据源](#数据源)
- [数据格式](#数据格式)
- [提取UA关键字段对应品牌与设备信息方式设备信息](#提取ua关键字段对应品牌与设备信息方式设备信息)
    - [工信部手机备案](#工信部手机备案)
    - [testin真机数据抓取](#testin真机数据抓取)
    - [kimovil网站数据抓取](#kimovil网站数据抓取)
- [扩充UA关键字段对应品牌与设备信息方式设备信息方式](#扩充ua关键字段对应品牌与设备信息方式)
    - [TanX mobile提取](#tanx_mobile提取)
    - [Fynas提取](#fynas提取)
    - [Device Atlas提取](#device-atlas提取)


## 规范化
整理入库数据要规范化书写
- 品牌名称中英文对照表。
- 设备名称中英文对照表。
- 中英文表达规范化。

## 手机市场占有
```
华为、荣耀、小米、vivo、apple、oppo 2019年占有84%。
```
## 数据源

**日志路径**

- TV UA

```
    zzy08, zzy19
    /sas/bs_history/
    安卓盒子的ua
    /sas/tk_history/box_ua_0327.log  zzy19
```

**爬虫资源链接**
- [ShouJi Tenaa](http://shouji.tenaa.com.cn/index.aspx)
    - [根据de=传字符串抓取](http://shouji.tenaa.com.cn/JavaScript/WebStation.aspx?DM=360&type=4&return=ddlSJXH)`spider_tenaa.py`
    - [品牌专区](http://shouji.tenaa.com.cn/Mobile/mobilebrandName.aspx)
- [testin 真机信息](https://www.testin.cn/realmachine/index.htm)
- [fynas](http://www.fynas.com/ua)
- [手机中关村在线](http://detail.zol.com.cn/cell_phone_index/subcate57_1673_list_1.html)
- [手机中国](http://www.cnmo.com/)
    - [手机品牌](http://product.cnmo.com/manu.html)
    - [产品大全](http://product.cnmo.com/all/product.html)
- 手机品牌大全
    - [all brand phone](https://www.gsmarena.com/makers.php3)
    - [all-smartphone-brands](https://www.kimovil.com/en/all-smartphone-brands)
    - [维基百科](https://en.wikipedia.org/wiki/List_of_mobile_phone_makers_by_country)复制数据在`tenaa/phone_maker_country`

**工具**
- [atool获取设备ua](http://www.atool.org/useragent.php)

## 数据格式
最终入库数据格式为：
```
    brand^model^type^recognition_string_1|recognition_string_2|
    // 0-unknown，1-pc, 2-mobile 3-tablet, 4-tv
```

## 提取UA关键字段对应品牌与设备信息方式设备信息

### 工信部手机备案
提取[工信部](http://shouji.tenaa.com.cn/index.aspx)手机厂商。

### testin真机数据抓取

[爬虫](https://git.rtbasia.com/galen/selenium_automatic/blob/master/src/testin_automatic.py)的到数据字段

`name, brand, device, system, resolving_power`

### kimovil网站数据抓取

调用程序`base_spider/spider_kimovil.py`

## 扩充UA关键字段对应品牌与设备信息方式
提取日志信息，过滤获得设备名称。

### Mobile Bidlog
运行[hadoop_tencent](https://git.rtbasia.com/galen/hadoop_tencent)`com.tagphi.hadoop.deviceclassify.MobileBrandApp`程序提取品牌设备信息。

#### 提取清单
- mobile_tanx
    - 201711
    - 201808
- mobile_adgdt
    - 201807

#### 过滤与整理规则
- 剔除空白字符串，多个空白字符串转为一个
- brand含有非数字、字母、中文、`,`、`.`以外的字符
- 含有`\x`字段
- keyword == brand 剔除
- keyword对应多个品牌 剔除
- `brand device in ["unknown","APPLE","Android"]`
- brand长度小于 1 剔除
- 剔除特殊字符串后比较brand 和 device是否有重复
- 构建品牌确定清单，在清单内放行


### Fynas提取
`spider_fynas_ua`爬虫抓取[fynas](http://www.fynas.com/ua)网站

### Device Atlas提取

**处理方式**
- `ua_device_atlas_rtb.py`deviceatlas数据提取后制作成RTB库数据。已废弃。

**TV ua**
```
https://deviceatlas.com/blog/list-smart-tv-user-agent-strings
Apple TV
AppleCoreMedia/1.0.0.12B466 (Apple TV; U; CPU OS 8_1_3 like Mac OS X; en_us)
AppleTV/tvOS/9.1.1
Haystack TV/20 (Apple TV; iOS 10.1; Scale/1.00)

Fire TV
Mozilla/5.0 (Linux; Android 5.1.1; AFTT Build/LVY48F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.10
Dalvik/2.1.0 (Linux; U; Android 5.1; AFTM Build/LMY47O)
Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTM Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30

Samsung Smart TV
Mozilla/5.0 (Linux; Tizen 2.3) AppleWebKit/538.1 (KHTML, like Gecko)Version/2.3 TV Safari/538.1

```


`/Users/wangchun/PycharmProjects/Analysis/user_agent_identyfy/resources/device_ua/device_ua_combine.txt`
`/Users/wangchun/PycharmProjects/Analysis/user_agent_identyfy/resources/ua/ua2device_pattern_20180320.txt`

[deviceatlas账户](https://deviceatlas.com/resources/download-cloud-api/?pi_email=galen.wang%40rtbasia.com)
- 账户：galen wang
- 邮箱：galen.wang@rtbasi.com
- 密码：galen1991

**工具**
- device atlas的库有ua到手机型号的map


Galen@_20180829_