
BOT_NAME = "datamining"

SPIDER_MODULES = ["datamining.spiders"]
NEWSPIDER_MODULE = "datamining.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
}


PROXY = 'http://brd-customer-hl_79cc5ce7-zone-isp_proxy_new_group_9:icse3v3b3sdp@brd.superproxy.io:22225'

import scrapy
import sys
# Configure the proxy in the spider
if sys.version_info[0] == 2:
    import six
    from six.moves.urllib import request
    opener = request.build_opener(
        request.ProxyHandler({'http': PROXY, 'https': PROXY})
    )
elif sys.version_info[0] == 3:
    import urllib.request
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
    )

# Use the opener to make requests in your spider
def make_request(self, url):
    if sys.version_info[0] == 2:
        response = opener.open(url)
        return scrapy.http.HtmlResponse(
            url=url, body=response.read(), encoding='utf-8'
        )
    elif sys.version_info[0] == 3:
        with opener.open(url) as response:
            return scrapy.http.HtmlResponse(
                url=url, body=response.read(), encoding='utf-8'
            )
