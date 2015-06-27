# -*- coding: utf-8 -*-
from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy import log

from MovieSpider.items import KickassMovieItem
from MovieSpider import pipelines



class KickassFifySpider(Spider):
    
    FIRST_PAGE = 'http://kat.cr/usearch/YIFY%201080/'

    name = 'Kickass_FIFY'
    allowed_domains = ['kat.cr']
    start_urls = []
    start_urls.append(FIRST_PAGE)
    
    pipeline = set([
        pipelines.MoviespiderPipeline
    ])

    
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
        movie_item = KickassMovieItem()

        for raw_sel in response.xpath('//tr')[2:]: 
#             print raw_sel
            movie_name_vintage = raw_sel.xpath('.//td[1]/div[2]/div/a/text()').extract()[0]
            token = movie_name_vintage.split(u"(")
            movie_item['movie_name_en']      = token[0].strip()
            movie_item['movie_vintage']      = token[1].split(u")")[0].strip()
            movie_item['torrent_dwn_link']   = \
                raw_sel.xpath(".//td[1]/div[1]/a[@class='idownload icon16']/@href").extract()[0]
            movie_item['file_size_num']      = raw_sel.xpath('.//td[2]/text()').extract()[0]
            movie_item['file_size_unit']     = raw_sel.xpath('.//td[2]/span/text()').extract()[0]
            movie_item['seed_age']           = raw_sel.xpath('.//td[4]/text()').extract()[0]
            movie_item['seed_amount']        = raw_sel.xpath('.//td[5]/text()').extract()[0]
            
            movie_item['movie_name_ch_tw']   = ''
            movie_item['movie_info_link']    = ''
            movie_item['movie_trailer_link'] = ''
            
            yield movie_item
