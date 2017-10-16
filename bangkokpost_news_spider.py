# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 22:16:33 2017

@author: Mark
"""

import scrapy
from pymongo import MongoClient
import re



class BangkokPostSpider(scrapy.Spider):
    name = "bkkp_news"
    #allowed_domains = ['https://www.khaosod.co.th']
    #start_urls = ['http://www.bangkokpost.com/topstories', 'http://www.bangkokpost.com/news/politics', 'http://www.bangkokpost.com/news/crime', 'http://www.bangkokpost.com/news/general','http://www.bangkokpost.com/news/asean','http://www.bangkokpost.com/news/world', 'http://www.bangkokpost.com/news/sports', 'http://www.bangkokpost.com/news/special-reports', 'http://www.bangkokpost.com/news/security', 'http://www.bangkokpost.com/news/transport' , 'http://www.bangkokpost.com/news/environment']
    start_urls = ['http://www.bangkokpost.com/business/all-article']
    def parse(self, response):

        base_urls = 'http://www.bangkokpost.com'

        link_zone = response.selector.xpath('//div[@class="allStory"]/ul//a')
        print(link_zone)
        link = link_zone.xpath('@href').extract()
        use_link = list(set(link))
        #print(use_link)
        for href in use_link:
            yield scrapy.Request(base_urls + href, self.parse_page)
        #next_page_zone = response.selector.xpath('//div[@class="allStory"]//nav//a[contains(., "Next")]')
        #next_page = next_page_zone.xpath('@href').extract()
        #yield scrapy.Request(base_urls + next_page[0], self.parse)
        
    def parse_page(self, response):
        url = str(response)
        topic = re.findall('\d+', str(url))
        client = MongoClient('localhost', 27017)
        db = client.newsbook
        collections = db.bangkokpostnews
        title = response.xpath('normalize-space(/html/body/section/article/div[1]/header/h1)').extract()
        zone = response.selector.xpath('//div[@class="articleContents"]//img')
        p_zone = response.selector.xpath('//div[@class="articleContents"]//p')
        topic_name = response.xpath('/html/body/section/p/a[2]/span/text()').extract()
        print(topic_name)
        paragraph = p_zone.xpath('text()').extract()
        time = response.xpath('/html/body/section/article/div[1]/header/ul/li[1]/span[1]/text()').extract()
        pictures = zone.xpath('@src').extract()
        for i in range(len(pictures)):
            pictures[i] = 'http://www.bangkokpost.com' + pictures[i]
        check_duplicate = collections.find({"reference_id" : str(topic[1])})
        check = check_duplicate.count()
        if(check > 0):
            print('there is')
        else:
            print('insert to database')
            #dic = {"reference_id" : str(topic[1]), "topic_name" : topic_name[0], "topic" : str(title[0]), "date" : time, "body" : paragraph, "image_url" : pictures}
            #collections.insert_one(dic)
        #print(len(paragraph))
        #print(pictures)
        #print(time)
        #file = open('hello_world.xml', 'w')
        #file.write("hello world")
        #file.close()