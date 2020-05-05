# -*- coding: UTF-8 -*-   
import re
import urlparse
from bs4 import BeautifulSoup


# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class HtmlParser(object):
    def __init__(self):
        self.page_url = "http://www.fynas.com"

    def parse_urls(self, html_cont):
        if html_cont is None:
            return
        new_urls = set()
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        links = soup.find_all('a', href=re.compile(r"/ua/search\?b=&d="))
        # page_url="http://www.fynas.com"
        for link in links:
            new_url = link['href'].encode('utf-8')
            # print new_url
            new_full_url = urlparse.urljoin(self.page_url, new_url)
            print
            new_full_url
            new_urls.add(new_full_url)
        return new_urls

    def parse(self, phone_urls, html_cont):
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        next_urls = self._next_new_urls(soup)
        new_data = self._get_new_data(phone_urls, soup)
        return next_urls, new_data

    def _next_new_urls(self, soup):
        # next_urls = set()
        # /view/123.htm
        # page_url="http://www.fynas.com"
        try:
            x = soup.find('a', string=re.compile(u"下页"))
            link = x['href'].encode('utf-8')
            next_urls = urlparse.urljoin(self.page_url, link)
            # print next_urls
            return next_urls
        except:
            return 1
        #     # new_urls=1
        return next_urls

    def _get_new_data(self, phone_urls, soup):
        # res_data = {}
        data = []
        s = re.findall(r"http:\/\/www\.fynas\.com\/ua\/search\?b=&d=(.*)", phone_urls)
        print
        s
        if s[0] == '华为' or s[0] == '荣耀':
            co = "Huawei"
        elif s[0] == '小米' or s[0] == '红米':
            co = "Xiaomi"
        elif s[0] == '三星':
            co = "Samsung"
        elif s[0] == '魅族':
            co = "Meizu"
        elif s[0] == 'OPPO' or s[0] == 'vivo':
            co = "OPPO"
        elif s[0] == '锤子':
            co = "Smartisan"
        elif s[0] == 'iphone':
            co = "Apple"
        # print res_data['company']
        # soup = BeautifulSoup(html_doct,'html.parser', from_encoding='utf-8')
        trs = soup.find_all('tr')
        for i in range(1, len(trs)):
            # print trs[i]
            res_data = {}
            res_data['company'] = co
            tds = trs[i].find_all('td')
            # print tds
            res_data['mobile'] = tds[0].string.strip()
            res_data['OS'] = tds[1].string.strip()
            res_data['browser'] = tds[2].string.strip()
            # get_text()
            res_data['UserAgent'] = tds[3].string.strip()
            data.append(res_data)

        return data
