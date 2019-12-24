# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class BiqukanItem(Item):
    # 小说
    name = Field()
    # 章节名字
    chapter_name = Field()
    # 内容
    content = Field()
