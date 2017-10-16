# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:48:18 2017

@author: Mark
"""


import scrapy
from pymongo import MongoClient
import re
import json


class ThairathSpider(scrapy.Spider):
    name = "thairath_news"
    #allowed_domains = ['https://www.khaosod.co.th']
    start_urls = ['https://www.thairath.co.th/news/generateviewmore?topic=royal']
    
    def parse(self, response):
        data = json.loads(response.body)
        records = data['arrModel']
        for i in range(len(records)):
            print(records[i]['id'])
        #link_zone = response.selector.xpath('//div[@class="container"]//a')
        #link = link_zone.xpath('@href').extract()
        #use_link = list(set(link))
        #print(use_link)
        #for href in use_link:
        #    yield scrapy.Request(href, self.parse_page)
        #next_page_zone = response.selector.xpath('//div[@class="page-nav td-pb-padding-side"]//a')
        #next_page_list = next_page_zone.xpath('@href').extract()
        #next_page = next_page_list[len(next_page_list)-1]
        #yield scrapy.Request(next_page, self.parse)
        