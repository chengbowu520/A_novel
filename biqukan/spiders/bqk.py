# -*- coding: utf-8 -*-
import scrapy,re
from biqukan.items import BiqukanItem


class BqkSpider(scrapy.Spider):
    name = 'bqk'
    allowed_domains = ['biqukan.com']
    start_urls = ['http://biqukan.com/']

    # 解析主页 获取所有类型的小说
    def parse(self, response):
        # 获取小说类型
        types = response.xpath("//div[@class='nav']//li")[2:]
        for book_type in types:
            type_url = book_type.xpath("./a/@href").extract_first()
            yield scrapy.Request(url=response.urljoin(type_url),callback=self.type_url)



    # 类型小说 解析获取每本小说的详细页
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

    # 获取每一本小说的详细页
    def book_url(self,response):
        # 小说题目
        title = response.xpath("//div[@class='info']/h2/text()").extract_first()
        lists = response.xpath('//div[@class="small"]//span/text()').extract()
        # 作者
        author = lists[0]
        # 分类
        classification = lists[1]
        # 状态
        state = lists[2]
        # 字数
        words = lists[3]
        # 更新时间
        Update_time = lists[4]
        # 获取每个章节的详细页
        chapters = response.xpath("//div[@class='listmain']//dd")[13:]
        for chapter in chapters:
            chapter_url = chapter.xpath("./a/@href").extract_first()
            yield scrapy.Request(url=response.urljoin(chapter_url),callback=self.text_url)


    # 每个章节的详细页
    def text_url(self,response):
        item = BiqukanItem()
        item["name"] = response.xpath("//div[@class='p']/a[2]/text()").extract_first()
        item["chapter_name"] = response.xpath("//div[@class='content']/h1/text()").extract_first()
        item["content"] = '\n'.join(response.xpath('//*[@id="content"]/text()').extract())
        yield item