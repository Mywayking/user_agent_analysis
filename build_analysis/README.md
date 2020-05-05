# User Agent Build分析

**任务**

再给我一个出现的次数。
并且跟[代号、标签和版本号]( https://source.android.com/setup/start/build-numbers)里面的Build做一个比对。如果出现在列表中的，后面做个标记。


## 原始数据
- zzy19 /sas/bs_history/ 目录下20180417一天日志的ua的build字段。
    - 分隔符 sep: "\001"
    - ua 为第四个
- [build-numbers](https://source.android.com/setup/start/build-numbers)

## 工作流程
- 通过`spider_build.py`抓取[build-numbers](https://source.android.com/setup/start/build-numbers) 获得build字符串.
- 清洗日志build `parse_build.py`,生成`android_build.txt`和`build_list.txt`,前者为官网build匹配