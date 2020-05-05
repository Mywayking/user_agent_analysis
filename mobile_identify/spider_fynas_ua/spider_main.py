# coding=utf-8
import url_manager, html_downloader, html_parser, html_outputer
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()  # url管理器
        self.downloader = html_downloader.HtmlDownloader()  # 下载器
        self.parser = html_parser.HtmlParser()  # 解析器
        self.outputer = html_outputer.HtmlOutputer()  # 输出器

    def craw(self, root_url):
        count = 1  # 判断当前爬取的是第几个url
        incount = 1
        html_cont = self.downloader.download(root_url)
        phone_urls = self.parser.parse_urls(html_cont)
        self.urls.add_new_urls(phone_urls)
        while self.urls.has_new_url():  # 循环,爬取所有相关页面,判断异常情况
            #     try:·
            phone_urls = self.urls.get_new_url()  # 取得url
            print
            '爬取 %d : %s' % (count, phone_urls)  # 打印当前是第几个url
            next_urls = self.crawindeep(phone_urls, phone_urls)
            # html_cont = self.downloader.download(new_url)   #下载页面数据
            # next_urls, new_data = self.parser.parse(new_url,html_cont)    #进行页面解析得到新的url以及数据
            # self.outputer.output_html(new_data)
            print
            next_urls
            while next_urls is not None:
                if next_urls == 1:
                    break
                next_urls = self.crawindeep(next_urls, phone_urls)
                if incount == 200000:
                    break
                incount = incount + 1
            if count == 200000:
                break
            count = count + 1

        # self.outputer.output_html()   #利用outputer输出收集好的数据

    def crawindeep(self, next_url, phone_urls):
        self.outputer.output_url(next_url)
        html_cont = self.downloader.download(next_url)  # 下载页面数据
        next_urls, new_data = self.parser.parse(phone_urls, html_cont)
        print
        next_urls, new_data
        self.outputer.output_html(new_data)
        return next_urls


if __name__ == "__main__":
    root_url = "http://www.fynas.com/ua/search?d=&b=&k=&page=1"
    obj_spider = SpiderMain()  # 创建
    obj_spider.craw(root_url)  # craw方法启动爬虫
