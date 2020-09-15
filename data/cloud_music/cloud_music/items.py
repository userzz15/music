# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CloudMusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #歌手名字
    singer_name = scrapy.Field()
    #歌名
    music_name = scrapy.Field()
    #时长
    duration = scrapy.Field()
    #专辑
    album = scrapy.Field()
    #歌曲url
    music_url = scrapy.Field()
    #地区
    area_name = scrapy.Field()
    #所属类别
    sub_categorys_name = scrapy.Field()