# UserAgent_Verificaiton 查询ua所属手机型号

**get**

`https://api.rtbasia.com/*************?ua=[IP]&key=[KEY]`

Parameter

| Field        | Type    |  Description  |
| --------   | :-----:   | :---- |
| ua        | String      |   查询的UA,如：Mozilla/5.0 (Linux; Android 5.1.1; vivo Xplay5A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 |
| key        | String      |   ODX查询客户提供的唯一编号（请向客服代表申请）。每个key都有预设的每日请求总量和接口权限    |


Success 200

| Field        | Type    |  Description  |
| --------   | :-----:   | :---- |
| brand        | String      |   返回的品牌名 |
| model        | String      |   设备型号    |
| type        | int      |   设备种类, 0-unknown，1-pc, 2-mobile 3-tablet, 4-tv |

Success-Response
```
{
  "brand": "Vivo",
  "model": "vivo Xplay5A",
  "type": 2
}
```

Error 4xx

| Name        | Description|
| --------   | :-----:   |
| error	| 错误信息      |

**Error-Response 非法参数:**
```
HTTP/1.1 200 OK
{
  "error": "Invalid Parameter"
}
```

**Error-Response 权限验证失败:**
```
HTTP/1.1 200 OK
{
  "error": "Permisson Denied"
}
```