# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 22:16:33 2017

@author: Mark
"""

import scrapy
from pymongo import MongoClient
from scrapy.spider import BaseSpider
from scrapy import Selector
import re


class QuotesSpider(scrapy.Spider):
    name = "crawls_news"
    #allowed_domains = ['https://www.khaosod.co.th']
    start_urls = ['https://www.khaosod.co.th/breaking-news', 'https://www.khaosod.co.th/special-stories', 'https://www.khaosod.co.th/hot-topics', 'https://www.khaosod.co.th/around-thailand', 'https://www.khaosod.co.th/around-the-world-news', 'https://www.khaosod.co.th/entertainment', 'https://www.khaosod.co.th/politics', 'https://www.khaosod.co.th/economics', 'https://www.khaosod.co.th/sports', 'https://www.khaosod.co.th/newspaper-column', 'https://www.khaosod.co.th/clips', 'https://www.khaosod.co.th/monitor-news', 'https://www.khaosod.co.th/lifestyle','https://www.khaosod.co.th/social-trend', 'https://www.khaosod.co.th/car-vehicle', 'https://www.khaosod.co.th/sci-tech', 'https://www.khaosod.co.th/amulets', 'https://www.khaosod.co.th/tv-guide']
    
    def parse(self, response):
        link_zone = response.selector.xpath('//div[@class="ud_loop_inner"]//a')
        link = link_zone.xpath('@href').extract()
        use_link = list(set(link))
        print(use_link)
        for href in use_link:
            yield scrapy.Request(href, self.parse_page)
        next_page_zone = response.selector.xpath('//div[@class="page-nav td-pb-padding-side"]//a')
        next_page_list = next_page_zone.xpath('@href').extract()
        next_page = next_page_list[len(next_page_list)-1]
        yield scrapy.Request(next_page, self.parse)
        
    def parse_page(self, response):
        #print("hello world")
        url = str(response)
        token_topic = url.split('_')
        topic=token_topic[len(token_topic)-1]
        topic = re.findall('\d+', str(topic))
        #print(topic)
        #print(url)
        client = MongoClient('localhost', 27017)
        db = client.test
        collections = db.news
        title = response.xpath('//*[@id="post-' + str(topic[0]) +'"]/div[2]/div[1]/header/h1/text()').extract()
        time_zone = response.selector.xpath('//div[@class="td-module-meta-info"]//time')
        zone = response.selector.xpath('//div[@class="td-post-content"]//img')
        p_zone = response.selector.xpath('//div[@class="td-post-content"]//p')
        paragraph = p_zone.xpath('text()').extract()
        time = time_zone.xpath('@datetime').extract()[0]
        pictures = zone.xpath('@src').extract()
        #print(topic[0])
        #print(type(title))
        #print(type(paragraph))
        #print(time)
        #print(pictures)
        check_duplicate = collections.find({"reference_id" : str(topic[0])})
        check = check_duplicate.count()
        if(check > 0):
            print('there is')
        else:
            print('insert to database')
            dic = {"reference_id" : str(topic[0]), "topic" : str(title[0]), "date" : time, "body" : paragraph, "image_url" : pictures}
            collections.insert_one(dic)
        #print(len(paragraph))
        #print(pictures)
        #print(time)
        #file = open('hello_world.xml', 'w')
        #file.write("hello world")
        #file.close()