# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest, response


class QuotesScrapeSpider(scrapy.Spider):
    name = 'quotes_scrape'
    allowed_domains = ['quotes.toscrape.com/js/']
    
    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url = "http://quotes.toscrape.com/js/", callback=self.parse, endpoint='execute', args={'lua_source':self.script})

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
               'quote_text': quote.xpath(".//span[@class='text']/text()").get(),
               'author': quote.xpath(".//small[@class='author']/text()").get(),
               'tags': quote.xpath(".//div[@class='tags']/a/text()").getall(),
         }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield SplashRequest(url = f"http://quotes.toscrape.com{next_page}", callback=self.parse, endpoint='execute', args={'lua_source':self.script})