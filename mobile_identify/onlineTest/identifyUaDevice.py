import countTVua
import logging
from collections import OrderedDict

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    # datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')


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
    filepath_pattern = "ua2device_pattern.txt"
    data_dict_precise = {}
    data_dict_pattern = OrderedDict()
    for data in get_data(filepath_precise):
        device = ()
        PRECISE_data = data.split('^')
        device = (PRECISE_data[0], PRECISE_data[1], PRECISE_data[2])
        if PRECISE_data[3] is not None:
            preciseKeywords = PRECISE_data[3].split('|')
            for kw in preciseKeywords:
                data_dict_precise[kw] = device
    for data in get_data(filepath_pattern):
        device = ()
        PATTERN_data = data.split('^')
        device = (PATTERN_data[0], PATTERN_data[1], PATTERN_data[2])
        if PATTERN_data[3] is not None:
            patternKeywords = PATTERN_data[3].split('|')
            for kw in patternKeywords:
                data_dict_pattern[kw] = device
    return data_dict_precise, data_dict_pattern


def device_model_detect(ua):
    data_dict_precise, data_dict_pattern = load_dict_precise()
    for prk in data_dict_precise.keys():
        if prk.lower() in ua.lower().replace("+", " "):
            return True
    for pak in data_dict_pattern.keys():
        if pak.lower() in ua.lower().replace("+", " "):
            # print "pattern_ua----------",ua
            # print data_dict_pattern[pak]
            logging.info(ua)
            return True
    return False


def detect_many_ua():
    # filepath = "/home/galen/nht_pixel_2017071000.log"
    # filepath ="100.txt"
    filepath = "ua_not_match_canbe.txt"
    # filename= raw_input_A = raw_input("filename: ")
    # filepath =os.path.dirname(os.path.dirname(os.path.abspath("identifyUaDevice.py")))+"/"+filename
    print
    filepath
    count = 0
    count_match = 0
    count_not_match = 0
    conunt_pc = 0
    conunt_other = 0
    for data in get_data(filepath):
        count += 1
        if "build" in data or "linux" in data or "android" or "iphone" or "ipad" in data.lower():
            if device_model_detect(data) == True:
                count_match += 1
            else:
                count_not_match += 1
                out_put_datass(data)
        else:
            if "Windows" in data or "Macintosh" in data:
                conunt_pc += 1
                out_put_datas()
            else:
                conunt_other += 1
                # print "pc占比：",1-float(conunt_pc)/float(count)
        if count % 100 == 0:
            print
            "占总匹配率：", float(count_match) / float(count)
            print
            "pc占比：", float(conunt_pc) / float(count)
            print
            "占手机ua匹配率", float(count_match) / (float(count_match) + float(count_not_match))
            print
            "匹配个数{0}；pc端UA个数{1}；其他种类个数{2}；总ua数{3}".format(count_match, conunt_pc, conunt_other, count)
    print
    "匹配个数{0}；pc端UA个数{1}；其他种类个数{2}；总ua数{3}".format(count_match, conunt_pc, conunt_other, count)
    return


def out_put_datass(data):
    fout = open("ua_not_match_canbe1.txt", "a")
    fout.write("%s" % data + "\n")
    fout.close()
    return


def out_put_datas(data):
    fout = open("ua_pc.txt", "a")
    fout.write("%s" % data + "\n")
    fout.close()
    return


def main():
    detect_many_ua()
    obj_count = countTVua.countTVua()
    obj_count.main("ua_not_match_canbe1.txt", "Test_ua_conutTest.txt")
    return


if __name__ == '__main__':
    # logging.debug('This is debug message')
    # logging.info('This is info message')
    # logging.warning('This is warning message')
    main()
