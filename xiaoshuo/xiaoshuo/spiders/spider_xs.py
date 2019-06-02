# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import time
from xiaoshuo.items import XiaoshuoItem
class SpiderXsSpider(scrapy.Spider):
    name = 'spider_xs'
    allowed_domains = ['http://www.biquge.tv/']
    start_urls = ['http://www.biquge.tv/']
    start_url = 'http://www.biquge.tv{}'
    start_page = 1
    story_type_page_1 = 1
    story_type_page_2 = 1
    story_type_page_3 = 1
    story_type_page_4 = 1
    story_type_page_5 = 1
    story_type_page_6 = 1
    def start_requests(self):
        yield scrapy.Request(url = 'http://www.biquge.tv/xuanhuanxiaoshuo/' , callback=self.directory_parse_1,dont_filter=True)
        yield scrapy.Request(url = 'http://www.biquge.tv/xiuzhenxiaoshuo/' , callback=self.directory_parse,dont_filter=True)
        yield scrapy.Request(url = 'http://www.biquge.tv/dushixiaoshuo/' , callback=self.directory_parse,dont_filter=True)
        yield scrapy.Request(url = 'http://www.biquge.tv/chuanyuexiaoshuo/' , callback=self.directory_parse,dont_filter=True)
        yield scrapy.Request(url = 'http://www.biquge.tv/wangyouxiaoshuo/' , callback=self.directory_parse,dont_filter=True)
        yield scrapy.Request(url = 'http://www.biquge.tv/kehuanxiaoshuo/' , callback=self.directory_parse,dont_filter=True)
    def directory_parse(self, response):
        directory = BeautifulSoup(response.text, 'lxml')
        for i in directory.find('div',{'class':'l'}).find('ul').find_all('li'):
            print(i.find('span',{'class':'s2'}).find('a')['href'],i.find('span',{'class':'s2'}).text)
    def directory_parse_1(self, response):
        directory = BeautifulSoup(response.text, 'lxml')
        for i in directory.find('div',{'class':'l'}).find('ul').find_all('li'):
            yield scrapy.Request(url=i.find('span',{'class':'s2'}).find('a')['href'],callback=self.story_directory_parse, dont_filter=True)
            #break
            #print(i.find('span',{'class':'s2'}).find('a')['href'],i.find('span',{'class':'s2'}).text)
        max_page = int(directory.find('a',{'class':'last'}).text)
        self.story_type_page_1 +=1
        if self.story_type_page_1 > max_page:
            pass
        else:
            yield scrapy.Request(url = 'http://www.biquge.tv/xuanhuanxiaoshuo/1_{}.html'.format(str(self.story_type_page_1)) , callback=self.directory_parse_1,dont_filter=True)
            pass
    def story_directory_parse(self, response):
        print(response.url)
        #print(response.text)
        #print(response)
        story_directory = BeautifulSoup(response.text, 'lxml')
        name = story_directory.find('div',{'id':'info'}).find('h1').text
        author = story_directory.find('div',{'id':'info'}).find('p').text
        start = story_directory.find('div',{'id':'list'}).find_all('dd')[9].find('a')['href']
        print(author,name,start)
        request = scrapy.Request(url = 'http://www.biquge.tv{}'.format(start), callback=self.full_text_parse,dont_filter=True)
        request.meta['author'] = author
        print(request.meta['author'])
        #yield scrapy.Request(url = 'http://www.biquge.tv{}'.format(start), callback = lambda response,author=author : self.full_text_parse(response,author),dont_filter=True)

        yield request
    def full_text_parse(self,response):
        html = BeautifulSoup(response.text, 'lxml')
        content = html.find('div',{'id':'content'}).text
        next = html.find('div',{'class':'bottem2'}).find_all('a')[4]['href']
        chapter = html.find('div',{'class':'bookname'}).find('h1').text
        name = html.find('div',{'class':'con_top'}).find_all('a')[1].text
        author = response.meta['author']
        Item =  XiaoshuoItem()
        Item['chapter'] = chapter
        Item['name'] = name
        Item['content'] = content
        Item['author'] = author
        print(Item['author'])
        print(Item['name'])
        print(Item['chapter'])
        print(Item['content'])
        yield Item
        while 1:
            try:
                request = scrapy.Request(url='http://www.biquge.tv{}'.format(next), callback=self.full_text_parse,dont_filter=True)
                request.meta['author'] = author
                yield request
                break
            except:
                pass