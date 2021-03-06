# -*- coding: utf-8 -*-
from scrapy.settings.default_settings import ITEM_PIPELINES

# Scrapy settings for MovieSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'MovieSpider'

SPIDER_MODULES = ['MovieSpider.spiders']
NEWSPIDER_MODULE = 'MovieSpider.spiders'

ITEM_PIPELINES = {'MovieSpider.pipelines.MoviespiderPipeline': 300}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'MovieSpider (+http://www.yourdomain.com)'
