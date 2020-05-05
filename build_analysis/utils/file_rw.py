"""
-------------------------------------------------
   Author :       galen
   date：          2018/4/19
-------------------------------------------------
   Description:
-------------------------------------------------
"""


def read_txt(filename, model="r"):
    """读取文件"""
    with open(filename, model, encoding='UTF-8', errors='ignore') as f:
        while True:
            lines = f.readline().strip('\n')
            if not lines:
                break
            yield lines


def reads_txt(filename, model="r"):
    """读取整个文件"""
    with open(filename, model, encoding='UTF-8', errors='ignore') as f:
        return f.read().splitlines()


def save_to_data_file(data, filename, mode="a"):
    """保存文件"""
    with open(filename, mode)as f:
        f.write(data)


def save_to_datas_file(data_list, filename, mode="a"):
    """保存文件"""
    with open(filename, mode)as f:
        for data in data_list:
            f.write(data + "\n")
