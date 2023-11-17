# to run 
# scrapy crawl basketballreference_spider -o results.csv

import scrapy 

class BasketballreferenceSpider(scrapy.Spider):
    name = 'basketballreference_spider'
    
    start_urls = ['https://www.basketball-reference.com/leagues/']

    years = ["2023"]

    def parse(self, response):
        '''
        This method
        '''
        page = response.url + "/" + start_urls[0] # to get to season
        yield scrapy.Request(page, callback = self.parse_advanced_stats)

    def parse_advanced_stats(self, response):
        '''
        This method 
        '''
        yield response.css("div.all_advanced_team").css("a.dlink").get()