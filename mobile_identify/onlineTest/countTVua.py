import re

class countTVua(object):
    def __init__(self):
        self.TV_dict = {}

    def get_device(self, ua):
        # print ua
        newlist = []
        a = re.findall(r'\((.+?[^;]Build)', ua)
        b = re.findall(r'\((.+?[^;]MIUI)', ua)
        # print a
        # print b
        if len(a) == 0 and len(b) == 0:
            return
        if len(a) != 0 and len(b) == 0:
            datas = a[0].split(';')
            newlist = [d for d in datas if "Build" in d]
        elif len(a) == 0 and len(b) != 0:
            datas = b[0].split(';')
            newlist = [d for d in datas if "MIUI" in d]
        else:
            print
            "有问题的ua{0}".format(ua)
            return None
        TVSpecies = newlist[0].replace('Build', '').replace('MIUI', '').strip(' ')
        # print TVSpecies
        return TVSpecies

    def get_test_ua(self, filename):
        with open(filename, 'r') as file_to_read:
            # n = 0
            while True:
                # while n < 10000000:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                # n += 1
                yield lines

    def TV_in_dict(self, ua):
        if ua is None:
            return
        if self.TV_dict.has_key(ua):
            print
            self.TV_dict[ua]
            self.TV_dict[ua] += 1
        else:
            self.TV_dict.setdefault(ua, 1)
        # 向字典插入元素，setdefault。
        # print self.TV_dict.items()
        return

    def out_put(self, filepath):
        fout = open(filepath, 'w')
        # fout = open("uacount.txt", 'a')
        for (d, x) in self.TV_dict.items():
            print
            "key:" + d + ",value:" + str(x)
            fout.write("%s^%s" % (d, str(x)) + "\n")
        fout.close()

    def main(self, filepath1, filepath2):
        ua_orgs = self.get_test_ua(filepath1)
        for us_org in ua_orgs:
            ua_data = self.get_device(us_org)
            if ua_data is not None:
                self.TV_in_dict(ua_data)
        self.out_put(filepath2)


if __name__ == '__main__':
    # filepath1 = "xiaomi_ua.txt"
    # filepath2 = "xiaomi_ua_conutTest.txt"
    # filepath1 = "needcount.txt"
    filepath1 = "ua_not_match_canbe1.txt"
    filepath2 = "Test_ua_conutTest.txt"
    obj_spider = countTVua()  # 创建
    obj_spider.main(filepath1, filepath2)
    # /Users/wangchun/Documents/Apy/src_data
    # print os.path.abspath("nht_pixel_20170401.log")
    # print os.path.dirname("nht_pixel_20170401.log")
