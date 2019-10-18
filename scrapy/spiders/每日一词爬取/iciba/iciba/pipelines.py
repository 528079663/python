# -*- coding: utf-8 -*-

import os

from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings


class IcibaPipeline(object):
    # 初始化创建文件的编码格式  名称 操作关键字 字符集
    def process_item(self, item, spider):
        content = item['content']
        title = item['title']
        note = item['note']
        translation = item['translation']
        file = open('spider_result.txt', 'a+', encoding='utf-8')
        file.write('title' + title + '\n')
        file.write('content: ' + content + '\n')
        file.write('note: ' + note + '\n')
        file.write('translation：' + translation + '\n')
        return item


class MyImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        yield Request(item['picture'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        os.rename(self.IMAGES_STORE + '\\' + image_paths[0].replace('/', '\\'),
                  self.IMAGES_STORE + '\\full\\' + item["title"] + ".jpg")
        # item['image_paths'] = self.IMAGES_STORE + '\\full\\' + item["last_title"]
        return item
