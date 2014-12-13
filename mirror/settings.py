# -*- coding: utf-8 -*-

# Scrapy settings for mirror project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME         = 'mirror'
SPIDER_MODULES   = ['mirror.spiders']
NEWSPIDER_MODULE = 'mirror.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mirror (+http://www.yourdomain.com)'
USER_AGENT     = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'
ITEM_PIPELINES = [
	'mirror.pipelines.MirrorUnoiqidPipeline',
	# 'mirror.pipelines.MirrorDownloadPipeline',
]