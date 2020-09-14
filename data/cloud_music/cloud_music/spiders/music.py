import scrapy


class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['https://music.163.com/']
    start_urls = ['http://https://music.163.com//']

    def parse(self, response):
        print("="*30)
        print(response)
