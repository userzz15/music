import scrapy
from cloud_music.items import CloudMusicItem
import re

class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/']
    initials = [i for i in range(65,91)] + [0]

    def parse(self, response):
        print("start")
        lis = response.xpath("//div[@class='wrap f-pr']/ul/li")
        for li in lis:
            category = li.xpath(".//text()").get()
            url = response.urljoin(li.xpath(".//@href").get())
            if category == "歌手":
                yield scrapy.Request(url=url, callback=self.recommend_parse, meta={"category":category})


    def recommend_parse(self, response):
        """歌手"""
        category = response.meta.get("category")
        areas = response.xpath("//div[@class='g-wrap4 n-sgernav']/div[@class='blk']")
        for area in areas:
            area_name = area.xpath("./h2/text()").get()
            sub_categorys = area.xpath("./ul/li")
            for sub_category in sub_categorys:
                sub_category_name = sub_category.xpath("./a/text()").get()
                sub_category_url = response.urljoin(sub_category.xpath("./a/@href").get())
                for number in self.initials:
                    url = sub_category_url + '&initial=%d' %number
                yield scrapy.Request(url=url, callback=self.allsinger_parse, meta={"category":category, "area_name":area_name, "sub_category_name":sub_category_name})

    def allsinger_parse(self, response):
        """全部歌手"""
        category = response.meta.get("category")
        area_name = response.meta.get("area_name")
        sub_category_name = response.meta.get("sub_category_name")

        singer_lis = response.xpath("//div[@class='m-sgerlist']/ul/li")
        for li in singer_lis:
            # singer_name = li.xpath(".//a/@title").get()[:-3]
            singer_url = response.urljoin(li.xpath(".//a/@href").get())
            yield scrapy.Request(url=singer_url, callback=self.singer_home_parse, meta={"category":category, "area_name":area_name, "sub_category_name":sub_category_name})

    def singer_home_parse(self, response):
        """歌手主页"""
        category = response.meta.get("category")
        area_name = response.meta.get("area_name")
        sub_category_name = response.meta.get("sub_category_name")
        # singer_name = response.meta.get("singer_name")

        musics = response.xpath("//ul[@class='f-hide']/li")
        for music in musics:
            music_name = music.xpath("./a//text()").get()
            music_url = response.urljoin(music.xpath("./a//@href").get())
            yield scrapy.Request(url=music_url, callback=self.music_home_parse, meta={"category":category, "area_name":area_name, "sub_category_name":sub_category_name, "music_name":music_name, "music_url":music_url})
            # duration = 
            # album = 

    def music_home_parse(self, response):
        """歌曲主页"""
        print("123")
        category = response.meta.get("category")
        area_name = response.meta.get("area_name")
        sub_category_name = response.meta.get("sub_category_name")

        music_name = response.meta.get("music_name")
        music_url = response.meta.get("music_url")

        msg = response.xpath("//meta[@property='og:description']/@content").get()
        # (_,album) = re.findall(r"《(.*?)》",msg)
        te = re.findall(r"《(.*?)》",msg)
        if te:
            (_,album) = re.findall(r"《(.*?)》",msg)
        else:
            album = ""
        singer_name = re.findall(r"由 (.*?) 演唱",msg)[0]

        item = CloudMusicItem(singer_name = singer_name, music_name = music_name, album = album, music_url = music_url, area_name = area_name, sub_category_name = sub_category_name)
        yield item

    def resident_singer_parse(self, response):
        """入驻歌手"""
        pass


        

