# -*- coding: utf-8 -*-
from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy import log
from scrapy.http import Request

from MovieSpider.items import KickassMovieItem
from MovieSpider import pipelines

import json
import sys, time

from selenium import webdriver
from _cffi_backend import callback

class AtmoviesLocator(object):
        
    search_term               = "//input[@name='search_term']"
    search_btn                = "//form[@id='searchform']/div/button"
    
    search_result_1st         = ".//*[@id='main']/blockquote[1]/ol/li/a"
    movie_name_ch_tw          = ".//*[@id='main']/div[2]/div/p/span[1]"

class SubtitleSpider(Spider):
    
    HOME_PAGE = 'http://www.atmovies.com.tw/home/'
    
    name = 'Subtitle'
    allowed_domains = ['atmovies.com.tw']
    
    pipeline = set([
        pipelines.MoviespiderPipeline
    ])
    
    def __init__(self):
        '''
        '''

        self.movie_datas = []

        
        # read all of json file into KickassMovieItem
        self.read_movie_src()
        
        # build start_url
        self.get_all_search_result_link()
        self.start_requests()


    def __del__(self):
        '''
        '''
        pass
#         self.driver.close()
#         if self.driver is not None:
#             self.driver.quit()

    def read_movie_src(self):
        '''
        '''
        from pprint import pprint
        
        file_path = r'C:\Users\alan\Dropbox\Code\github\prototype\MyMovieSecretary\MovieSpider\MovieSpider\spiders\movie.jl'
        file_path = r'C:\Users\alan\Dropbox\Code\github\prototype\MyMovieSecretary\MovieSpider\movie.jl'
        
        with open(file_path) as movie_data_fp:
            
            for line in movie_data_fp.readlines():
                json_line_data = json.loads(line)
#                 pprint(json_line_data)
                
                self.movie_datas.append(json_line_data)
    
    def start_requests(self):
        '''
        '''
        log.msg('start_requests', level=log.DEBUG)
        for movie_data in self.movie_datas:
            
            movie_info_url = movie_data.get(u'movie_info_link')
            print movie_info_url
            
            if movie_info_url.startswith("http://"):
                log.msg('movie_info_url start with "http://"', level=log.DEBUG)
                yield Request(url = movie_info_url,
                              meta = {'movie_data': movie_data},
                              callback=self.parse,
                              dont_filter=True)
            else:
                log.msg('movie_info_url not start with "http://"', level=log.DEBUG)
                yield Request(url = self.HOME_PAGE,
                              meta = {'movie_data': movie_data},
                              callback=self.parse_nothing,
                              dont_filter=True)
            
        
    def get_all_search_result_link(self):
        '''
        '''
        self.driver = webdriver.Firefox()
        
        for movie_data in self.movie_datas:

            try:
                self.driver.get("http://www.atmovies.com.tw/home/")
                
                search_sel = self.driver.find_element_by_xpath(AtmoviesLocator.search_term)
                search_sel.send_keys(movie_data.get(u'movie_name_en'))
                 
                search_btn = self.driver.find_element_by_xpath(AtmoviesLocator.search_btn)
                search_btn.click()
                 
                # TODO:waiting/ensure page loaded
                # try to find link and click it
                movie_link = self.driver.find_element_by_xpath(AtmoviesLocator.search_result_1st)
                movie_link.click()
                # get the url and add to url list
                movie_data[u'movie_info_link'] = self.driver.current_url
                
            except:
                continue
            
            time.sleep(1)
    
        self.driver.quit()
        
        
    def parse(self, response):
        '''
        '''
        movie_item = KickassMovieItem()
        data = response.meta['movie_data']
        
        log.msg('parse()', level=log.DEBUG)
        print 'parse():{0}'.format(data.get(u'movie_name_en'))

        movie_item['movie_name_en']      = data.get(u'movie_name_en')
        movie_item['movie_vintage']      = data.get(u'movie_vintage') 
        movie_item['torrent_dwn_link']   = data.get(u'torrent_dwn_link') 
        movie_item['file_size_num']      = data.get(u'file_size_num') 
        movie_item['file_size_unit']     = data.get(u'file_size_unit') 
        movie_item['seed_age']           = data.get(u'seed_age') 
        movie_item['seed_amount']        = data.get(u'seed_amount')
        movie_item['movie_name_ch_tw']   = \
                response.xpath("//p/span/text()").extract()[0].strip()
        movie_item['movie_info_link']    = data.get(u'movie_info_link')
        movie_item['movie_trailer_link'] = data.get(u'movie_trailer_link')

        return movie_item

    def parse_nothing(self, response):
        '''
        '''
        movie_item = KickassMovieItem()
        data = response.meta['movie_data']
        
        log.msg('parse_nothing()', level=log.DEBUG)
        print 'parse_nothing():{0}'.format(data.get(u'movie_name_en'))
        
        movie_item['movie_name_en']      = data.get(u'movie_name_en')
        movie_item['movie_vintage']      = data.get(u'movie_vintage') 
        movie_item['torrent_dwn_link']   = data.get(u'torrent_dwn_link') 
        movie_item['file_size_num']      = data.get(u'file_size_num') 
        movie_item['file_size_unit']     = data.get(u'file_size_unit') 
        movie_item['seed_age']           = data.get(u'seed_age') 
        movie_item['seed_amount']        = data.get(u'seed_amount')
        movie_item['movie_name_ch_tw']   = data.get(u'movie_name_ch_tw')
        movie_item['movie_info_link']    = data.get(u'movie_info_link')
        movie_item['movie_trailer_link'] = data.get(u'movie_trailer_link')

        return movie_item
