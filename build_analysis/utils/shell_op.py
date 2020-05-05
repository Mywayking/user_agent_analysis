"""
-------------------------------------------------
   Author :       galen
   date：          2018/4/19
-------------------------------------------------
   Description:
-------------------------------------------------
"""
import os


def deduplication_data(data_path):
    """数据shell命令去重"""
    command = "awk '!a[$0]++' {0}|sort -o {1}".format(data_path, data_path)
    print(command)
    os.system(command)


def sort_data(data_path):
    """数据shell命令排序"""
    command = "sort -n  -r -t$'\t' -k 2 {0} -o {1}".format(data_path, data_path)
    print(command)
    os.system(command)


def delete_existed_file(path):
    """删除已存在文件"""
    if os.path.exists(path):
        print("删除已存在文件夹:{}".format(path))
        os.remove(path)
    else:
        print("不存在文件夹:{}".format(path))
