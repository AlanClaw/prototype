# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieSpiderItem(scrapy.Item):
    # define the fields for your item here like:
#     name = scrapy.Field()
#     title = scrapy.Field()
#     link = scrapy.Field()
#     desc = scrapy.Field()

    torrent_title   = scrapy.Field()
    movie_name      = scrapy.Field()
    movie_vintage   = scrapy.Filld()
    torrent_link    = scrapy.Field()
    file_size       = scrapy.Field()
    seed_age        = scrapy.Field()
    seed_amount     = scrapy.Field()