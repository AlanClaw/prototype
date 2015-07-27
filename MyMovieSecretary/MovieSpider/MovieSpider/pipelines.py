# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

import json
import functools



class MoviespiderPipeline(object):
    
    '''
    '''
    
    def __init__(self):
        '''
        '''
        self.file = None

    def check_spider_pipeline(process_item_method):
        '''
        '''

        @functools.wraps(process_item_method)
        def wrapper(self, item, spider):
            '''
            '''
#             print 'check_spider_pipeline():Wrapper()'
            
#             print self.__class__
#             print spider.pipeline
            
            # if class is in the spider's pipeline, then use the
            # process_item_method method normally.
            
            # message template for debugging
            msg = '%%s %s pipeline step' % (self.__class__.__name__)
            
            if self.__class__ in spider.pipeline:
                
                if self.file is None:
                    self.file = open('movie.jl', 'wb')
                
                spider.log(msg % 'executing', level=log.DEBUG)
                return process_item_method(self, item, spider)
    
            # otherwise, just return the untouched item (skip this step in
            # the pipeline)
            else:
                spider.log(msg % 'skipping', level=log.DEBUG)
                return item
    
        return wrapper
  
    @check_spider_pipeline        
    def process_item(self, item, spider):
        
        valid = True
        
        line = json.dumps(dict(item)) + "\n" 
        self.file.write(line)
        
        return item
