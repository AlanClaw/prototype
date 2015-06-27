# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class KickassMovieItem(scrapy.Item):
    # define the fields for your item here like:

    movie_name_en        = scrapy.Field()
    movie_vintage        = scrapy.Field()
    torrent_dwn_link     = scrapy.Field()
    file_size_num        = scrapy.Field()
    file_size_unit       = scrapy.Field()
    seed_age             = scrapy.Field()
    seed_amount          = scrapy.Field()
    movie_name_ch_tw     = scrapy.Field()
    movie_info_link      = scrapy.Field()
    movie_trailer_link   = scrapy.Field()