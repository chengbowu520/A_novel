# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
class BiqukanPipeline(object):
    def process_item(self, item, spider):
        # 爬取的数据保存的位置
        curPath = "G:/小说"
        # 获取小说的名字
        tempPath = str(item['name'])
        # 拼接 将位置 + 分隔符 + 小说的名字
        targetPath = curPath + os.path.sep + tempPath
        # 判断当前位置是否存在
        if not os.path.exists(targetPath):
            # 不存在就创建文件夹
            os.makedirs(targetPath)
        # 将章节保存在对应的文件夹下
        filename_path = "G:/小说" + os.path.sep + str(item['name']) + os.path.sep + str(item['chapter_name']) + ".txt"
        with open(filename_path,'w',encoding="utf-8") as f:
            # 将获取的文本内容写入到txt文档中
            f.write(item['content']+"\n")
            f.close()
        return item