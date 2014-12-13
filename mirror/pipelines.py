# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.exceptions import DropItem

from mirror import BloomFilter,SimpleHash

urls = BloomFilter()

# 链接去重
class MirrorUnoiqidPipeline(object):
    def process_item(self, item, spider):
    	item['item'] = item['item'].split('?')[0].split('#')[0]
    	if not urls.has(item['item']):
        	urls.add(item['item'])
        	open('items.lst','a').write(item['item']+'\n')
        	return item
        else:
        	raise DropItem("Item contains no biaomodel")

# # 下载资源，html，css，img，js 等
# class MirrorDownloadPipeline(FilesPipeline):

#     def get_media_requests(self, item, info):
#         if item.get('item'):
#             yield Request(item['item'])

#     def item_completed(self, results, item, info):
#         paths = [x['path'] for ok, x in results if ok]

#         if not paths:
#             raise DropItem("Item contains no paths")

#         # 移动文件        
#         # 移动文件
#         if not os.path.exists(os.path.join(PDFS_STORE)):
#             os.mkdir(os.path.join(PDFS_STORE))

#         if not os.path.exists(os.path.join(PDFS_STORE, item.get('brand'))):
#             os.mkdir(os.path.join(PDFS_STORE, item.get('brand')))
        
#         pdf = item.get('model') + '.pdf'
#         src = os.path.join(FILES_STORE, paths[0])
#         dst = os.path.join(PDFS_STORE, item.get('brand'), pdf)

#         shutil.copyfile(src, dst)

#         return item        