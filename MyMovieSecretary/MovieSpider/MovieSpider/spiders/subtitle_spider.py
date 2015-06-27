# -*- coding: utf-8 -*-
from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy import log
from scrapy.http import Request

from MovieSpider.items import KickassMovieItem
from MovieSpider import pipelines

import json
import sys, time

# import selenium
from selenium import webdriver
from _cffi_backend import callback

class AtmoviesLocator(object):
        
    search_term               = "//input[@name='search_term']"
    search_btn                = "//form[@id='searchform']/div/button"
    
    search_result_1st         = ".//*[@id='main']/blockquote[1]/ol/li/a"
    movie_name_ch_tw          = ".//*[@id='main']/div[2]/div/p/span[1]"

class SubtitleSpider(Spider):
    
    FIRST_PAGE = 'http://www.atmovies.com.tw/home/'
    
    name = 'Subtitle'
    allowed_domains = ['atmovies.com.tw']
    start_urls = ['http://www.atmovies.com.tw/home/']
    
#     pipeline = set([])
    pipeline = set([
        pipelines.MoviespiderPipeline
    ])
    
    def __init__(self):
        '''
        '''
#         from pprint import pprint
#         with open('movie.jl') as movie_data_fp:
#             for line in movie_data_fp.readlines():
#                 data = json.loads(line)
#                 pprint(data)

        self.movie_datas = []

        
        # read all of json file into KickassMovieItem
        self.read_movie_src()
#         print self.movie_datas[0].get(u'movie_name_en')
        
        # build start_url
        self.get_all_search_result_link()
        self.start_requests()
#         self.selenium = selenium("localhost", 4444, "chrome", "http://www.atmovies.com.tw/home/")

#         self.driver.get("http://www.atmovies.com.tw/home/")

#         sel = self.selenium
#         sel.open("http://www.atmovies.com.tw/home/")

    def __del__(self):
        '''
        '''
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
            print movie_data.get(u'movie_info_link')
            yield Request(url = movie_data.get(u'movie_info_link'),
                          meta = {'movie_data': movie_data},
                          callback=self.parse,
                          dont_filter=True)
#             yield self.make_requests_from_url(url = movie_data.get(u'movie_info_link'),
#                           meta = {'movie_data': movie_data},
#                           callback=self.parse)
                
    def get_all_search_result_link(self):
        '''
        '''
#         self.selenium.start()
        self.driver = webdriver.Firefox()
        
#         self.driver.get("http://www.atmovies.com.tw/home/")
#         search_sel = self.driver.find_element_by_xpath(AtmoviesLocator.search_term)
#         search_sel.send_keys(self.movie_datas[0].get(u'movie_name_en'))
#         
#         search_btn = self.driver.find_element_by_xpath(AtmoviesLocator.search_btn)
#         search_btn.click()
#         
#         # waiting/ensure page loaded
#         # try to find link and click it
#         movie_link = self.driver.find_element_by_xpath(AtmoviesLocator.search_result_1st)
#         movie_link.click()
#         # get the url and add to url list
# #             print self.driver.current_url
# #         movie_data[u'movie_info_link'] = self.driver.current_url
#         
#         print self.driver.find_elements_by_xpath(AtmoviesLocator.movie_name_ch_tw)
#         raw_input('')
#         self.driver.close()

        for movie_data in self.movie_datas:

            try:
                self.driver.get("http://www.atmovies.com.tw/home/")
                
                search_sel = self.driver.find_element_by_xpath(AtmoviesLocator.search_term)
                search_sel.send_keys(movie_data.get(u'movie_name_en'))
                 
                search_btn = self.driver.find_element_by_xpath(AtmoviesLocator.search_btn)
                search_btn.click()
                 
                # waiting/ensure page loaded
                # try to find link and click it
                movie_link = self.driver.find_element_by_xpath(AtmoviesLocator.search_result_1st)
                movie_link.click()
                # get the url and add to url list
    #             print self.driver.current_url
                movie_data[u'movie_info_link'] = self.driver.current_url
                #             self.driver.close()
            except:
                continue
            
            time.sleep(1)
    
        self.driver.quit()
        
        
    def parse(self, response):
        '''
        '''
        movie_item = KickassMovieItem()

        data = response.meta['movie_data']

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
