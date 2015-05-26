import logging
_logger = logging.getLogger(__name__)

import scrapy

class KickassSpider(scrapy.spider.Spider):
    
    name = 'kickass'
    allowed_domains = ['kat.cr']
    start_urls = ['http://kat.cr/usearch/YIFY%201080/']
    
    def parse(self, response):
        
        for sel in response.css('.cellMainLink').extract():
            print sel
        print '*********************************************'
#         for sel in response.xpath('.//td[1]/div[2]/div/a/text()').extract():
#             print sel

        for sel in response.xpath('.//td[1]/div[2]/div'):
            print sel.xpath('a/text()').extract()[0]
#             raw_input()