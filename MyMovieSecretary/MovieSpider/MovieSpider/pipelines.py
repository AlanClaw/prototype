# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

import json

class MoviespiderPipeline(object):
    
    def __init__(self):
        '''
        '''
        
        self.file = open('movie.jl', 'wb')

    
    def process_item(self, item, spider):
        
        valid = True
        
        line = json.dumps(dict(item)) + "\n" 
        self.file.write(line) 
        
        return item
