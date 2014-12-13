# -*- coding: utf-8 -*-
from scraper.settings import USER_AGENT_LIST
from scrapy import log

import random

class ProxyMiddleware(object):

    proxy_list = []

    def __init__ (self):
        for p in open('proxy.txt'):
            p = p.strip().split(',')
            proxy = '%s://%s:%s/' % (p[0].lower(), p[1], p[2])
            self.proxy_list.append(proxy)

    def process_request(self, request, spider):

        try:
            proxy = random.choice(self.proxy_list)

            if proxy:
                request.meta['proxy'] = proxy
        except Exception,e:
            print 'proxy', e
            log.msg(e,level = log.ERROR)


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        
        if ua:
            request.headers.setdefault('User-Agent', ua)
        
        log.msg('>>>> UA %s'%request.headers)            