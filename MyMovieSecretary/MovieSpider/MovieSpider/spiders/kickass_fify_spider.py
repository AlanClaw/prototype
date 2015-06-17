# -*- coding: utf-8 -*-
from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy import log

class KickassFifySpider(Spider):
    
    FIRST_PAGE = 'http://kat.cr/usearch/YIFY%201080/'

    name = 'Kickass_FIFY'
    allowed_domains = ['kat.cr']
    start_urls = []
    start_urls.append(FIRST_PAGE)
    
    def __init__(self, page_limit = 3):
        '''
        '''
        
        # setup all target URL
        for page_count in range(2, page_limit+1):
            url = '{0}/{1}'.format(KickassFifySpider.FIRST_PAGE, int(page_count))
            self.start_urls.append(url)
    
    def parse(self, response):
        '''
        '''
        
        # Movie name, size, download link

        for raw_sel in response.xpath('//tr')[2:]:
#             print raw_sel
            movie_name_vintage = raw_sel.xpath('.//td[1]/div[2]/div/a/text()').extract()[0]
            download_link      = raw_sel.xpath('.//td[1]/div[1]/a[5]/@href').extract()[0]
            file_size_num      = raw_sel.xpath('.//td[2]/text()').extract()[0]
            file_size_unit     = raw_sel.xpath('.//td[2]/span/text()').extract()[0]
            seed_age           = raw_sel.xpath('.//td[4]/text()').extract()[0]
            seed_amount        = raw_sel.xpath('.//td[5]/text()').extract()[0]
            
            log.msg(movie_name_vintage, level=log.DEBUG)
            log.msg(download_link     , level=log.DEBUG)
            log.msg(file_size_num     , level=log.DEBUG)
            log.msg(file_size_unit    , level=log.DEBUG)
            log.msg(seed_age          , level=log.DEBUG)
            log.msg(seed_amount       , level=log.DEBUG)
            
            
#         for title_sel in response.css('.cellMainLink').extract():
#             print title_sel
#         print '*********************************************'
#         for title_sel in response.xpath('.//td[1]/div[2]/div/a/text()').extract():
#             print title_sel

#         for title_sel in response.xpath('.//td[1]/div[2]/div'):
#             movie_name_vintage = title_sel.xpath('a/text()').extract()[0]
#             log.msg(movie_name_vintage, level=log.INFO)
#             log.msg(title_sel, level=log.INFO)

#         for movie_name_vintage in response.xpath('.//td[1]/div[2]/div/a/node()').extract():
#             print movie_name_vintage
# 
#         for file_size_num in response.xpath('.//td[2]/text()').extract():
#             print file_size_num
            
#             file_size_num = file_size_num.xpath('.//text()').extract()[0]
#             log.msg(file_size_num, level=log.INFO)