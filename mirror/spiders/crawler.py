# -*- coding: utf-8 -*-
from scrapy.utils.url import urljoin_rfc, url_has_any_extension
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.response import get_base_url
from scrapy.http import Request,FormRequest
from mirror.items import MirrorItem

import scrapy

class CrawlerSpider(scrapy.Spider):
    allowed_domains = []
    allowed_types   = ['.css','.js','.png','.gif','.jpg']
    start_urls      = []
    name            = "crawler"

    def __init__(self, url = None, allow = None, domain = None, path = None, conf = None):
        self.allowed_domains = [domain] if url else self.allowed_domains
        self.allowed_types   = [allow] if url else self.allowed_types
        self.start_urls      = (url,) if url else self.start_urls
        
        if conf:
            for x in open(conf):
                self.start_urls.append(x)


    def parse(self, response):
        base = get_base_url(response)
        for url in response.xpath('//a/@href'):
            url = url.extract()
            if (url != '#') and (not 'javascript:' in url):
                yield Request(url=urljoin_rfc(base, url), callback=self.parseItem)


    # # 分析里面的css，js，img
    def parseItem(self, response):
        base = get_base_url(response)       
        item = MirrorItem()
        meta = {}

        item['item'] = response.url
        yield item

        for img in response.xpath('//img/@src'):
            img = urljoin_rfc(base, img.extract())
            item['item'] = img
            yield item

        for js in response.xpath('//script/@src'):
            js = urljoin_rfc(base, js.extract())
            item['item'] = js
            yield item

        for css in response.xpath('//link/@href'):
            if url_has_any_extension(css.extract(), '.css'):
                css = urljoin_rfc(base, css.extract())
                yield Request(url=css, meta=meta, callback=self.parseStyle)
            else:
                item['item'] = css
                yield item


    def parseStyle(self, response):
        base = get_base_url(response)
        item = MirrorItem()
        meta = {}

        item['item'] = response.url
        yield item

        if response.selector.re('url\((.*?)\)'):
            for src in response.selector.re('url\((.*?)\)'):
                src = src.strip("'").strip('"')
                if not 'data:' in src:
                    src = urljoin_rfc(base, src)
                    if url_has_any_extension(src, '.css'):
                        yield Request(url=src, meta=meta, callback=self.parseStyle)
                    else:
                        item['item'] = src
                        yield item

