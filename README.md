# A_novel
爬取全站笔趣看小说
第一步：
爬取的url：“https://www.biqukan.com”
第二步：
创建项目，修改items中的参数
from scrapy import Item,Field
class BiqukanItem(Item):
    # 小说
    name = Field()
    # 章节名字
    chapter_name = Field()
    # 内容
    content = Field()


def parse(self, response):
    # 获取小说类型
    types = response.xpath("//div[@class='nav']//li")[2:]
    for book_type in types:
        type_url = book_type.xpath("./a/@href").extract_first()
        yield scrapy.Request(url=response.urljoin(type_url),callback=self.type_url)

第三步：
获取每个分类后，获取里面所有的小说
def type_url(self,response):
    # 热门小说
    hot_book = response.xpath("//div[@class='hot bd']//div[@class='item']")
    for hot in hot_book:
        book_url = hot.xpath("./div[@class='p10']/dl/dt/a/@href").extract_first()
        yield scrapy.Request(url=response.urljoin(book_url),callback=self.book_url)

    # 好看的小说
    # nice_book = response.xpath("//div[@class='up']//li")
    # for nice in nice_book:
    #     nice_url = nice.xpath("./span[@class='s2']/a/@href").extract_first()
    #     yield scrapy.Request(url=response.urljoin(nice_url),callback=self.book_url)

第四步：
获取每本小说之后，进入小说，获取当中每个章节的url
def book_url(self,response):
    chapters = response.xpath("//div[@class='listmain']//dd")[13:]
    for chapter in chapters:
        chapter_url = chapter.xpath("./a/@href").extract_first()
        yield scrapy.Request(url=response.urljoin(chapter_url),callback=self.text_url)

第五步：
进入章节后，获取小说的名字，章节名称，小说文本
def text_url(self,response):
    item = BiqukanItem()
    item["name"] = response.xpath("//div[@class='p']/a[2]/text()").extract_first()
    item["chapter_name"] = response.xpath("//div[@class='content']/h1/text()").extract_first()
    item["content"] = '\n'.join(response.xpath('//*[@id="content"]/text()').extract())
    yield item

第六步：
编写pipelines，用来保存爬取下来的小说，存储为txt格式
import os
class BiqukanPipeline(object):
    def process_item(self, item, spider):
        # 爬取的数据保存的位置
        curPath = "G:/小说"
        # 获取小说的名字
        tempPath = str(item['name'])
        # 将保存的目录 + 分隔符 + 小说的名字
        targetPath = curPath + os.path.sep + tempPath
        # 判断是否存在
        if not os.path.exists(targetPath):
            # 创建文件夹
            os.makedirs(targetPath)
        # 章节需要保存的路径    
        filename_path = "G:/小说" + os.path.sep + str(item['name']) + os.path.sep + str(item['chapter_name']) + ".txt"
        with open(filename_path,'w',encoding="utf-8") as f:
            # 将爬取的content写入txt文档中
            f.write(item['content']+"\n")
            f.close()
        return item
