# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:37:47 2018

@author: Mark
"""

import scrapy
from pymongo import MongoClient
import re
from scrapy.exceptions import CloseSpider
import sys


close = 0
class PantipSpider(scrapy.Spider):
    name = "pantip"
    close_down = 'hello'
    #allowed_domains = ['https://www.khaosod.co.th']
    start_urls = ['https://pantip.com']
    #start_urls = ['https://www.bangkokpost.com/tech/all-article/page-1581/']
    #response = HtmlResponse(url='http://example.com', body=body)
    def parse(self, response):
        base_urls = 'https://pantip.com/topic/'
        client = MongoClient('localhost', 27017)
        db = client.newsbook
        collections = db.pantip
        reference_id = collections.find_one(sort=[("reference_id", -1)])
        print(reference_id['reference_id'])
        news_id = 30000000

        for i in range(news_id,news_id+7444655):#news_id+7444655):
            yield scrapy.Request(base_urls + str(i), self.parse_page)

    def parse_page(self, response):
        global close
        url = str(response)
        print(url)
        reference_id = re.findall('\d+', str(url))
        client = MongoClient('localhost', 27017)
        db = client.newsbook
        collections = db.pantip  #don't forget to change
        check_empty2 = response.selector.xpath('//div[@class="content"]//div[@class="container-outer"]//div[@class="container-inner"]//div[@class="callback-status"]')
        check_empty = response.selector.xpath('//div[@class="content"]//div[@class="container-outer"]//div[@class="container-inner"]//div[contains(@class, "callback-status") or contains(@class, "alone")]')
        sentence = check_empty.xpath('text()').extract()
        sentence2 = check_empty2.xpath('//strong/text()').extract()
        #print(sentence)
        #print(sentence2)
        if(sentence or sentence2):
            #print(sentence)
            print("oh noooo")
        else:
            type_tag = response.selector.xpath('//div[@class="display-post-status-leftside"]//div[contains(@class, "display-post-favourite") and contains(@class, "remark-four-txt")]//span')
            tag = type_tag.xpath('text()').extract()
            if(len(tag)> 1):
                newstype = "".join(tag[1].split())
            else:
                newstype = "".join(tag[0].split())
            #print("newstype", newstype)    
            check_duplicate = collections.find({"reference_id" : str(reference_id[1])})
            check = check_duplicate.count()
            if(newstype == "กระทู้ข่าว"):
                print("newstype")
                if(check > 0):
                    print('there is')
                else:
                    header_tag = response.selector.xpath('//div[@class="display-post-status-leftside"]//h2[@class="display-post-title"]')
                    time_tag = response.selector.xpath('//div[@class="edit-history"]//abbr')
                    video_tag = response.selector.xpath('//div[@class="display-post-story"]//a[@class="video_id"]')
                    img_tag = response.selector.xpath('//div[@class="display-post-story"]//img[@class="img-in-post"]')
                    text_tag = response.selector.xpath('//div[@class="display-post-story"]')
                    video = video_tag.xpath('@href').extract()
                    img = img_tag.xpath('@src').extract()
                    text = text_tag.xpath('text()').extract()
                    title = header_tag.xpath('text()').extract()
                    time = time_tag.xpath('@data-utime').extract()
                    if(len(time)>0):
                        pass
                    else:
                        time_tag = response.selector.xpath('//div[@class="display-post-story-footer"]//div[@class="display-post-avatar-inner"]//span[@class="display-post-timestamp"]//abbr[@class="timeago"]')
                        time = time_tag.xpath('@data-utime').extract()
                    #print(time)
                    print('insert to database')
                    dic = {"reference_id" : str(reference_id[1]),
                           "topic_name" : None,
                           "topic" : str(title[0]),
                           "date" : time[0],
                           "body" : text,
                           "image_url" : img,
                           "video_url" : video,
                           "publisher" : "pantip"}
                    collections.insert_one(dic)
                
                #time = response.xpath('//*[@id="topic-'+ str(reference_id[1]) +'"]/div/div[4]/div[1]/div/div/em/abbr/@data-utime').extract()
                #print(title)
                #print(video)
                #print(img)
                #print(text)
                #print(reference_id[1])
                #print(time)

                
        #title = response.xpath('normalize-space(//div[@class="cXenseParse"]//h1)').extract()
        #check = str(title)
        #if(len(check) > 4):
         #   print("")
         #   zone = response.selector.xpath('//div[@class="cXenseParse"]//img')
         #   p_zone = response.selector.xpath('//div[@class="cXenseParse"]//p')
         #   topic_name = response.xpath('normalize-space(//p[@class="levelNavigaton"]//a/text())').extract()
         #   paragraph = p_zone.xpath('text()').extract()
         #   time = response.xpath('/html/body/section/article/div[1]/header/ul/li[1]/span[1]/text()').extract()
         #   pictures = zone.xpath('@src').extract()
         #   if(len(pictures) > 0):
         #       for i in range(len(pictures)):
         #           pictures[i] = 'http://www.bangkokpost.com' + pictures[i]
         #   check_duplicate = collections.find({"reference_id" : str(topic[1])})
         #   check = check_duplicate.count()
            #print(topic)
            #print(topic[1])
            #print(title)
            #print(topic_name)
            #print(paragraph)
            #print(time)
            #print(pictures)
            #if(check > 0):
               # print('there is')
            #else:
             #   print('insert to database')
              #  dic = {"reference_id" : str(topic[1]), "topic_name" : topic_name[0], "topic" : str(title[0]), "date" : time, "body" : paragraph, "image_url" : pictures}
               # collections.insert_one(dic)
        #else:
         #   title = response.xpath('normalize-space(//*[@id="headergroup"]/h2)').extract()
          #  zone = response.selector.xpath('//div[@class="entry"]//img')
           # topic_name = response.xpath('//*[@id="content"]/p/a/text()').extract()
            #paragraph = response.xpath('//*[@id="content"]/div[1]/p/text()').extract()
            #time = response.xpath('//*[@id="headergroup"]/p[1]/text()').extract()
            #pictures = zone.xpath('@src').extract()
            #if(len(pictures) > 0):
            #    for i in range(len(pictures)):
            #        pictures[i] = 'http://www.bangkokpost.com' + pictures[i]
            #check_duplicate = collections.find({"reference_id" : str(topic[1])})
            #check = check_duplicate.count()
            #print(topic[len(topic)-1])
            #print(title)
            #print(topic_name)
            #print(paragraph)
            #print(time)
            #print(pictures)
            
            #if(check > 0):
             #   print('there is')
            #else:
             #   print('insert to database')
             #   dic = {"reference_id" : str(topic[1]), "topic_name" : topic_name[0], "topic" : str(title[0]), "date" : time, "body" : paragraph, "image_url" : pictures}
             #   collections.insert_one(dic)
        #print(len(paragraph))
        #print(pictures)
        #print(time)
        #file = open('hello_world.xml', 'w')
        #file.write("hello world")
        #file.close()