import urllib


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        req = urllib.Request(url, headers=headers)
        try:
            response = urllib.urlopen(req)
        except urllib.URLError as e:
            print(e.reason)
            return None
        return response.read()

        # response = urllib2.urlopen(url)

        # if response.getcode() != 200:
        #     return None

        # return response.read()
