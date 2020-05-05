# coding=utf-8
from collections import OrderedDict



def get_data(filepath):
    with open(filepath, 'rU') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            lines = lines.strip('\n')
            if not lines:
                break
            yield lines


def load_dict_precise():
    # 读入数据ua2deviceprecise.txt
    filepath_precise = "ua2device_precise.txt"
    data_dict_precise = {}
    for data in get_data(filepath_precise):
        PRECISE_data = data.split('^')
        # device = (PRECISE_data[0],PRECISE_data[1],PRECISE_data[2])
        if PRECISE_data[3] is not None:
            preciseKeywords = PRECISE_data[3].split('|')
            for kw in preciseKeywords:
                data_dict_precise[kw.upper()] = 0
    return data_dict_precise


def load_dict_order_precise():
    # 读入数据ua2deviceprecise.txt
    filepath_order_precise = "ua_device_count.txt"
    data_dict_order_precise = {}
    for data in get_data(filepath_order_precise):
        order_data = data.split('^')
        # device = (PRECISE_data[0],PRECISE_data[1],PRECISE_data[2])
        data_dict_order_precise[order_data[0].upper()] = order_data[1]
    return data_dict_order_precise


def order_dict_precise():
    # 读入数据ua2deviceprecise.txt
    data_dict_order_precise = load_dict_order_precise()
    filepath_precise = "ua2device_precise.txt"
    data_dict_precise = {}
    for data in get_data(filepath_precise):
        PRECISE_data = data.split('^')
        # device = (PRECISE_data[0],PRECISE_data[1],PRECISE_data[2])
        if PRECISE_data[3] is not None:
            preciseKeywords = PRECISE_data[3].split('|')
            value = 0
            for kw in preciseKeywords:
                if data_dict_order_precise.has_key(kw):
                    value = value + int(data_dict_order_precise[kw])
            data_dict_precise[data] = value
    return dict_order(data_dict_precise)


def dict_order(dict_data):
    data_dict_order = OrderedDict()
    dict_data = sorted(dict_data.iteritems(), key=lambda asd: asd[1], reverse=True)
    for data in dict_data:
        data_dict_order[data[0]] = data[1]
    return data_dict_order


def out_put_data(data):
    fout = open("ua2device_precise_order.txt", "w")
    data_order = sorted(data.iteritems(), key=lambda asd: asd[1], reverse=True)
    for value in data_order:
        fout.write("{0}".format(value[0]) + "\n")
    fout.close()
    return


if __name__ == '__main__':
    # main()
    out_put_data(order_dict_precise())
